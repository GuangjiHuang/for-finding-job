import json
import os
import glob
import copy

# the classification
"ml: "
"dl: "
"img: "
"lc: "
"c++&python: "
"resume: "

def fileToDict(file_path, topic1, topic2, o_js_var):
    questions_with_count = dict()
    with open(file_path, "r", encoding="utf-8") as f:
        questions = f.readlines()
        questions = [question.strip() for question in questions if len(question.strip()) > 0 and not question.strip().startswith("#")]
        if len(questions) == 0:
            # renew the o_js_var
            if topic2 == "":
                o_js_var[topic1] = {}
            else:
                if topic1 in o_js_var.keys():
                    o_js_var[topic1][topic2] = {}
                else:
                    o_js_var[topic1] = dict()
                    o_js_var[topic1].update({topic2: {}})
        for question in questions:
            # try to split the question by the #
            question_ls = question.split("#", 1)
            link = ""
            if len(question_ls) == 2:
                link = question_ls[-1].strip()
                question = question_ls[0].strip()
            else:
                question = question.strip()
            # renew the questions_with_count
            tmp_dict = {question: {"occur": 0, "score": 0, "link": link}}
            questions_with_count.update(tmp_dict)
            # just renew the link for the old_js_var
            if topic1 in o_js_var.keys():
                if topic2 == "":
                    if question in o_js_var[topic1].keys():
                        o_js_var[topic1][question]["link"] = link
                    else:
                        o_js_var[topic1].update(tmp_dict)
                else:
                    if not topic2 in o_js_var[topic1].keys():
                        o_js_var[topic1][topic2] = dict()
                    if question in o_js_var[topic1][topic2].keys():
                        o_js_var[topic1][topic2][question]["link"] = link
                    else:
                        o_js_var[topic1][topic2].update(tmp_dict)
            else:
                o_js_var[topic1] = dict()
                if topic2 == "":
                    o_js_var[topic1].update(tmp_dict)
                else:
                    o_js_var[topic1][topic2] = dict()
                    o_js_var[topic1][topic2].update(tmp_dict)
    return questions_with_count

# get the questions from the file
def txt_to_js(dir_path, js_path, o_js_var, mode="cover"):
    js_var = dict()
    if o_js_var == {}:
        mode = "cover"
    files_dirs = os.listdir(dir_path)
    files_dirs.sort()
    files_dirs_path = [os.path.join(dir_path, file_dir) for file_dir in files_dirs]
    # the js_var to store the result
    for i, file_dir_path in enumerate(files_dirs_path):
        if os.path.isdir(file_dir_path):
            js_var[files_dirs[i]] = dict()
            sub_files_dirs = os.listdir(file_dir_path)
            sub_files = [sub_file_dir for sub_file_dir in sub_files_dirs if sub_file_dir.endswith(".txt")]
            for sub_file in sub_files:
                sub_file_path = os.path.join(file_dir_path, sub_file)
                js_var[files_dirs[i]].update({sub_file[:-4]: fileToDict(sub_file_path, files_dirs[i], sub_file[:-4], o_js_var)})
        elif os.path.isfile(file_dir_path) and file_dir_path.endswith(".txt"):
            # {cv: {question1: {count: 0, scores: 0}, question2: {..}}
            js_var[files_dirs[i][:-4]] = fileToDict(file_dir_path, files_dirs[i][:-4], "", o_js_var)
    #
    # save the js_var to the json file
    with open(js_path, "w", encoding="utf-8") as f:
        if mode == "cover":
            json.dump(js_var, f)
        else:
            json.dump(o_js_var, f)
    # return the one of them
    return js_var if mode == "cover" else o_js_var

if __name__ == "__main__":
    # test the function
    txt_dir_path = "../data/questions_all"
    js_path = "../data/questions_json/questions.json"

    try:
        with open(js_path, "r", encoding="utf-8") as f:
            o_js_var = json.loads(f.read())
            print("fail to open the o_js_var!")
    except:
        o_js_var = {}

    #o_js_var = {}
    txt_to_js(txt_dir_path, js_path, o_js_var, mode="new")

    # open and then load the json file
    is_show_js = False
    if is_show_js:
        with open(js_path, "r", encoding="utf-8") as f:
            js_var = json.load(f)
        for key, val in js_var.items():
            print("----------------------------------------")
            print(key, ":")
            print(val)
            print("----------------------------------------")