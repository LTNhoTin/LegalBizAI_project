import json

# Define the chunk ranges
chunk_range = {
    "Luật doanh nghiệp 2020": [0, 433],
    "01_2021_NĐ-CP": [434, 683],
    "16_2023_NĐ-CP": [684, 716],
    "23_2022_NĐ-CP": [717, 813],
    "47_2021_NĐ-CP": [814, 865],
    "122_2021_NĐ-CP": [866, 1001],
    "153_2020_NĐ-CP": [1002, 1114]
}

# Load the JSON data from the file
file_path = '/Users/nhotin/Documents/GitHub/LegalBizAI_project/test_set/cleaning/qaset.json'
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Correct the problematic line
problematic_line_index = 14422  # Index of the problematic line (adjust as needed)
lines[problematic_line_index] = '    },\n'

# Reassemble the JSON content
corrected_json_content = ''.join(lines)

# Parse the corrected JSON content
data = json.loads(corrected_json_content)

# Update each entry with the corresponding chunk_id
for entry in data:
    for reference in entry["references"]:
        if reference[1] in chunk_range:
            entry["chunk_id"] = chunk_range[reference[1]]

# Save the updated data to a new JSON file
updated_file_path = 'corrected.json'
with open(updated_file_path, 'w', encoding='utf-8') as updated_file:
    json.dump(data, updated_file, ensure_ascii=False, indent=4)

print(f'Updated file saved to: {updated_file_path}')
