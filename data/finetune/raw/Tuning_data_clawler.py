from bs4 import BeautifulSoup
import re
import asyncio
import httpx
from motor.motor_asyncio import AsyncIOMotorClient
from tqdm import tqdm

# Thêm header Authorization nếu cần
headers = {
    # "Authorization": "SAPISIDHASH 5832935a601c3623cbe544548dcfde01aa5a2949",
}

# Kết nối tới MongoDB
client = AsyncIOMotorClient("mongodb://admin:password@localhost:27017/")
db = client['llm_finetune_db']
collection = db['finetune_pairs']

# Hàm hỗ trợ giới hạn số lượng yêu cầu đồng thời
async def gather_with_concurrency(n, *coros):
    semaphore = asyncio.Semaphore(n)
    async def sem_coro(coro):
        async with semaphore:
            return await coro
    return await asyncio.gather(*(sem_coro(c) for c in coros))

# Hàm lấy câu hỏi và câu trả lời từ trang web
async def getQues_Ans(site, pbar):
    try:
        async with httpx.AsyncClient(timeout=None, follow_redirects=True) as QA_site:
            QA_raw = await QA_site.get(site)
            QA_soup = BeautifulSoup(QA_raw.text, "lxml")

            valid_tag = {"h2", "p", "blockquote"}
            QA_list = []
            save = False
            flag = False
            QA = None
            Ques = QA_soup.find("section", class_="news-content", id="news-content")

            for descendant in Ques.descendants:
                tag = descendant.name
                if tag in valid_tag:
                    if tag == "h2":
                        flag = True
                        if save and QA and QA["answer"].strip() and QA["base_content"].strip():
                            QA["answer"] += " Căn cứ vào " + ", ".join(QA["references"])
                            QA_list.append(QA)
                        QA = {
                            "question": descendant.get_text(strip=True),
                            "answer": "",
                            "base_content": "",
                            "references": [],
                            "blockquote": ""
                        }
                        save = True
                    if not flag:
                        continue
                    if tag == "blockquote":
                        QA["base_content"] += descendant.text + "\n"
                    if tag == "p" and descendant.find("img") is None:
                        next_sibling = descendant.find_next_sibling()
                        prev_sibling = descendant.find_previous_sibling()
                        if (next_sibling and next_sibling.name == "blockquote") or (prev_sibling and prev_sibling.name == "h2"):
                            try:
                                a_tag = descendant.find("a")
                                law_name = a_tag.text
                                ref = descendant.get_text()
                                pattern = fr'(?<=tại)\s*(.*?)\s*(?={law_name})' if 'tại' in ref else fr'(?<=vào)\s*(.*?)\s*(?={law_name})'
                                QA["references"].append(re.findall(pattern, ref)[0] + " " + law_name)
                            except:
                                save = False
                                continue
                            QA["base_content"] += ref + "\n"
                        elif descendant.em is None:
                            QA["answer"] += descendant.get_text() + "\n"
            
            if QA and save:
                QA_list.append(QA)
            
            if QA_list:
                await collection.insert_many(QA_list)
            pbar.update(1)
    except Exception as e:
        print(e)
        with open("data_processing/data4llm/error.txt", "a") as ferror:
            ferror.write(site + "\n")

# Hàm gọi hàm getQues_Ans với danh sách các liên kết
async def getQA(links):
    with tqdm(total=len(links)) as pbar:
        await gather_with_concurrency(100, *(getQues_Ans(link, pbar) for link in links))

# Đọc danh sách các liên kết từ file
with open("data_processing/data4llm/example copy.txt", "r") as file:
    links = file.read().split("\n")

# Chạy chương trình
asyncio.run(getQA(links[:20]))

# Đóng kết nối MongoDB
client.close()
