import pandas as pd

file_path = "test_set/splipt_qaset/qaset1.json"
data = pd.read_json(file_path)

def classify_question_type(question):
    question = question.lower()
    if any(word in question for word in ['có phải', 'có không', 'không', 'đúng không', 'được không', 'có thể', 'đúng', 'sai', 'nên', 'không nên']):
        return 'verify'
    elif any(word in question for word in ['như thế nào', 'là gì', 'bao gồm', 'cách', 'khi nào', 'ở đâu', 'ai', 'tại sao', 'thế nào', 'như nào', 'cần gì', 'phải làm sao', 'trường hợp nào']):
        return 'query'
    else:
        return 'reasoning'

data['type_question'] = data['question'].apply(classify_question_type)

output_path = "test_set/combine_qaset/qaset1.json"
data.to_json(output_path, orient='records', force_ascii=False, indent=4)

print(data.head())
