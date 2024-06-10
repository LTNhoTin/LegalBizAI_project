import pandas as pd

file_path = r"test_set/id_cof/qaset.json"

# Đọc dữ liệu từ tệp JSON
data = pd.read_json(file_path)

def classify_question_type(question):
    question = question.lower()
    if any(word in question for word in [
        'như thế nào', 'là gì', 'bao gồm', 'cách', 'khi nào', 'ở đâu', 'ai', 'tại sao', 'thế nào', 'như nào', 'cần gì', 
        'phải làm sao', 'có được', 'không nên', 'trong trường hợp nào', 'gồm những gì', 'trong các trường hợp nào', 
        'hoạt động nào', 'trường hợp nào', 'bao lâu', 'nghĩa vụ nào', 'hoạt động nào', 'gồm những gì', 'mục tiêu nào', 
        'hoạt động gì', 'giấy tờ gì', 'điều kiện nào', 'vào đâu', 'bao nhiêu ngày', 'cơ quan nào', 'bao lâu', 'làm gì', 
        'ngày nào', 'đối tượng nào', 'gì?', 'bao nhiêu', 'các trường hợp', 'ra sao', 'nào?', 'gì?', 'luật?', 'nào', 'nào?', 
        'gì', 'mấy', 'theo quy định', 'quyền và nghĩa vụ', 'quy trình thực hiện', 'đâu?', 'tại đâu?', 'đối tượng?', 'diện?', 
        'cho từng', 'thời hạn', 'doanh nghiệp?', 'khi', 'quy định của pháp luật', 'đối với', 'mấy', 'khái niệm', 'thời điểm', 
        'cơ cấu tổ chức', 'không được', 'quyền và nghĩa vụ', 'thời hiệu', 'trường hợp'
    ]):
        return 'query'
    elif any(word in question for word in ['có phải', 'có không', 'đúng không', 'được không', 'có thể', 'đúng', 'sai', 'nên','không?','có tiếp','hay','có được','nhất thiết']):
        return 'verify'
    else:
        return 'reasoning'

# Áp dụng hàm phân loại loại câu hỏi
data['type_question'] = data['question'].apply(classify_question_type)

# Ghi đè lên tệp JSON ban đầu
data.to_json(file_path, orient='records', force_ascii=False, indent=4)

print("Cập nhật thành công!")
print(data.head())
