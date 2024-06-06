import re
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
import json
import pandas as pd

v = '/Users/nhotin/Documents/GitHub/LegalBizAI_project/test_set/id_cof/qaset.json'
with open(v, 'r', encoding='utf-8') as f:
    df = json.load(f)

json_file_path = '/Users/nhotin/Documents/GitHub/LegalBizAI_project/test_set/id_cof/all_chunk.json'
with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Define the chunk range mapping
chunk_range = {
    "Luật Doanh nghiệp 2020": [0, 433],
    "Nghị định 01/2021/NĐ-CP": [434, 683],
    "Nghị định 16/2023/NĐ-CP": [684, 716],
    "Nghị định 23/2022/NĐ-CP": [717, 813],
    "Nghị định 47/2021/NĐ-CP": [814, 865],
    "Nghị định 122/2021/NĐ-CP": [866, 1001],
    "Nghị định 153/2020/NĐ-CP": [1002, 1114]
}
df = pd.json_normalize(df)
item = df.columns
df = df.drop(columns=["asigned"])
# Add chunk_ids and type_question fields if they don't exist
if 'chunk_ids' not in df.columns:
    df['chunk_ids'] = ""
if 'asigned' not in df.columns:
    df["asigned"] = ""
if 'type_question' not in df.columns:
    df['type_question'] = ""

# Function to extract articles
def extract_articles(reference):
    pattern = re.compile(r'Điều \d+')
    matches = pattern.findall(reference)
    return ', '.join(matches)

# Function to match references and get the chunk_ids ranges
def match_references_and_assign_chunk_ids(references):
    chunk_ids = []
    for ref in references:
        article, document = ref
        if document in chunk_range:
            chunk_ids_range = chunk_range[document]
            matched_rows = [d for d in data if re.search(article, d['title']) and chunk_ids_range[0] <= d['id'] <= chunk_ids_range[1]]
            chunk_ids.extend([row['id'] for row in matched_rows])
    return chunk_ids

# Apply the function to assign chunk_ids to each item in df
df["chunk_ids"] = df["references"].apply(match_references_and_assign_chunk_ids)

root = tk.Tk()
root.title("Gán ID và loại câu hỏi")
root.geometry("1000x900")

# Tìm ô đầu tiên của câu hỏi chưa có ID
def find_first_empty_id(df):
    id_cl = df["asigned"].tolist()
    for index in range(len(id_cl)):
        if not id_cl[index]:
            return index
    return 0

current_index = find_first_empty_id(df)



def update_progress():
    progress_label.config(text=f"{current_index}/{len(df)} câu đã hoàn thành")
    root.update_idletasks()

def create_id_entries(reference_count):
    for widget in id_entries_frame.winfo_children():
        widget.destroy()

    global id_entries
    id_entries = []

    for i in range(reference_count):
        label = tk.Label(id_entries_frame, text=f"Nhập ID {i+1}:", font=("Helvetica", 16))
        label.pack(side=tk.LEFT)
        entry = tk.Entry(id_entries_frame, font=("Helvetica", 16))
        entry.pack(side=tk.LEFT, padx=5)
        id_entries.append(entry)

