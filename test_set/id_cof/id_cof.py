import re
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import json
import pandas as pd

font_content = ("Helvetica", 14)

qaset_file = r"test_set/id_cof/qaset.json"
all_chunk_file = r"test_set/id_cof/qaset.json"

with open(qaset_file, "r", encoding="utf-8") as f:
    df = json.load(f)

with open(all_chunk_file, "r", encoding="utf-8") as f:
    data = json.load(f)

chunk_range = {
    "Luật Doanh nghiệp 2020": [0, 433],
    "Nghị định 01/2021/NĐ-CP": [434, 683],
    "Nghị định 16/2023/NĐ-CP": [684, 716],
    "Nghị định 23/2022/NĐ-CP": [717, 813],
    "Nghị định 47/2021/NĐ-CP": [814, 865],
    "Nghị định 122/2021/NĐ-CP": [866, 1001],
    "Nghị định 153/2020/NĐ-CP": [1002, 1114],
}

df = pd.json_normalize(df)
item = df.columns

if "chunk_ids" not in df.columns:
    df["chunk_ids"] = [[] for _ in range(len(df))]

if "type_question" not in df.columns:
    df["type_question"] = ""

if "chunk_range" not in df.columns:
    df["chunk_range"] = ""


def match_references_and_assign_chunk_ranges(references):
    chunk_ranges = []
    for ref in references:
        article, document = ref
        if document in chunk_range:
            chunk_ids_range = chunk_range[document]
            matched_rows = [
                d
                for d in data
                if re.search(article, d["title"]) and chunk_ids_range[0] <= d["id"] <= chunk_ids_range[1]
            ]
            chunk_ranges.extend([row["id"] for row in matched_rows])
    return chunk_ranges


df["chunk_range"] = df["references"].apply(match_references_and_assign_chunk_ranges)


def adjust_window_size(root):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # Adjusting the window size to 80% of the screen size
    width = int(screen_width * 0.8)
    height = int(screen_height * 0.8)
    root.geometry(f"{width}x{height}")


root = tk.Tk()
root.title("Gán ID và loại câu hỏi")
adjust_window_size(root)


def find_first_empty_id(df):
    for index, chunk_ids in enumerate(df["chunk_ids"]):
        if not chunk_ids:
            return index
    return 0


current_index = find_first_empty_id(df)


def update_progress():
    progress_label.config(text=f"{current_index}/{len(df)} câu đã hoàn thành")
    root.update_idletasks()


def create_id_entries(reference_count, saved_ids):
    for widget in id_entries_frame.winfo_children():
        widget.destroy()

    global id_entries
    id_entries = []

    if reference_count > 1:
        label = tk.Label(
            id_entries_frame, text="Cảnh báo: Câu này có nhiều hơn một reference!", font=font_content, fg="red"
        )
        label.grid(row=0, column=0, columnspan=2)

    label = tk.Label(id_entries_frame, text="Nhập ID:", font=font_content)
    label.grid(row=1, column=0, padx=5, pady=5)
    entry = tk.Entry(id_entries_frame, font=font_content)
    entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew", columnspan=2)
    id_entries.append(entry)

    if saved_ids:
        entry.insert(0, ",".join(map(str, saved_ids)))


def next_question():
    global current_index
    if current_index == len(df) - 1:
        messagebox.showinfo("Hoàn thành", "Bạn đã gán ID cho tất cả các câu hỏi.")
        return

    current_index += 1
    display_current_question()


def display_current_question():
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

    type_select.delete(0, tk.END)
    if row["type_question"]:
        # type_entry.insert(0, row["type_question"])
        type_select.set(row["type_question"])

    passage_text.config(state=tk.NORMAL)
    passage_text.delete(1.0, tk.END)
    if row["chunk_range"]:
        for chunk_id in row["chunk_range"]:
            match = next((d for d in data if d["id"] == chunk_id), None)
            if match:
                passage_text.insert(tk.END, "ID: ", "red")
                passage_text.insert(tk.END, f"{match['id']}\n", "red")
                passage_text.insert(tk.END, "Title: ", "green")
                passage_text.insert(tk.END, f"{match['title']}\n", "green")
                passage_text.insert(tk.END, f"Passage: {match['passage']}\n{'-'*50}\n")
    else:
        passage_text.insert(tk.END, "Không có khớp nào tìm thấy.")
    passage_text.config(state=tk.DISABLED)

    references = row["references"]
    create_id_entries(len(references), row["chunk_ids"])
    update_progress()


