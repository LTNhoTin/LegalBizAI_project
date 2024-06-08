import pandas as pd

# Load the JSON file
file_path = "test_set/splipt_qaset/qaset1.json"
data = pd.read_json(file_path)

# Define the classification function
def classify_question_type(question):
    question = question.lower()
    if any(word in question for word in ['có phải', 'có không', 'không', 'đúng không', 'được không', 'có thể']):
        return 'verify'
    elif any(word in question for word in ['như thế nào', 'là gì', 'bao gồm', 'cách', 'khi nào', 'ở đâu', 'ai', 'tại sao']):
        return 'query'
    else:
        return 'reasoning'

# Apply the classification function to the dataset
data['type_question'] = data['question'].apply(classify_question_type)

# Save the updated dataframe to a new JSON file
output_path = "test_set/combine_qaset/qaset1.json"
data.to_json(output_path, orient='records', force_ascii=False, indent=4)

# Display the first few rows of the dataframe
print(data.head())
