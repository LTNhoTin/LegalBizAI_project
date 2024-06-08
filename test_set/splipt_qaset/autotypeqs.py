import pandas as pd

file_path = r"test_set/splipt_qaset/qaset2.json"
data = pd.read_json(file_path)

def classify_question_type(question):
    question = question.lower()
    if any(word in question for word in ['có phải', 'có không', 'đúng không', 'được không', 'có thể', 'đúng', 'sai', 'nên']):
        return 'verify'
    elif any(word in question for word in ['như thế nào', 'là gì', 'bao gồm', 'cách', 'khi nào', 'ở đâu', 'ai', 'tại sao', 'thế nào', 'như nào', 'cần gì', 'phải làm sao','có được','không nên','trong trường hợp nào','gồm những gì','trong các trường hợp nào','hoạt động nào','trường hợp nào','bao lâu','nghĩa vụ nào','hoạt động nào','gồm những gì','mục tiêu nào','hoạt động gì','giấy tờ gì','điều kiện nào','vào đâu','bao nhiêu ngày','cơ quan nào','bao lâu']):
        return 'query'
    else:
        return 'reasoning'

data['type_question'] = data['question'].apply(classify_question_type)

output_path = r"D:\khổ dâm data\bạo dâm data\qaset1.json"
data.to_json(output_path, orient='records', force_ascii=False, indent=4)

print(data.head())
