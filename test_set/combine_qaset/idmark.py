import re
import json
import pandas as pd

# Định nghĩa đường dẫn tới các tệp JSON
qaset_file = 'test_set/combine_qaset/qaset2.json'
all_chunk_file = 'test_set/id_cof/all_chunk.json'

# Đọc dữ liệu từ các tệp JSON
with open(qaset_file, 'r', encoding='utf-8') as f:
    df = json.load(f)

with open(all_chunk_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Định nghĩa phạm vi của các chunk
chunk_range = {
    "Luật Doanh nghiệp 2020": [0, 433],
    "Nghị định 01/2021/NĐ-CP": [434, 683],
    "Nghị định 16/2023/NĐ-CP": [684, 716],
    "Nghị định 23/2022/NĐ-CP": [717, 813],
    "Nghị định 47/2021/NĐ-CP": [814, 865],
    "Nghị định 122/2021/NĐ-CP": [866, 1001],
    "Nghị định 153/2020/NĐ-CP": [1002, 1114]
}

# Chuyển dữ liệu JSON thành DataFrame
df = pd.json_normalize(df)

# Thêm các cột cần thiết nếu chưa có
if 'chunk_ids' not in df.columns:
    df['chunk_ids'] = [[] for _ in range(len(df))]

if 'type_question' not in df.columns:
    df['type_question'] = ""

if 'chunk_range' not in df.columns:
    df['chunk_range'] = ""

# Hàm để khớp các tham chiếu và gán phạm vi chunk
def match_references_and_assign_chunk_ranges(references):
    chunk_ids = []
    range_chunks = []
    for ref in references:
        article, document = ref
        if document in chunk_range:
            chunk_ids_range = chunk_range[document]
            range_chunks.append(chunk_ids_range)
            matched_rows = [d for d in data if re.search(article, d['title']) and chunk_ids_range[0] <= d['id'] <= chunk_ids_range[1]]
            chunk_ids.extend([row['id'] for row in matched_rows])
    return chunk_ids, range_chunks

# Hàm gán ID và chunk range
def assign_chunk_ids_and_ranges(row):
    chunk_ids, chunk_ranges = match_references_and_assign_chunk_ranges(row['references'])
    if len(chunk_ids) <= 2:
        return chunk_ids, chunk_ranges
    return [], chunk_ranges

# Gán ID và phạm vi chunk vào các cột tương ứng
df[['chunk_ids', 'chunk_range']] = df.apply(assign_chunk_ids_and_ranges, axis=1, result_type='expand')

# Lưu lại DataFrame vào tệp JSON
with open(qaset_file, 'w', encoding='utf-8') as f:
    json.dump(df.to_dict('records'), f, ensure_ascii=False, indent=4)

print("Hoàn thành gán ID vào cột chunk_ids và chunk_range.")
