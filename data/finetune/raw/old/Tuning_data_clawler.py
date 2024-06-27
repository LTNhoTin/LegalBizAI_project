import re
import asyncio
import aiohttp
from motor.motor_asyncio import AsyncIOMotorClient
from tqdm import tqdm
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Kết nối tới MongoDB
client = AsyncIOMotorClient("mongodb://admin:password@localhost:27017/")
db = client['llm_finetune_db']
collection = db['finetune_pairs_v2']

# Số lượng yêu cầu đồng thời tối đa
MAX_CONCURRENCY = 100

# Đường dẫn tệp lỗi
ERROR_FILE_PATH = "/Users/nhotin/Documents/GitHub/LegalBizAI_project/data/finetune/raw/error.txt"

# Hàm hỗ trợ giới hạn số lượng yêu cầu đồng thời
async def gather_with_concurrency(coros):
    semaphore = asyncio.Semaphore(MAX_CONCURRENCY)
    async def sem_coro(coro):
        async with semaphore:
            return await coro
    return await asyncio.gather(*(sem_coro(c) for c in coros))

# Hàm lấy câu hỏi và câu trả lời từ trang web
async def get_ques_ans(site, session, executor):
    try:
        async with session.get(site) as response:
            html = await response.text()
            soup = await loop.run_in_executor(executor, BeautifulSoup, html, "lxml")

            qa_list = []
            ques = soup.find("section", class_="news-content", id="news-content")

            for h2_tag in ques.find_all("h2"):
                question = h2_tag.get_text(strip=True)
                answer = ""
                references = []

                # Lấy các đoạn văn bản trong tag p sau tag h2 hiện tại
                for p_tag in h2_tag.find_next_siblings("p"):
                    if p_tag.find("img") is None:
                        answer += p_tag.get_text() + "\n"
                    a_tags = p_tag.find_all("a")
                    for a_tag in a_tags:
                        references.append(a_tag.get("href"))

                qa = {
                    "question": question,
                    "answer": answer.strip(),
                    "references": references,
                    "request_link": site
                }

                if qa["answer"]:
                    qa_list.append(qa)

            if qa_list:
                await collection.insert_many(qa_list)
    except Exception as e:
        print(f"Error occurred for {site}: {e}")
        with open(ERROR_FILE_PATH, "a") as error_file:
            error_file.write(f"{site}\n")
            
# Hàm gọi hàm get_ques_ans với danh sách các liên kết
async def get_qa(links):
    async with aiohttp.ClientSession() as session:
        with ThreadPoolExecutor() as executor:
            with tqdm(total=len(links)) as pbar:
                await gather_with_concurrency([get_ques_ans(link, session, executor) for link in links])
                pbar.update(len(links))

# Đọc danh sách các liên kết từ file
with open("data/finetune/raw/example.txt", "r") as file:
    links = file.read().split("\n")

# Chạy chương trình
loop = asyncio.get_event_loop()
loop.run_until_complete(get_qa(links))

# Đóng kết nối MongoDB
client.close()