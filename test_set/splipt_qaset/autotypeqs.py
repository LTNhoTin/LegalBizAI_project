import pandas as pd

def classify_question_type(question):
    question = question.lower()
    if any(word in question for word in ['có phải', 'có không', 'không']):
        return 'verify'
    elif any(word in question for word in ['như thế nào', 'là gì', 'bao gồm', 'cách', 'khi nào']):
        return 'query'
    else:
        return 'reasoning'

# Đọc file qaset1.json vào DataFrame
df = pd.read_json('test_set/splipt_qaset/qaset1.json')

# Áp dụng hàm phân loại câu hỏi và thêm cột 'type_question'
df['type_question'] = df['question'].apply(classify_question_type)

# Lưu DataFrame vào file qaset1.json
df.to_json('test_set/splipt_qaset/qaset1.json', orient='records', lines=True)
