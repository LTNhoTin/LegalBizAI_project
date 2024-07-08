import json
import re
import unicodedata as ud

import faiss
import numpy as np
import pandas as pd

# from configs.paths import relative_path
from langchain_community.vectorstores import FAISS
# from tqdm import tqdm
from underthesea import word_tokenize

bizlaw_short_dict = {
    "BCC": "hợp tác kinh doanh",
    "BHTN": "Bảo hiểm thất nghiệp",
    "BHXH": "Bảo hiểm xã hội",
    "BHYT": "Bảo hiểm y tế",
    "CT": "Công ty",
    "CTCP": "Công ty cổ phần",
    "DNTN": "Doanh nghiệp tư nhân",
    "DV": "Dịch vụ",
    "EUR": "Euro",
    "EVN": "Điện lực Việt Nam",
    "GCN": "Giấy chứng nhận",
    "GPS": "hệ thống định vị toàn cầu GPS",
    "HĐQT": "Hội đồng quản trị",
    "JPY": "Yên Nhật",
    "MTV": "Một thành viên",
    # "ODA": "Hỗ trợ phát triển chính thức",
    # "PPP": "theo phương thức đối tác công tư",
    "STT": "Số thứ tự",
    "TM": "Thương mại",
    "TNDN": "thu nhập doanh nghiệp",
    "TNHH": "Trách nhiệm hữu hạn",
    "TP": "Thành phố",
    "USD": "Đô la Mỹ",
    "ĐHĐCĐ": "Đại hội đồng cổ đông",
    "ĐKKD": "Đăng ký kinh doanh",
}
stop_words_vn = set(
    [
        "và",
        "của",
        "là",
        "các",
        "trong",
        "với",
        "cho",
        "để",
        "những",
        "khi",
        "thì",
        "này",
        "làm",
        "từ",
        "đã",
        "sẽ",
        "rằng",
        "mà",
        "như",
        "lại",
        "ra",
        "sau",
        "cũng",
        "vậy",
        "nếu",
        "đến",
        "thế",
        "biết",
        "theo",
        "đâu",
        "đó",
        "trước",
        "vừa",
        "rồi",
        "trên",
        "dưới",
        "ngoài",
        "gì",
        "còn",
        "nữa",
        "nào",
        "hết",
        "ai",
        "ấy",
        "lúc",
        "ở",
        "đi",
        "về",
        "ngay",
        "luôn",
        "đang",
        "thì",
        "đây",
        "kia",
        "ấy",
        "điều",
        "việc",
        "vì",
        "giữa",
        "qua",
        "vẫn",
        "chỉ",
        "nói",
        "thật",
        "hơn",
        "vậy",
        "hay",
        "lại",
        "ngày",
        "giờ",
        "tại",
        "bởi",
        "sao",
        "trước",
        "sau",
        "đó",
        "mà",
        "về",
        "đến",
        "thì",
        "được",
        "thế",
        "còn",
        "đến",
        "cũng",
        "này",
        "đấy",
        "một",
        "vì",
        "những",
        "thì",
        "vậy",
        "thế",
        "đây",
        "vẫn",
        "lại",
        "thì",
        "còn",
        "đó",
        "này",
        "ở",
        "trong",
        "làm",
        "khi",
        "vậy",
        "này",
        "đó",
        "ở",
        "được",
        "làm",
        "để",
        "khi",
        "với",
        "về",
        "đi",
        "cho",
        "về",
        "đã",
        "với",
        "như",
        "đi",
        "này",
        "như",
        "được",
        "cho",
        "thì",
        "làm",
        "ở",
        "như",
        "điều",
        "khi",
        "với",
        "trong",
    ]
)

index_path = "data/faiss_index"

faiss_index = faiss.read_index(index_path)


def tokenizer(text):
    text = re.sub(r"[^\w\s%]", "", ud.normalize("NFC", text))
    words = text.split()
    for idx in range(len(words)):
        if words[idx] in bizlaw_short_dict.keys():
            words[idx] = bizlaw_short_dict[words[idx]]
    temp = " ".join(words).lower()

    # words = word_tokenize(temp, format="text")
    return temp


from sentence_transformers import SentenceTransformer

# Load the model from the local directory
model = SentenceTransformer("models/embedding")

def get_embedding(text):
    return model.encode(text)


def load_chunks(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


chunks = load_chunks("data/all_chunks_by_clauseWarticle.json")


def get_question_embedding(question):
    return get_embedding(question)


def get_full_article(chunk_ids: list[int]) -> dict:
    """
    description: get the full article passage of a chunk by id

    input:
        chunks: list of chunk objects
        chunk_id: the chunk id to be retrieved passage
    output:
        tuple: (concatenation of articles passage, all article chunk ids)

    notes:
        Article: Điều
        Clause: Khoản
        Point: Điểm
    """
    articles_ids = set()
    for chunk_id in chunk_ids:
        if chunk_id in articles_ids:
            continue
        articles_ids.add(chunk_id)
        chunk_title = chunks[chunk_id]["title"]
        run_id = chunk_id - 1
        while run_id >= 0 and chunks[run_id]["title"] == chunk_title:
            articles_ids.add(run_id)
            run_id -= 1
        run_id = chunk_id + 1
        while run_id < len(chunks) and chunks[run_id]["title"] == chunk_title:
            articles_ids.add(run_id)
            run_id += 1
    articles_ids = sorted(articles_ids)
    content_lines = []
    chunk_title = ""
    for id in articles_ids:
        if chunk_title != chunks[id]["title"]:
            chunk_title = chunks[id]["title"]
            content_lines.append(chunk_title)
        passage_lines = chunks[id]["passage"].splitlines()
        content_lines.extend(passage_lines[1:])
    content = "\n".join(content_lines)
    return {"ids": articles_ids, "content": content}


def retrieve(ques, topk=3):
    ques_embedding = model.encode(tokenizer(ques))
    _, I = faiss_index.search(np.array([ques_embedding]), k=topk)
    return get_full_article(I[0].tolist())["ids"]
