import os
import shutil
import glob

dir_ls = ["cv", "img", "ml", "PLang", "others"]

save_dir = "./questions_all_try"
if os.path.exists(save_dir):
	shutil.rmtree(save_dir)
os.mkdir(save_dir)

for dir_name in dir_ls:
	files_ls = os.listdir(dir_name)
	files_ls = [file for file in files_ls if file.endswith(".md")]
	lines = list()
	for i, file in enumerate(files_ls):
		# deal with the file_name
		file_name = file[:-3]
		file_name = file_name.replace("_", ".", 1)
		line = file_name + "#" + file
		lines.append(line)
	content = "\n".join(lines)
	file_path = os.path.join(save_dir, dir_name+".txt")
	with open(file_path, "w", encoding="utf-8") as f:
		f.write(content)


