import os

file_path = "./questions_all/lc_al/数论.txt"
if not os.path.exists(file_path):
	print(f"the file path {file_path} not exist!")
	exit()
with open(file_path, "r", encoding="utf-8") as f:
	lines = f.readlines()
lines = [line.strip("\n") for line in lines if len(line.strip("\n"))>2]
lines = [line+"#\n" for line in lines]
content = "".join(lines)

with open(file_path, "w", encoding="utf-8") as f:
	f.write(content)