def next_question():
    global current_index
    if current_index >= len(df):
        messagebox.showinfo("Hoàn thành", "Bạn đã gán ID cho tất cả các câu hỏi.")
        return

    row = df.iloc[current_index]

    question_text.config(state=tk.NORMAL)
    question_text.delete(1.0, tk.END)
    question_text.insert(tk.END, "Question: ", "red")
    question_text.insert(tk.END, f"{row['question']}\n\n")
    question_text.insert(tk.END, "Answer: ", "green")
    question_text.insert(tk.END, f"{row['answer']}\n\n")
    question_text.insert(tk.END, "Reference: ", "green")
    question_text.insert(tk.END, f"{row['references']}\n\n")
    question_text.config(state=tk.DISABLED)

    # Hiển thị type_question nếu có
    type_entry.delete(0, tk.END)
    if row['type_question']:
        type_entry.insert(0, row['type_question'])

    passage_text.config(state=tk.NORMAL)
    passage_text.delete(1.0, tk.END)
    if row['chunk_ids']:
        for chunk_id in row['chunk_ids']:
            match = next((d for d in data if d['id'] == chunk_id), None)
            if match:
                passage_text.insert(tk.END, "ID: ", "red")
                passage_text.insert(tk.END, f"{match['id']}\n", "red")
                passage_text.insert(tk.END, "Title: ", "green")
                passage_text.insert(tk.END, f"{match['title']}\n", "green")
                passage_text.insert(tk.END, f"Passage: {match['passage']}\n{'-'*50}\n")
    else:
        passage_text.insert(tk.END, "Không có khớp nào tìm thấy.")
    passage_text.config(state=tk.DISABLED)

    # Tạo các ô nhập ID động
    references = row['references']
    create_id_entries(len(references))
    update_progress()

def save_id(event=None):
    global current_index
    ids = [entry.get() for entry in id_entries]
    question_type = type_entry.get()
    df.at[current_index , 'asigned'] = ids
    df.at[current_index , 'type_question'] = question_type
    current_index += 1
    if current_index < len(df):
        next_question()
    else:
        messagebox.showinfo("Hoàn thành", "Bạn đã gán ID cho tất cả các câu hỏi.")
    with open(v, 'w', encoding='utf-8') as f:
        json.dump(df.to_dict(orient='records'), f, ensure_ascii=False, indent=4)

def previous_question():
    global current_index
    if current_index > 0:
        current_index -= 1
        next_question()
    else:
        messagebox.showwarning("Cảnh báo", "Đây là câu hỏi đầu tiên.")

question_frame = tk.LabelFrame(root, text="Câu hỏi và câu trả lời", padx=10, pady=10)
question_frame.pack(fill="both", expand="yes", padx=10, pady=10)
question_text = scrolledtext.ScrolledText(question_frame, height=10, wrap=tk.WORD, font=("Helvetica", 16))
question_text.pack(fill="both", expand=True)
question_text.tag_config("red", foreground="red")
question_text.tag_config("green", foreground="green")
question_text.tag_config("blue", foreground="blue")
question_text.config(state=tk.DISABLED)

passage_frame = tk.LabelFrame(root, text="Các khớp có thể", padx=10, pady=10)
passage_frame.pack(fill="both", expand="yes", padx=10, pady=10)
passage_text = scrolledtext.ScrolledText(passage_frame, height=20, wrap=tk.WORD, font=("Helvetica", 16))
passage_text.pack(fill="both", expand=True)
passage_text.tag_config("red", foreground="red")
passage_text.tag_config("green", foreground="green")
passage_text.config(state=tk.DISABLED)

id_progress_frame = tk.Frame(root)
id_progress_frame.pack(pady=10)

id_entries_frame = tk.Frame(id_progress_frame)
id_entries_frame.pack()

type_label = tk.Label(id_progress_frame, text="Loại câu hỏi:", font=("Helvetica", 16))
type_label.pack(side=tk.LEFT)
type_entry = tk.Entry(id_progress_frame, font=("Helvetica", 16))
type_entry.pack(side=tk.LEFT, padx=5)
type_entry.bind("<Return>", save_id)

progress_label = tk.Label(id_progress_frame, text="", font=("Helvetica", 16))
progress_label.pack(side=tk.LEFT, padx=10)
update_progress()

button_frame = tk.Frame(root)
button_frame.pack(pady=10)
save_button = tk.Button(button_frame, text="Lưu ID và loại câu hỏi", command=save_id, font=("Helvetica", 14))
save_button.pack(side=tk.LEFT, padx=5)
back_button = tk.Button(button_frame, text="Quay lại câu hỏi trước", command=previous_question, font=("Helvetica", 14))
back_button.pack(side=tk.LEFT, padx=5)

next_question()
root.mainloop()