def save_id(event=None):
    global current_index
    ids = id_entries[0].get()
    ids_list = [int(id.strip()) for id in ids.split(",")]
    question_type = type_select.get()
    df.at[current_index, "chunk_ids"] = ids_list
    df.at[current_index, "type_question"] = question_type
    if current_index < len(df) - 1:
        next_question()
    else:
        messagebox.showinfo("Hoàn thành", "Bạn đã gán ID cho tất cả các câu hỏi.")
    with open(qaset_file, "w", encoding="utf-8") as f:
        json.dump(df.to_dict("records"), f, ensure_ascii=False, indent=4)


def previous_question():
    global current_index
    if current_index > 0:
        current_index -= 1
        display_current_question()
    else:
        messagebox.showwarning("Cảnh báo", "Đây là câu hỏi đầu tiên.")


root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=0)
root.grid_rowconfigure(3, weight=0)
root.grid_columnconfigure(0, weight=1)

question_frame = tk.LabelFrame(root, text="Câu hỏi và câu trả lời", padx=10, pady=10)
question_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
question_frame.grid_rowconfigure(0, weight=1)
question_frame.grid_columnconfigure(0, weight=1)

question_text = scrolledtext.ScrolledText(question_frame, wrap=tk.WORD, font=font_content)
question_text.grid(row=0, column=0, sticky="nsew")
question_text.tag_config("red", foreground="red")
question_text.tag_config("green", foreground="green")
question_text.tag_config("blue", foreground="blue")
question_text.config(state=tk.DISABLED)

passage_frame = tk.LabelFrame(root, text="Các khớp có thể", padx=10, pady=10)
passage_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
passage_frame.grid_rowconfigure(0, weight=1)
passage_frame.grid_columnconfigure(0, weight=1)

passage_text = scrolledtext.ScrolledText(passage_frame, wrap=tk.WORD, font=font_content)
passage_text.grid(row=0, column=0, sticky="nsew")
passage_text.tag_config("red", foreground="red")
passage_text.tag_config("green", foreground="green")
passage_text.config(state=tk.DISABLED)

id_progress_frame = tk.Frame(root)
id_progress_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
# id_progress_frame.grid_columnconfigure(1, weight=1)

id_entries_frame = tk.Frame(id_progress_frame)
id_entries_frame.grid(row=0, column=0, columnspan=3, sticky="ew")
# id_entries_frame.grid_columnconfigure(1, weight=1)


type_label = tk.Label(id_progress_frame, text="Loại câu hỏi:", font=font_content)
type_label.grid(row=1, column=0, padx=5, pady=5)
# type_entry = tk.Entry(id_progress_frame, font=font_content)
# type_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
# type_entry.bind("<Return>", save_id)
type_choices = ["query", "verify", "reasoning"]
type_select = ttk.Combobox(id_progress_frame, values=type_choices, font=font_content)
type_select.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

progress_label = tk.Label(id_progress_frame, text="", font=font_content)
progress_label.grid(row=1, column=2, padx=10, pady=5)
update_progress()

button_frame = tk.Frame(root)
button_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

save_button = tk.Button(button_frame, text="Lưu ID và loại câu hỏi", command=save_id, font=font_content)
save_button.pack(side=tk.LEFT, padx=5)
back_button = tk.Button(button_frame, text="<- Quay lại câu hỏi trước", command=previous_question, font=font_content)
back_button.pack(side=tk.LEFT, padx=5)
next_button = tk.Button(button_frame, text="Qua câu tiếp theo ->", command=next_question, font=font_content)
next_button.pack(side=tk.LEFT, padx=5)

# next_question()
display_current_question()

root.mainloop()
