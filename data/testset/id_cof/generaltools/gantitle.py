import json

# Load the data from the downloaded file
file_path = 'test_set/id_cof/all_chunk_final.json'
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Function to check and add title to passage if it does not start with "Điều"
def ensure_title_in_passage(data):
    updated_data = []
    for entry in data:
        if not entry['passage'].startswith("Điều"):
            entry['passage'] = f"{entry['title']}\n{entry['passage']}"
        updated_data.append(entry)
    return updated_data

# Ensure all passages have the title if they do not start with "Điều"
updated_data = ensure_title_in_passage(data)

# Save the updated data to a new file
updated_file_path = 'corrected_all_chunk_final.json'
with open(updated_file_path, 'w', encoding='utf-8') as updated_file:
    json.dump(updated_data, updated_file, ensure_ascii=False, indent=2)

print("File has been updated and saved as corrected_all_chunk_final.json")
