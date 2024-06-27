from bs4 import BeautifulSoup
import re
import asyncio
import httpx
from motor.motor_asyncio import AsyncIOMotorClient
from tqdm import tqdm

headers = {
    # "Authorization": "SAPISIDHASH 5832935a601c3623cbe544548dcfde01aa5a2949",

}
client = AsyncIOMotorClient("mongodb://admin:password@localhost:27017/")

db = client['QA']
collection = db['thuvienphapluat']



async def gather_with_concurrency(n, *coros):
    semaphore = asyncio.Semaphore(n)
    async def sem_coro(coro):
        async with semaphore:
            return await coro
    return await asyncio.gather(*(sem_coro(c) for c in coros))


def verify_refer_link(link):
    valid_link = {
         "https://thuvienphapluat.vn/van-ban/Doanh-nghiep/Luat-Doanh-nghiep-so-59-2020-QH14-427301.aspx",
         "https://thuvienphapluat.vn/van-ban/Doanh-nghiep/Nghi-dinh-16-2023-ND-CP-to-chuc-quan-ly-doanh-nghiep-truc-tiep-phuc-vu-quoc-phong-an-ninh-564517.aspx",
         "https://thuvienphapluat.vn/van-ban/Chung-khoan/Nghi-dinh-08-2023-ND-CP-sua-doi-Nghi-dinh-chao-ban-giao-dich-trai-phieu-doanh-nghiep-rieng-le-557520.aspx",
         "https://thuvienphapluat.vn/van-ban/Doanh-nghiep/Nghi-dinh-65-2022-ND-CP-sua-doi-Nghi-dinh-153-2020-ND-CP-chao-ban-giao-dich-trai-phieu-doanh-nghiep-529835.aspx",
         "https://thuvienphapluat.vn/van-ban/Doanh-nghiep/Nghi-dinh-23-2022-ND-CP-thanh-lap-doanh-nghiep-do-Nha-nuoc-nam-giu-100-von-dieu-le-509241.aspx",
         "https://thuvienphapluat.vn/van-ban/Dau-tu/Nghi-dinh-122-2021-ND-CP-xu-phat-vi-pham-hanh-chinh-linh-vuc-ke-hoach-285024.aspx",
         "https://thuvienphapluat.vn/van-ban/Doanh-nghiep/Nghi-dinh-47-2021-ND-CP-huong-dan-Luat-Doanh-nghiep-470561.aspx",
         "https://thuvienphapluat.vn/van-ban/Doanh-nghiep/Nghi-dinh-01-2021-ND-CP-dang-ky-doanh-nghiep-283247.aspx",
         "https://thuvienphapluat.vn/van-ban/Chung-khoan/Nghi-dinh-153-2020-ND-CP-chao-ban-giao-dich-trai-phieu-doanh-nghiep-tai-thi-truong-trong-nuoc-461187.aspx"
    }
    main_link = link.split("?")[0]
    status = main_link in valid_link
    return status    

async def getQues_Ans(site,pbar):
    try:
        async with httpx.AsyncClient(timeout=None, follow_redirects=True) as QA_site:
            QA_raw = await QA_site.get(site)
            QA_raw = QA_raw.text
            valid_tag = {"h2","p","blockquote"}
            QA_soup = BeautifulSoup(QA_raw,"lxml")
            QA_list = []
            save = False
            flag = False
            Ques = QA_soup.find("section", class_="news-content", id="news-content")
            for descendant in Ques.descendants:
                if ((tag := descendant.name) in valid_tag):
                    if (tag == "h2"):
                        flag = True 
                        if ((save == True) and QA):
                            QA_list.append(QA)
                        QA = dict()
                        save = True
                        QA["question"] = descendant.get_text(strip=True)
                        QA["answer"] = ""
                        QA["references"] = []
                    if not flag:
                        continue
                    if tag == "blockquote":
                                QA["answer"] = QA["answer"] + descendant.text + "\n"
                    if (tag == "p") and (descendant.find("img") is None):
                        next_sibling = descendant.find_next_sibling()
                        prev_sibling = descendant.find_previous_sibling()
                        if (next_sibling and next_sibling.name == "blockquote") or (prev_sibling and prev_sibling.name == "h2"):
                            try:
                                a_tag = descendant.find("a")
                                law_link = a_tag.get("href")  
                                law_name = a_tag.text
                                ref = descendant.get_text()
                                pattern = fr'(?<=tại)\s*(.*?)\s*(?={law_name})'
                                QA["references"].append(re.findall(pattern, ref)[0] + " " + law_name)
                            except:
                                    save = False
                                    continue
                            if not verify_refer_link(law_link):
                                save = False
                                continue

                            QA["answer"] = QA["answer"] + ref + "\n"
                        
                        elif (descendant.em is None):
                            QA["answer"] = QA["answer"] + descendant.get_text() + "\n"

            if (QA  and (save == True)):
                QA_list.append(QA)

            if QA_list:
                await collection.insert_many(QA_list)
            pbar.update(1)
    except:
        with open("error.txt", "a") as ferror:
            ferror.write(site + "\n")       
async def getQA(links):
    
    with tqdm(total=len(links)) as pbar:
        await gather_with_concurrency(100,*(getQues_Ans(link, pbar) for link in links))
        

# async def getQA(links):
#     await gather_with_concurrency(100,*(getQues_Ans(link) for link in links))
                
            
with open("error.txt", "r") as file:
    links = file.read().split("\n")

asyncio.run(getQA(links))

client.close()


#57060