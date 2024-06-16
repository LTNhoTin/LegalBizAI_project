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

            valid_tag = {"h2", "p", "a"}
            qa_list = []
            save = False
            flag = False
            qa = None
            ques = soup.find("section", class_="news-content", id="news-content")

            for descendant in ques.descendants:
                tag = descendant.name
                if tag in valid_tag:
                    if tag == "h2":
                        flag = True
                        if save and qa and qa["answer"].strip() and qa["base_content"].strip():
                            qa["answer"] += " Căn cứ vào " + ", ".join(qa["references"])
                            qa_list.append(qa)
                        qa = {
                            "request_link": site,  # Thêm đường dẫn liên kết vào đây
                            "question": descendant.get_text(strip=True),
                            "answer": "",
                            "base_content": "",
                            "references": []
                        }
                        save = True
                    if not flag:
                        continue
                    if tag == "a":
                        qa["references"].append(descendant.get("href"))
                    if tag == "p" and descendant.find("img") is None:
                        next_sibling = descendant.find_next_sibling()
                        prev_sibling = descendant.find_previous_sibling()
                        if (next_sibling and next_sibling.name == "blockquote") or (prev_sibling and prev_sibling.name == "h2"):
                            try:
                                a_tag = descendant.find("a")
                                law_name = a_tag.text
                                ref = descendant.get_text()
                                pattern = fr'(?<=tại)\s*(.*?)\s*(?={law_name})' if 'tại' in ref else fr'(?<=vào)\s*(.*?)\s*(?={law_name})'
                                qa["references"].append(re.findall(pattern, ref)[0] + " " + law_name)
                            except:
                                save = False
                                continue
                            qa["base_content"] += ref + "\n"
                        elif descendant.em is None:
                            qa["answer"] += descendant.get_text() + "\n"
                    elif tag == "p" and qa is not None:
                        qa["base_content"] += descendant.get_text() + "\n"

            if qa and save:
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