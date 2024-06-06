import json

# Load the original file
with open('/Users/nhotin/Documents/GitHub/LegalBizAI_project/test_set/cleaning/qaset.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Calculate the number of items per file
num_items = len(data)
items_per_file = num_items // 4

# Create the smaller JSON files
for i in range(4):
    start_index = i * items_per_file
    if i == 3: 
        end_index = num_items
    else:
        end_index = (i + 1) * items_per_file
    
    subset = data[start_index:end_index]
    output_filename = f'/Users/nhotin/Documents/GitHub/LegalBizAI_project/test_set/splipt_qaset/qaset{i + 1}.json'
    
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        json.dump(subset, output_file, ensure_ascii=False, indent=4)

print("Files have been split and saved as qaset1.json, qaset2.json, qaset3.json, and qaset4.json.")
