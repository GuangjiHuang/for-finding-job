import os

main_dir = "./"
sub_dirs = os.listdir(main_dir)
save_path = "./file_names.txt"
sub_dirs = [sub_dir for sub_dir in sub_dirs if os.path.isdir(sub_dir)]
#
content = str()
for sub_dir in sub_dirs:
    files_ls = os.listdir(sub_dir)
    files_ls = [file for file in files_ls if file.endswith(".md")]
    content += f"\n# {sub_dir}\n"
    content += "\n".join(files_ls)
print(content)
# write the content to the file
with open(save_path, "w") as f:
    f.write(content)
