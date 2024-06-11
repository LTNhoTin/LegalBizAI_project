import pandas as pd

file_path = r"test_set/id_cof/chunk_sz_full_article/qaset_full_article.json"
data = pd.read_json(file_path)

def classify_question_type(question):
    question = question.lower()
    if any(word in question for word in ['trường hợp', 'khi']):
        return 'reasoning'
    elif any(word in question for word in [
    'như thế nào', 'là gì', 'bao gồm', 'cách', 'khi nào', 'ở đâu', 'ai', 'tại sao', 'thế nào', 'như nào', 'cần gì', 
    'phải làm sao', 'có được', 'không nên', 'gồm những gì', 
    'hoạt động nào', 'trường hợp nào', 'bao lâu', 'nghĩa vụ nào', 'hoạt động nào', 'gồm những gì', 'mục tiêu nào', 
    'hoạt động gì', 'giấy tờ gì', 'điều kiện nào', 'vào đâu', 'bao nhiêu ngày', 'cơ quan nào', 'bao lâu', 'làm gì', 
    'ngày nào', 'đối tượng nào', 'gì?', 'bao nhiêu', 'các trường hợp', 'ra sao', 'nào?', 'gì?', 'luật?', 'nào?', 
    'gì', 'mấy', 'theo quy định', 'quyền và nghĩa vụ', 'quy trình thực hiện', 'đâu?', 'tại đâu?', 'đối tượng?', 'diện?', 
    'thời hạn', 'doanh nghiệp?', 'quy định của pháp luật', 'đối với', 'mấy', 'khái niệm', 'thời điểm', 
    'cơ cấu tổ chức', 'không được', 'quyền và nghĩa vụ',
    ]):
        return 'query'
    else: # any(word in question for word in ['có phải', 'có không', 'đúng không', 'được không', 'có thể', 'đúng', 'sai', 'nên','không?','có tiếp','hay','có được','nhất thiết']):
        return 'verify'
    

data['type_question'] = data['question'].apply(classify_question_type)

output_path = file_path
data.to_json(output_path, orient='records', force_ascii=False, indent=4)

print(data.head())
