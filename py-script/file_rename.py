import os
import re
from glob import glob

def file_rename(files_dir=None):
    if files_dir == None:
        files_dir = "../data/answers/PLang/c++/"
    files_path_ls = glob(files_dir + "/*.md")
    pattern = re.compile(r"[0-9]{1,}_")
    for i, file_path in enumerate(files_path_ls):
        ret = re.search(pattern, file_path)
        print(file_path, "\t"*2, end="")
        ret = re.sub(pattern, str(i)+".", file_path)
        os.rename(file_path, ret)

def generate_question_txt(files_dir, save_file_path):
    file_names = os.listdir(files_dir)
    file_names = [file_name for file_name in file_names if file_name.endswith(".md")]
    # sort the file_names by the order
    file_names.sort(key=lambda x: int(x.split(".")[0]))
    # add the file_names to the content
    item_ls = list()
    for file_name in file_names:
        part_1 = file_name[:-3]
        item_ls.append(part_1 + "#" + file_name)
    # commbine to the string
    content = "\n".join(item_ls)
    content.rsplit() # ripe of the \n
    print(content)
    # save to the file path
    with open(save_file_path, "w", encoding="utf-8") as f:
        f.write(content)

files_dir = "../data/answers/PLang/c++/"
save_file_path = "../data/questions_all/PLang/c++.txt"
generate_question_txt(files_dir, save_file_path)
generate_question_txt()