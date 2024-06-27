import re
import json
import bs4
import httpx
import asyncio
import nest_asyncio
import pymongo
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import urlparse, parse_qs

nest_asyncio.apply()

client = pymongo.MongoClient("mongodb://nhotin:password@localhost:27017/")
db = client["fine_tune_data"]
collection = db["training_data"]
error_collection = db["error_data"]

# File path
data_path = "/Users/nhotin/Documents/GitHub/LegalBizAI_project/data/finetune/raw/old/finetune_data_no_base_no_taive.json"

NEWLINE_REGEX = r"(\r\n|\r|\n)"

def array_index(arr, value):
    try:
        return arr.index(value)
    except ValueError:
        return None

def filter_text(text, remove_ellipsis=True):
    if remove_ellipsis:
        text = re.sub(rf"{NEWLINE_REGEX}[.]{{3}}", "", text)
    text = re.sub(r"[^\S\r\n]+", " ", text)
    return text.strip()

def get_tag_content(tag):
    text = "".join(
        re.sub(NEWLINE_REGEX, " ", child.text) for child in tag.contents)
    return text.strip()

def get_query_dict(url):
    return parse_qs(urlparse(url).query)

async def gather_with_concurrency(n, *coros):
    semaphore = asyncio.Semaphore(n)

    async def sem_coro(coro):
        async with semaphore:
            return await coro

    return await asyncio.gather(*(sem_coro(c) for c in coros))

processed_sites = {}

# fetch law domain and keywords
async def fetch_law_metadata(aclient, site):
    metadata = {"domain_name": None, "domain_code": None, "keywords": []}

    try:
        response = await aclient.get(site)
        soup = BeautifulSoup(response.content, "html.parser")
        law_domain = soup.find(class_="tvpl-breadcrumb breadcrumb")
        if law_domain:
            anchor = law_domain.select("a")[-1]
            metadata["domain_code"] = anchor.get("href").split("/")[-1]

            law_domain_text = re.sub(r"\s+", " ", law_domain.text)
            metadata["domain_name"] = law_domain_text.split("/")[-1].split(
                "về")[-1].strip()

        keywords = soup.select(".kwseo")
        for kw in keywords:
            keyword_text = re.sub(r"\s+", " ", kw.text)
            metadata["keywords"].append(keyword_text)
    except Exception as e:
        raise ValueError(f"Error fetching metadata from {site}: {e}")

    return metadata

async def get_law_content(aclient, law_link):
    ordered_anchors = list(
        reversed(
            ("phan", "chuong", "muc", "tieu_muc", "dieu", "khoan", "diem")))

    try:
        response = await aclient.get(law_link)
        soup = BeautifulSoup(response.content, "html.parser")
        law_doc = soup.select_one(".content1")

        anchor_value = get_query_dict(law_link)["anchor"][0]
        start_anchor_name = anchor_value.split("_")[0]
        start_anchor_level = array_index(ordered_anchors, start_anchor_name)
        if start_anchor_level is None:
            raise ValueError(f"Invalid anchor level for {law_link}")

        current = law_doc.select_one(f':has(> a[name="{anchor_value}"])')
        if not current:
            raise ValueError(f"Could not find start anchor in {law_link}")

        law_lines = [get_tag_content(current)]

        for current in current.next_siblings:
            if isinstance(current, bs4.element.NavigableString):
                if stripped_text := current.text.strip():
                    law_lines.append(stripped_text)
                continue
            elif current.name != "p":
                break

            current_anchor = current.select_one("a[name]")
            if not current_anchor:
                law_lines.append(get_tag_content(current))
            else:
                current_anchor_name = current_anchor.get("name").split("_")[0]
                current_anchor_level = array_index(ordered_anchors,
                                                   current_anchor_name)
                if current_anchor_level is None or current_anchor_level < start_anchor_level:
                    law_lines.append(get_tag_content(current))
                else:
                    break
            current = current.next_sibling

        return "\n".join(law_lines)
    except Exception as e:
        raise ValueError(f"Error fetching content from {law_link}: {e}")

async def fetch_base_data(item, pbar):
    async with httpx.AsyncClient(timeout=None,
                                 follow_redirects=True) as aclient:
        req_link = item["request_link"].strip()
        try:
            if req_link not in processed_sites:
                processed_sites[req_link] = await fetch_law_metadata(
                    aclient, req_link)
            new_item = {**processed_sites[req_link], **item}
            del new_item["base_content"]

            new_item["reference_passages"] = await gather_with_concurrency(
                2,
                *(get_law_content(aclient, law_link.strip())
                  for law_link in new_item["references"]))
            collection.insert_one(new_item)
        except Exception as e:
            error_collection.insert_one({
                "request_link": req_link,
                "question": item.get("question"),
                "references": item.get("references"),
                "base_content": None,
                "error": str(e)
            })
        pbar.update(1)

async def crawl_fullbase_data(items):
    with tqdm(total=len(items)) as pbar:
        await gather_with_concurrency(
            50, *(fetch_base_data(item, pbar) for item in items))

with open(data_path, "r", encoding="utf-8") as f_data:
    data = json.load(f_data)

asyncio.run(crawl_fullbase_data(data))
