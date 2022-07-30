import os
# which file you want to change
deal_file = "¶þ·Ö²éÕÒ"
dir = r"./questions_all"
files_ls = os.listdir(dir)
files_ls = [file for file in files_ls if file.endswith(".txt")]
# 
for file in files_ls:
	if deal_file not in file:
		continue
	file_path = os.path.join(dir, file)
	with open(file_path, "r", encoding="gbk") as f:
		lines = f.readlines()
		new_lines = list()
		for line in lines:
			if len(line.strip()) <= 0:
				continue
			line = line[:-1] + "#\n"
			new_lines.append(line)
	# write
	w_content = "".join(new_lines)
	print(w_content)
	with open(file_path, "w", encoding="gbk") as f:
		f.write(w_content)
		
