import os

def save(fname, content, folder_path):
    """Lưu nội dung vào file trong thư mục."""
    file_path = os.path.join(folder_path, fname + ".txt")
    with open(file_path, "w", encoding="utf-8") as savef:
        savef.write(content)

def extract_chapters_and_rules(content):
    """Hàm xử lý và chia cột dữ liệu thành chương và điều."""
    chapters = []
    current_chapter = None

    lines = content.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("Chương"):
            current_chapter = line
        elif line.startswith("Điều"):
            rule_number = line
            context = ""
            i += 1
            while i < len(lines):
                next_line = lines[i].strip()
                if next_line.startswith("Điều") or next_line.startswith("Chương"):
                    i -= 1
                    break
                context += next_line + " "
                i += 1
            chapters.append({"Chapter": current_chapter, "Article": rule_number, "Context": context.strip()})
        i += 1
    return chapters

def split_and_save(base_path, file_number, start_no):
    """Chia file theo chương và điều, lưu vào thư mục tương ứng."""
    file_name = f"{file_number}.txt"
    folder_name = f"split_folder{file_number}"
    folder_path = os.path.join(base_path, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    try:
        with open(os.path.join(base_path, file_name), "r", encoding="utf-8") as file:
            content = file.read()

        data = extract_chapters_and_rules(content)

        if not data:
            print(f"Không tìm thấy chương hoặc điều nào trong file: {file_name}")
            return

        no_chapter_folder = os.path.join(folder_path, "No_Chapter")
        os.makedirs(no_chapter_folder, exist_ok=True)

        for item in data:
            if item["Chapter"]:
                chapter_folder = os.path.join(folder_path, item["Chapter"].replace(" ", "_"))
                os.makedirs(chapter_folder, exist_ok=True)
                folder_to_save = chapter_folder
            else:
                folder_to_save = no_chapter_folder

            article_name = f"Dieu_{start_no}"
            save(article_name, f'{item["Article"]}\n{item["Context"]}', folder_to_save)
            start_no += 1

    except FileNotFoundError:
        print(f"Không tìm thấy file: {file_name}")

# Đường dẫn đến thư mục chứa các file
base_path = "/Users/nhotin/Documents/Python_work/datatrans/vanbanhuongdan/Final_guilddoc"

# Xử lý từ file 1.txt đến 8.txt
for file_number in range(1, 9):
    path = os.path.join(base_path, f"split_folder{file_number}")
    if os.path.exists(path):
        start_no = int(input(f"Nhập số điều luật bắt đầu cho file {file_number}.txt: "))
    else:
        start_no = 1
    split_and_save(base_path, file_number, start_no)
