import pandas as pd
import re
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext, ttk

csv_file_path = '/Users/nhotin/Documents/GitHub/LegalBizAI_project/test_set/id_cof/qaset.csv'
df = pd.read_csv(csv_file_path)

json_file_path = '/Users/nhotin/Documents/GitHub/LegalBizAI_project/test_set/id_cof/all_chunk.json'
data = pd.read_json(json_file_path)

# Khởi tạo cột 'id' với kiểu dữ liệu Int64 nếu chưa tồn tại
if 'id' not in df.columns:
    df['id'] = pd.Series(dtype='Int64')

# Hàm khớp tham chiếu với tiêu đề từ JSON
def match_references(reference, data):
    matches = data[data['title'].str.contains(reference, na=False)]
    return matches

root = tk.Tk()
root.title("Gán ID cho câu hỏi")
root.geometry("1000x800")

# Tìm ô đầu tiên của câu hỏi chưa có ID
def find_first_empty_id(df):
    empty_id_index = df[df['id'].isna()].index
    if not empty_id_index.empty:
        return empty_id_index[0]
    return len(df) 

current_index = find_first_empty_id(df)

def update_progress():
    progress['value'] = (current_index / len(df)) * 100
    root.update_idletasks()

def next_question():
    global current_index
    if current_index >= len(df):
        messagebox.showinfo("Hoàn thành", "Bạn đã gán ID cho tất cả các câu hỏi.")
        return

    row = df.iloc[current_index]
    matches = match_references(row['references'], data)

    if matches.empty:
        messagebox.showwarning("Cảnh báo", "Không có khớp nào tìm thấy cho tham chiếu này.")

    question_text.config(state=tk.NORMAL)
    question_text.delete(1.0, tk.END)
    question_text.insert(tk.END, "Question: ", "red")
    question_text.insert(tk.END, f"{row['question']}\n\n")
    question_text.insert(tk.END, "Answer: ", "green")
    question_text.insert(tk.END, f"{row['answer']}\n\n")
    question_text.insert(tk.END, "Reference: ", "green")
    question_text.insert(tk.END, f"{row['references']}\n\n")
    question_text.config(state=tk.DISABLED)

    passage_text.config(state=tk.NORMAL)
    passage_text.delete(1.0, tk.END)
    if not matches.empty:
        for i, match in matches.iterrows():
            passage_text.insert(tk.END, "ID: ", "red")
            passage_text.insert(tk.END, f"{match['id']}\n", "red")
            passage_text.insert(tk.END, "Title: ", "green")
            passage_text.insert(tk.END, f"{match['title']}\n", "green")
            passage_text.insert(tk.END, f"Passage: {match['passage']}\n{'-'*50}\n")
    else:
        passage_text.insert(tk.END, "Không có khớp nào tìm thấy.")
    passage_text.config(state=tk.DISABLED)
    update_progress()

def save_id(event=None):
    global current_index
    correct_id = id_entry.get()
    try:
        # Kiểm tra nếu ID là số nguyên
        correct_id_int = int(correct_id)
        df.at[current_index, 'id'] = correct_id_int
        current_index += 1
        id_entry.delete(0, tk.END)
        df.to_csv(csv_file_path, index=False)  # Lưu trực tiếp vào tệp CSV
        next_question()
    except ValueError:
        messagebox.showerror("Lỗi nhập ID", "ID phải là một số nguyên.")

def previous_question():
    global current_index
    if current_index > 0:
        current_index -= 1
        df.at[current_index, 'id'] = pd.NA
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
id_label = tk.Label(id_progress_frame, text="Nhập ID chính xác:", font=("Helvetica", 16))
id_label.pack(side=tk.LEFT)
id_entry = tk.Entry(id_progress_frame, font=("Helvetica", 16))
id_entry.pack(side=tk.LEFT, padx=5)
id_entry.bind("<Return>", save_id)  
progress = ttk.Progressbar(id_progress_frame, orient="horizontal", length=300, mode="determinate")
progress.pack(side=tk.LEFT, padx=10)
update_progress()

# Nút để lưu ID và chuyển sang câu hỏi tiếp theo và nút quay lại câu hỏi trước
button_frame = tk.Frame(root)
button_frame.pack(pady=10)
save_button = tk.Button(button_frame, text="Lưu ID và chuyển câu hỏi", command=save_id, font=("Helvetica", 14))
save_button.pack(side=tk.LEFT, padx=5)
back_button = tk.Button(button_frame, text="Quay lại câu hỏi trước", command=previous_question, font=("Helvetica", 14))
back_button.pack(side=tk.LEFT, padx=5)

next_question()
root.mainloop()
