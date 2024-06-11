def split_file_into_parts(input_file, output_files):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Tính toán số dòng cho mỗi phần
    total_lines = len(lines)
    lines_per_part = total_lines // 4

    # Chia tệp thành 4 phần
    for i in range(4):
        start_index = i * lines_per_part
        # Đảm bảo phần cuối cùng lấy hết các dòng còn lại
        if i == 3:
            end_index = total_lines
        else:
            end_index = (i + 1) * lines_per_part

        part_lines = lines[start_index:end_index]
        with open(output_files[i], 'w', encoding='utf-8') as part_file:
            part_file.writelines(part_lines)

input_file = 'data_processing/data4llm/example.txt'
output_files = ['part1.txt', 'part2.txt', 'part3.txt', 'part4.txt']
split_file_into_parts(input_file, output_files)
