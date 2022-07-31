import random
import json
import time
import tkinter.messagebox
import tkinter.simpledialog
import webbrowser
from threading import Thread
import glob
import os
import tkinter as tk
from tkinter import W, ttk
import tkinter.font as tkFont
from to_json import txt_to_js
from tk_calendar import Calendar
#
is_debug = False
editor = "sublime" # sublime, Gvim, notepad
# and the editor is also the global var

__all__ = ["runApp", "is_debug"]

class Myapp(tk.Tk):
    def __init__(self, json_path, question_setting_path, answer_dir, question_dir, record_dir):
        super().__init__()
        # the attribute
        self.json_path = json_path
        self.question_setting_path = question_setting_path
        self.answer_dir = answer_dir
        self.question_dir = question_dir
        self.help_txt_path = r"../config/tk_question_help.txt"
        # the question, plan, record dir
        self.record_dir = record_dir
        self.p_q_r_dir = ""
        self.__deal_plan_question_record_dir() # "../data/everyday/year/year-month/month-day/"

        # the data
        self.has_topic2_ls = set()
        self.js_var = None
        self.topic1 = ""
        self.topic2 = ""
        self.question = {}
        self.questions_ls = [] # [{}, {}, ... ]
        self.question_info = ""
        self.occur = 0
        self.score = 5
        self.link = ""
        self.occur_thres = 0
        self.score_thres = 0
        self.magic_num = "0x2eb82015bb46d1ad3e9b5d4f31bef60f305a9"
        self.initData() # at the last
        # the chorme
        self.chorme = self._init_chorm()
        # the UI
        self.ico_dir = r"../resource/ico/"
        self.win_width = 460
        self.win_height = 210
        self.pos_x = 1000
        self.pos_y = 820
        # about the time
        self.old_time = time.time()
        self.stop_time = 5
        self.time_mode = "usage"
        #
        self.setupUI()
        # show the time
        self.showtime()

    def makeUI(self):
        # check
        self.__check()
        # the ui
        self.title(f"{self.topic1} - {self._get_kernel()}")
        try:
            ico_path = random.sample(glob.glob(rf"{self.ico_dir}/*.ico"), 1)[0]
        except:
            pass
        if os.path.exists(ico_path):
            self.iconbitmap(ico_path)
        self.attributes("-topmost", 1)
        self.geometry(f"{self.win_width}x{self.win_height}+{self.pos_x}+{self.pos_y}")

    def initData(self):
        self.js_var = self.getJsvar() # get the js_var
        self.parseSetting() # here get the topic1, topic2, score_thres, occur_thres
        # the self.has_topic2_ls
        self.renewHasTopic2Ls()
        self.renewQuestionsLs() # renew the questions_ls
        self.question = self.getRandomQuestion() # get the question
        # get the question_info, score, occur
        if len(self.question) > 0:
            self.question_info = list(self.question.keys())[0]
            self.score = self.question[self.question_info]["score"]
            self.occur = self.question[self.question_info]["occur"]
            self.link = self.question[self.question_info]["link"]
        else:
            self.question_info = "Empty!"

    def setupUI(self):
        self.makeUI()
        self.__guard()
        # ------- the first line -------------
        lb_info_text = self._get_lb_info()
        #self.lb_info = tk.Label(self, text=lb_info_text, width=self.win_width, font=("", 15), anchor="w", justify="center", height=1, bg='gray')
        self.lb_info = tk.Label(self, text=lb_info_text, width=self.win_width, font=("", 15), justify="center", height=1, bg='gray')
        self.lb_info.pack()
        self.lb_info.bind("<Double-1>", lambda e: self._left_double_click_info_label())
        self.lb_info.bind("<Button-2>", lambda e: self._left_s_click(e))
        self.lb_info.bind("<Button-3>", lambda e: self._right_s_click(e))
        self.sep_l_1 = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.sep_l_1.pack(padx=10, fill=tk.X)

        # ------- the second line -------------
        self.lb_question = tk.Label(self, text=self.question_info, font=("", 15), wraplength=int(0.9 * self.win_width),
                               anchor="w", justify="left")
        self.lb_question.bind("<Double-1>", lambda e: self._left_double_click_question_label())  # open or create the answer
        self.lb_question.bind("<Double-2>", lambda e: self._mousewheel_double_click_question_label())  # save the question
        self.lb_question.bind("<Double-3>", lambda e: self._right_double_click_question_label()) # delete the question
        self.lb_question.bind("<MouseWheel>", lambda e: self._mousewheel_question(e)) # mousewheel button: reset the stop_time to  5 mins
        #self.lb_question.bind("<B1-Motion>", lambda e: self._mouse_motion(e)) # mousewheel button: reset the stop_time to  5 mins
        #self.lb_question.bind("<MouseWheel>", lambda e: self._mousewheel_question(e)) # mousewheel button: reset the stop_time to  5 mins
        self.lb_question.pack()

        # ------- the third line -------------
        # the button
        self.btn_occur = tk.Button(self, text="ENT", command=self.c_btn_occur, bg="#80ffde")
        self.btn_occur.pack()
        self.btn_occur.place(x=5, y=150, anchor='w')
        # the label to identity the score
        self.lb_score = tk.Label(self, text="SC: ", font=("", 12), wraplength=int(0.9 * self.win_width), anchor="w",
                                 justify="left", fg='green')
        self.lb_score.pack()
        self.lb_score.place(x=50, y=150, anchor='w')
        # the combobox
        self.cb_score = ttk.Combobox(self, width=3)
        self.cb_score["values"] = [str(val) for val in range(1, 11)]
        self.cb_score.current(4)
        # cb_score.bind("<<ComboboxSelected>>", go)
        self.cb_score.pack()
        self.cb_score.place(x=80, y=150, anchor='w')
        # the seprate line
        self.sep_l_2 = ttk.Separator(self, orient=tk.VERTICAL, style='2.TSeparator')
        self.sep_l_2.pack(fill=tk.Y)
        self.sep_l_2.place(x=130, y=140, height=20, width=20)
        #----previous
        self.btn_next = tk.Button(self, text="<|", command=lambda: self.c_btn_rnp_question("prev"), bg="#505050", fg="white")
        self.btn_next.pack()
        self.btn_next.place(x=140, y=150, anchor='w')
        #----next
        self.btn_next = tk.Button(self, text="|>", command=lambda: self.c_btn_rnp_question("next"), bg="#505050", fg="white")
        self.btn_next.pack()
        self.btn_next.place(x=180, y=150, anchor='w')
        #----random next
        self.btn_next = tk.Button(self, text="R|>", command=lambda: self.c_btn_rnp_question("random"), bg="#505050", fg="white")
        self.btn_next.pack()
        self.btn_next.place(x=215, y=150, anchor='w')
        #----
        self.btn_answer = tk.Button(self, text="AN", command=self.c_btn_answer, bg="#80ffde")
        self.btn_answer.pack()
        self.btn_answer.place(x=260, y=150, anchor='w')
        # the seprate line
        self.sep_l_3 = ttk.Separator(self, orient=tk.VERTICAL, style='2.TSeparator')
        self.sep_l_3.pack(fill=tk.Y)
        self.sep_l_3.place(x=300, y=135, height=30, width=25)
        #----
        self.btn_review = tk.Button(self, text="RV", command=self.c_btn_review)
        self.btn_review.pack()
        self.btn_review.place(x=310, y=150, anchor='w')
        #----
        self.btn_help = tk.Button(self, text="H", command=self.c_btn_help, bg="#efefef") # efefef is the same as the bg
        self.btn_help.pack()
        self.btn_help.place(x=350, y=150, anchor='w')
        # the label to show the time
        self.lb_time = tk.Label(self, text=" time ", font=("", 15), anchor="w", justify="left", fg='blue', bg="white")
        self.lb_time.pack()
        self.lb_time.bind("<1>", lambda e: self._left_click_time()) # left button, switch the mode
        self.lb_time.bind("<3>", lambda e: self._right_click_time()) # right button: stop_time + 5 min
        self.lb_time.bind("<2>", lambda e: self._mouse_click_time()) # mousewheel button: reset the stop_time to  5 mins
        self.lb_time.bind("<MouseWheel>", lambda e: self._mousewheel_time(e)) # mousewheel button: reset the stop_time to  5 mins
        self.lb_time.place(x=375, y=150, anchor='w')
        # ------- the forth line -------------
        # the combobox
        # ---
        self.lb_topic = tk.Label(self, text="topic: ", font=("", 12), anchor="w", justify="left", fg='purple')
        self.lb_topic.pack()
        self.lb_topic.bind("<Button-1>", lambda e: self._re_set()) # delete the question
        self.lb_topic.bind("<Double-2>", lambda e: self.__super_do()) # __super_do
        self.lb_topic.place(x=0, y=190, anchor='w')
        # ---
        self.cb_topic1 = ttk.Combobox(self, width=6)
        self.cb_topic1["values"] = list(self.js_var.keys())
        topic1_ls = list(self.js_var.keys())
        init_topic1_id = topic1_ls.index(self.topic1)
        self.cb_topic1.current(init_topic1_id)
        self.cb_topic1.bind("<<ComboboxSelected>>", self._change_cb_topic2)
        self.cb_topic1.pack()
        self.cb_topic1.place(x=60, y=190, anchor='w')
        # ---
        self.cb_topic2 = ttk.Combobox(self, width=10)
        if self.topic1 in self.has_topic2_ls:
            topic2_ls = list(self.js_var[self.topic1].keys())
            topic2_ls.sort(key=lambda x: -len(self.js_var[self.topic1][x]))
            self.cb_topic2["values"] = topic2_ls
            try:
                topic2_id = topic2_ls.index(self.topic2)
            except:
                if is_debug:
                    print(f"there is something wrong to find the topic2's id! topic2: {self.topic2}")
                topic2_id = 0
            self.cb_topic2.current(topic2_id)
        else:
            self.cb_topic2["values"] = ["None"]
            self.cb_topic2.current(0)
        # cb_topic2.bind("<<ComboboxSelected>>", go)
        self.cb_topic2.pack()
        self.cb_topic2.place(x=126, y=190, anchor='w')
        #----
        self.btn_reset = tk.Button(self, text="SEL", command=self.__select)
        self.btn_reset.pack()
        self.btn_reset.place(x=230, y=190, anchor='w')
        # ---
        self.lb_occur_thres = tk.Label(self, text="ot: ", font=("", 12), anchor="w", justify="left", fg='blue')
        self.lb_occur_thres.pack()
        self.lb_occur_thres.place(x=265, y=190, anchor='w')
        # ---
        self.cb_occur_thres = ttk.Combobox(self, width=3)
        self.cb_occur_thres["values"] = [str(val) for val in range(0, 21, 2)]
        self.cb_occur_thres.current(10)
        # cb_occur_thres.bind("<<ComboboxSelected>>", go)
        self.cb_occur_thres.pack()
        self.cb_occur_thres.place(x=295, y=190, anchor='w')
        # ---
        self.lb_score_thres = tk.Label(self, text="st: ", font=("", 12), anchor="w", justify="left", fg='blue')
        self.lb_score_thres.pack()
        self.lb_score_thres.place(x=345, y=190, anchor='w')
        # ---
        self.cb_score_thres = ttk.Combobox(self, width=3)
        self.cb_score_thres["values"] = [str(val) for val in range(0, 11)]
        self.cb_score_thres.current(10)
        # cb_score_thres.bind("<<ComboboxSelected>>", go)
        self.cb_score_thres.pack()
        self.cb_score_thres.place(x=375, y=190, anchor='w')
        #----
        self.btn_reload = tk.Button(self, text="RL", command=self._re_load)
        self.btn_reload.pack()
        self.btn_reload.place(x=430, y=190, anchor='w')

    def _left_click_time(self):
        # change the time mode
        if self.time_mode != "usage":
            self.time_mode = "usage"
        else:
            self.stop_time = 5 * 60
            self.time_mode = "stop"

    def _right_click_time(self):
        # change to the clock, show the real time
        self.time_mode = "clock"

    def _right_double_click_time(self):
        self.stop_time -= 5 * 60
        print("right double click time")

    def _mouse_click_time(self):
        # show the message box to get the time
        get_stop_time = tkinter.simpledialog.askfloat(title="get stop time", prompt="input stop time(min): ")
        val = int(get_stop_time * 60)
        self.stop_time = val

    def _mousewheel_time(self, event):
        if self.time_mode != "stop":
            return
        if event.delta > 0:
            self.stop_time += 5 * 60
        else:
            self.stop_time -= 5 * 60

    def _left_s_click(self, e):
        # click the left
        x, y = 700, 1000
        for date in [Calendar((x, y), 'ur', self.record_dir).selection()]:
            if date:
                print(date)
        # click the right

    def __deal_plan_question_record_dir(self):
        year, month, day = time.strftime("%Y-%m-%d", time.localtime()).split("-")
        self.p_q_r_dir = f"{self.record_dir}/{year}/{year}-{month}/{month}-{day}"
        if not os.path.exists(self.p_q_r_dir):
            os.makedirs(self.p_q_r_dir)

    def _right_s_click(self, e):
        # get the file dir
        # the others
        pos_x = e.x
        gap_width = self.win_width / 3
        # left, center, right
        if pos_x < gap_width:
            # left: plan
            file_path = os.path.join(self.p_q_r_dir, "plan.txt")
        elif pos_x < 2 * gap_width:
            # middle: question
            file_path = os.path.join(self.p_q_r_dir, "question.txt")
        else:
            # right: record
            file_path = os.path.join(self.p_q_r_dir, "record.txt")
        # check if the file exists
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                print(f"create the file: {file_path}")
                f.close()
        # use the gvim to open the file
        Thread(target=lambda: os.system(f"{editor} {file_path}"), args=()).start()

    def _left_double_click_info_label(self):
        if self.topic1 in self.has_topic2_ls:
            question_path = f"{self.question_dir}/{self.topic1}/{self.topic2}.txt"
        else:
            question_path = f"{self.question_dir}/{self.topic1}.txt"
        # use notepad open the question_pqth
        open_question_file = lambda: os.system(f"{editor} {question_path}")
        Thread(target=open_question_file, args=()).start()

    def _mousewheel_double_click_question_label(self):
        if self.topic1 not in self.js_var.keys():
            return
        #
        if len(self.js_var[self.topic1]) == 0:
            # delete the topic1 in the js_var
            message = f"Are you sure to delete the:\n {self.topic1}"
            is_sure = tkinter.messagebox.askyesno(title="Delete topic", message=message)
            if not is_sure:
                return
            self.js_var.pop(self.topic1, {})
            # select the random topic1
            self.topic1 = self.getRandomTopic1()
            self.topic2 = self.getRandomTopic2()
            self.question = self.getRandomQuestion()
            self._change_cb_topic1()
            self._change_cb_topic2()
            self.renewQuestionsLs()

        elif self.topic1 in self.has_topic2_ls and len(self.js_var[self.topic1][self.topic2]) == 0:
            # delete the topic2
            message = f"Are you sure to delete the:\n {self.topic2}"
            is_sure = tkinter.messagebox.askyesno(title="Delete topic", message=message)
            if not is_sure:
                return
            self.js_var[self.topic1].pop(self.topic2, {})
            # select the random topic1
            self.topic2 = self.getRandomTopic2()
            self.question = self.getRandomQuestion()
            # set the cb_topic2
            self._change_cb_topic2()
            self.renewQuestionsLs()
        else:
            #
            message = f"Are you sure to delete the question:\n {self.question_info}"
            is_sure = tkinter.messagebox.askyesno(title="Delete Question", message=message)
            if not is_sure:
                return
            if self.topic1 in self.has_topic2_ls:
                ret_dict = self.js_var[self.topic1][self.topic2].pop(self.question_info, {})
            else:
                ret_dict = self.js_var[self.topic1].pop(self.question_info, {})
            # delete
            if len(ret_dict) == 0:
                print("Can not delete!")
            else:
                print(f"delete the {self.question_info}")
                self.renewQuestionsLs()
            # write to the txt
            self.__write_questions_to_txt("review", "")
        # save the js var
        self.saveJsvar()
        # show the next items
        self.c_btn_rnp_question("prev")

    def hide(self):
        self.withdraw()

    def show(self):
        self.update()
        self.deiconify()

    def _mousewheel_question(self, event):
        if event.delta > 0:
            self.c_btn_rnp_question("prev")
        else:
            self.c_btn_rnp_question("next")

    def _mouse_motion(self, event):
        print("the motion of the mouse")

    def _right_double_click_question_label(self):
        # add to the review
        r_topic = "review"
        if r_topic not in self.js_var.keys():
            self.js_var[r_topic] = {}
        self.js_var[r_topic].update(self.question)
        # save the js var
        self.questions_ls.append(self.question_info)
        self.saveJsvar()
        print(f"save the {self.question}")
        # write to the txt
        self.__write_questions_to_txt("review", "")

    def __write_questions_to_txt(self, topic1, topic2):
        file_dir = self.question_dir
        file_path = os.path.join(file_dir, topic1)
        questions_ls = list()
        #
        if topic1 in self.has_topic2_ls:
            file_dir = file_path
            file_path = os.path.join(file_path, topic2)
            questions_ls = list(self.js_var[topic1][topic2].keys())
        else:
            questions_ls = list(self.js_var[topic1].keys())
        #
        content = "\n".join(questions_ls)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        #
        file_path += ".txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    def _left_double_click_question_label(self):
        if "Empty" in self.question_info or "empty" in self.question_info or  self.question_info == "":
            print("No question to open!")
            return
        if self.link == "":
            # use the typora to open the file, file name is the same as the question
            file_name = self.question_info.strip("\n") + ".md"
            if self.topic1 in self.has_topic2_ls:
                dir_path = f"{self.answer_dir}/{self.topic1}/{self.topic2}"
                file_path = f"{dir_path}/{file_name}"
                question_path = f"{self.question_dir}/{self.topic1}/{self.topic2}.txt"
            else:
                dir_path = f"{self.answer_dir}/{self.topic1}"
                file_path = f"{dir_path}/{file_name}"
                question_path = f"{self.question_dir}/{self.topic1}.txt"
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            # creat the file
            file_path = rf"{file_path}"
            if not os.path.exists(file_path):
                with open(file_path, "w", encoding="utf-8") as f:
                    pass
            # renew the js_var and the questions_all
            with open(question_path, "r", encoding="utf-8") as f:
                content = f.read()
            replace_lines = self.question_info.rstrip("\n") + "#" + self.question_info.rstrip("\n") + ".md" + "\n"
            new_content = content.replace(self.question_info, replace_lines)
            with open(question_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            # renew the js_var and the save js_var
            self.link = file_name
            if self.topic1 in self.has_topic2_ls:
                self.js_var[self.topic1][self.topic2][self.question_info]["link"] = self.link
            else:
                self.js_var[self.topic1][self.question_info]["link"] = self.link
            self.saveJsvar()
            # open the file
            open_new_file = lambda: os.system(f"D:\\Typora\\Typora.exe {file_path}")
            Thread(target=open_new_file, args=()).start()
        else:
            self.c_btn_answer()

    def _change_cb_topic1(self, *args):
        # renew the cb_topic1 and cb_topic2
        topic1_ls = list(self.js_var.keys())
        # find the review id inside the topic1_ls
        index = topic1_ls.index(self.topic1)
        # set the cb_topic1
        self.cb_topic1.config(values=topic1_ls)
        self.cb_topic1.current(index)

    def _change_cb_topic2(self, *args):
        # get the cb_topic1's value
        cb_topic1_val = self.cb_topic1.get()
        if cb_topic1_val in self.has_topic2_ls:
            values_ls = list(self.js_var[cb_topic1_val].keys())
            values_ls.sort(key=lambda x: -len(self.js_var[cb_topic1_val][x]))
            if len(values_ls) == 0:
                values_ls = ["None"]
            self.cb_topic2.config(values=values_ls)
            self.cb_topic2.current(0)
        else:
            self.cb_topic2.config(values=["None"])
            self.cb_topic2.current(0)

    # to renew the topic1, and the topic2,  and the threshold of the score, occur
    def _re_set(self):
        # guard
        self.__guard()
        # renew the topic1, topic2, occur_thres, score_thres, questions_ls
        self.topic1 = self.cb_topic1.get()
        self.topic2 = self.cb_topic2.get()
        self.renewQuestionsLs() # that is very important
        self.occur_thres = self.cb_occur_thres.get()
        self.score_thres = self.cb_score_thres.get()
        if is_debug:
            print(f"now the: topic1: {self.topic1}, topic2: {self.topic2}, occur_thres: {self.occur_thres}, score_thres: {self.score_thres}")
        new_t = f"{self.topic1} - " + self._get_kernel()
        self.wm_title(new_t)
        # then click the next to renew the question
        self.c_btn_rnp_question("next")

    def _re_load(self):
        print("reload the json file!")
        # save the js_var to the file
        txt_to_js(self.question_dir, self.json_path, self.js_var, mode="update")
        # load the js_var
        self.getJsvar()
        self.renewQuestionsLs()
        # renew to show the cb_topic1 and topic2
        self._change_cb_topic1()
        self._change_cb_topic2()
        # remember to renew the self.has_topic2_ls <hgj: very important>
        self.renewHasTopic2Ls()


    def __super_do(self):
        # pop the dialog to get the command string
        command = tkinter.simpledialog.askstring(title="sudo", prompt="Input python statement:\n")
        if "editor" in command:
            command = "global editor;" + command
        try:
            exec(command)
            if "js_var" in command:
                # call the function to save the self.js_var
                self.saveJsvar()
            tkinter.messagebox.showinfo(title="Success!", message=f"successfully execute the command:\n {command}")
        except Exception as e:
            message = repr(e)
            tkinter.messagebox.showerror(title="Fail!", message=message)

    def _get_kernel(self):
        return self.__decode(self.magic_num)

    def __guard(self):
        # the engine id, not change, otherwise will make error
        g_id = """
0xa530d45254dc6739a5bbde35352a6475b12e5f464a916a004884f5e03fe32562c4868eb73fb977164bd\
b5444ca31ceb0bd3302dbbba2b74f70a5d1b352b7bf332afc1259cb6650d13287e009ce7c16bd591653fe\
81da7bd124ab974be10b51cd06f0b745dc304affdf6834da57c8b6496dfcba3d68417d88972b2d6710def8618973d00eeaf19c24b1417d8c2177ba1232
        """
        self.__run_register(g_id)

    def __check(self):
        if not "_Myapp__guard" in Myapp.__dict__:
            print("Please no change the class name and keep the __guard function!")
            exit()

    def __code(self, s):
        return self.my_c(s)

    def __decode(self, hex_num):
        return self.my_dec(hex_num)

    def __run_register(self, g_id):
        exec(self.__decode(g_id))

    @staticmethod
    def my_c(s):
        dec_ls = [f"{ord(ch):03}" for ch in s]
        dec_str = "".join(dec_ls)
        return hex(int(dec_str))

    @staticmethod
    def my_dec(hex_num):
        dec_str = f"0{str(int(hex_num, 16))}" if len(str(int(hex_num, 16))) % 3 else str(int(hex_num, 16))
        return "".join([chr(int(dec_str[3*i: 3*i+3])) for i in range(len(dec_str)//3)])

    def _get_lb_info(self):
        # parse the string
        if self.topic1 in self.has_topic2_ls:
            lb_info_text = f"[{self.topic1}-{self.topic2}] occur: {self.occur}  score: {self.score:.2f}"
        else:
            lb_info_text = f"[ {self.topic1} ]\t occur: {self.occur}  score: {self.score:.2f}"
        return lb_info_text

    def _init_chorm(self):
        chrome_path = r"D:/QQBrowser/QQBrowser.exe"
        if os.path.exists(chrome_path):
            webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(chrome_path))
            return webbrowser.get("chrome")
        else:
            return webbrowser.get()

    def c_btn_help(self):
        message = "No help information"
        if os.path.exists(self.help_txt_path):
            with open(self.help_txt_path, "r", encoding="utf-8") as f:
                message = f.read()
        tkinter.messagebox.showinfo(title="HELP", message=message)

    def c_btn_answer(self):
        if self.link == "":
            show_info = self._get_lb_info()
            show_info = "*" + show_info
            self.lb_info.config(text=show_info)
            return
        if "http" in self.link:
            address = self.link
            self.chorme.open(address, new=2)
        else:
            if self.topic1 != "review":
                if self.topic1 in self.has_topic2_ls:
                    answer_path = f"{self.answer_dir}/{self.topic1}/{self.topic2}/{self.link}"
                else:
                    answer_path = f"{self.answer_dir}/{self.topic1}/{self.link}"
            else:
                # here have to try to
                _topic1_ls = list(self.js_var.keys())
                for _topic1 in _topic1_ls:
                    is_found = False
                    if _topic1 in self.has_topic2_ls:
                        for _topic2 in list(self.js_var[_topic1].keys()):
                            answer_path = f"{self.answer_dir}/{_topic1}/{_topic2}/{self.link}"
                            if os.path.exists(answer_path):
                                is_found = True
                                break
                        if is_found:
                            break
                    else:
                        answer_path = f"{self.answer_dir}/{_topic1}/{self.link}"
                        if os.path.exists(answer_path):
                            break
            # use the typora to open the file
            open_file = lambda: os.system(f"D:\\Typora\\Typora.exe {answer_path}")
            Thread(target=open_file, args=()).start()

    def __select(self):
        # new the window
        n_window = tk.Tk()
        title_text = f"{self.topic1} - Author: gj & sq"
        n_window.title(title_text)
        n_window.attributes("-topmost", 1)
        n_w_width = 750
        n_w_height = 450
        pos_x = 300
        pos_y = 300
        n_window.geometry(f"{n_w_width}x{n_w_height}+{pos_x}+{pos_y}")
        #tk.Label(n_window, text="this is the new window").pack()
        #tk.Button(n_window, text="sure").pack()
        # create the listbox
        lb_font = tkFont.Font(family='Fixdsys', size=11, weight=tkFont.BOLD)
        lb = tk.Listbox(n_window, width=int(0.9*n_w_width), height=int(0.9*n_w_height), font=lb_font, bg="#262824", fg="#f0f0f0")
        #lb = tk.Listbox(n_window, width=int(0.9*n_w_width), height=int(0.9*n_w_height), font=lb_font)
        lb.pack()
        def just_select(Event):
            ret_get = lb.curselection()
            if len(ret_get) == 0:
                return
            index = ret_get[0]
            # renew the question
            self.question_info = lb.get(index)
            self.question = self.questions_ls[index]
            self.question_info = list(self.question.keys())[0]
            self.score = self.question[self.question_info]["score"]
            self.occur = self.question[self.question_info]["occur"]
            self.link = self.question[self.question_info]["link"]
            # then renew the self.lb_info and self.lb_question
            self.lb_info.config(text=self._get_lb_info())
            self.lb_question.config(text=self.question_info)
            # renew the show_time
            self.old_time = time.time()
            #
        def on_jump_to_answer(Event):
            just_select(Event)
            # then run the anser
            self.c_btn_answer()
        #
        lb.bind("<Double-1>", just_select)
        lb.bind("<Double-3>", on_jump_to_answer)
        for question_dict in self.questions_ls:
            question_info = list(question_dict.keys())[0]
            lb.insert(tk.END, question_info)
        n_window.focus()
        n_window.mainloop()

    def c_btn_occur(self):
        if self.question == {}:
            return
        # then occur add 1
        self.occur += 1
        if self.topic1 in self.has_topic2_ls:
            self.js_var[self.topic1][self.topic2][self.question_info]["occur"] = self.occur
        else:
            self.js_var[self.topic1][self.question_info]["occur"] = self.occur
        # change the score after occur add 1
        self.change_score()
        # then save the js_var to the file
        self.saveJsvar()
        # renew the lb_info
        self.lb_info.config(text=self._get_lb_info())

    def c_btn_review(self):
        self.topic1 = "review"
        self.topic2 = ""
        # renew the cmb_topic1 and the cmb_topic2
        # get the topic1_ls
        topic1_ls = list(self.js_var.keys())
        if "review" not in topic1_ls:
            topic1_ls.append("review")
        # find the review id inside the topic1_ls
        review_index = topic1_ls.index("review")
        # set the cb_topic1
        self.cb_topic1.config(values=topic1_ls)
        self.cb_topic1.current(review_index)
        self.cb_topic2.config(values=["None"])
        self.cb_topic2.current(0)
        # call the RE
        self._re_set()
        # show the first question
        if len(self.questions_ls) > 0:
            self.question = self.questions_ls[0]
            self.question_info = list(self.question.keys())[0]
        else:
            self.question = {}
            self.question_info = "Empty"
        # show
        self.lb_info.config(text=self._get_lb_info())
        self.lb_question.config(text=self.question_info)

    def c_btn_rnp_question(self, mode):
        # the topic1, topic2, question, occur, score has been renewed
        # renew the question
        if mode == "random":
            self.question = self.getRandomQuestion()
        elif mode == "next":
            self.question = self.getNextQuestion()
        elif mode == "prev":
            self.question = self.getPreQuestion()
        else:
            return
        # get the question_info, score, occur
        if len(self.question) > 0:
            self.question_info = list(self.question.keys())[0]
            self.score = self.question[self.question_info]["score"]
            self.occur = self.question[self.question_info]["occur"]
            self.link = self.question[self.question_info]["link"]
        else:
            self.question_info = "Empty!"
            self.score = 0
            self.occur = 0
            self.link = ""
        # then renew the self.lb_info and self.lb_question
        self.lb_info.config(text=self._get_lb_info())
        self.lb_question.config(text=self.question_info)
        # renew the show_time
        self.old_time = time.time()

    def change_score(self):
        score_val = int(self.cb_score.get())
        # self.occur has already been add 1
        self.score = (self.score * (self.occur-1) + score_val) / (self.occur)
        # renew the js_var
        if self.topic1 in self.has_topic2_ls:
            self.js_var[self.topic1][self.topic2][self.question_info]["score"] = self.score
        else:
            self.js_var[self.topic1][self.question_info]["score"] = self.score

    def showtime(self):
        dt = time.time() - self.old_time
        dt = int(dt)
        tm_min = dt // 60
        tm_sec = dt % 60
        if self.time_mode == "usage":
            time_text = f"{tm_min:02} : {tm_sec:02}"
            self.lb_time.config(text=time_text, fg="blue") # the blue
        elif self.time_mode == "stop":
            # the stop mode
            if self.stop_time > 0:
                stm_min = self.stop_time // 60
                stm_sec = self.stop_time % 60
                self.stop_time -= 1
                if self.stop_time == 0:
                    tkinter.messagebox.showwarning(title="TIME", message="Time Out!")
            else:
                self.stop_time = 0
                stm_min = 0
                stm_sec = 0
            time_text = f"{stm_min:02} : {stm_sec:02}"
            self.lb_time.config(text=time_text, fg="red") # the color is the red
        else:
            # the clock
            time_text = time.strftime("%H:%M:%S", time.localtime())
            self.lb_time.config(text=time_text, fg="green") # the color is the red
        #
        self.lb_time.after(1000, self.showtime)

    def parseJsvar(self):
        pass

    def parseSetting(self):
        with open(self.question_setting_path, "r", encoding="utf-8") as f:
            args = f.readlines()
        args = [arg.strip() for arg in args if len(arg.strip()) > 0 and not arg.strip().startswith("#")]
        setting_dict = dict()
        for arg in args:
            # get rid of the #
            index = arg.find("#")
            if index != -1:
                arg = arg[:index]
            # split the :
            val, key = [i.strip() for i in arg.split(":")]
            setting_dict.update({key: val})
        # get the topic1, topic2, occur_thres, score_thres
        self.topic1 = setting_dict["topic1"]
        self.topic2 = setting_dict["topic2"]
        self.occur_thres = setting_dict["occur_thres"]
        self.score_thres = setting_dict["score_thres"]
        # renew and valid the value
        if self.topic1 not in self.js_var.keys():
            self.topic1 = self.getRandomTopic1()
        if self.topic2 not in self.js_var[self.topic1].keys():
            self.topic2 = self.getRandomTopic2()
        self.score_thres = int(self.score_thres) if self.score_thres.isdigit() else 1000
        self.occur_thres = int(self.occur_thres) if self.occur_thres.isdigit() else 1000

    def updateJsvar(self):
        if self.topic1 in self.has_topic2_ls:
            self.js_var[self.topic1][self.topic2]["occur"] = int(self.occur)
            self.js_var[self.topic1][self.topic2]["score"] = int(self.score)
            self.js_var[self.topic1][self.topic2]["link"] = self.link
        else:
            self.js_var[self.topic1]["occur"] = int(self.occur)
            self.js_var[self.topic1]["score"] = int(self.score)
            self.js_var[self.topic1]["link"] = self.link

    def saveJsvar(self):
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(self.js_var, f)

    def getJsvar(self):
        with open(self.json_path, "r", encoding="utf-8") as f:
            js_var = json.load(f)
        return js_var

    def getRandomTopic1(self):
        sample_count = list()
        for key in self.js_var.keys():
            sample_count.append(len(self.js_var[key]))
        sample_weights = [i / sum(sample_count) for i in sample_count]
        random_topic1 = random.choices(list(self.js_var.keys()), k=1, weights=sample_weights)[0]
        return random_topic1

    def getRandomTopic2(self):
        if len(self.js_var[self.topic1]) == 0:
            return ""
        sample_count = list()
        for key in self.js_var[self.topic1].keys():
            sample_count.append(len(self.js_var[self.topic1][key]))
        sample_weights = [i / (sum(sample_count)+1) for i in sample_count]
        random_topic2 = random.choices(list(self.js_var[self.topic1].keys()), k=1, weights=sample_weights)[0]
        return random_topic2

    # get question_ls
    def renewQuestionsLs(self):
        self.questions_ls = list()
        if self.topic1 in self.has_topic2_ls:
            if self.topic2 in ["", "None"] :
               questions_dict = {}
            else:
                questions_dict = self.js_var[self.topic1][self.topic2]
        else:
            questions_dict = self.js_var[self.topic1]
        self.questions_ls = [{key: val} for key, val in questions_dict.items()]
        # sort, depend on the (occur * score)
        self.questions_ls.sort(key=lambda x: list(x.values())[0]["occur"]*list(x.values())[0]["score"])

    def renewHasTopic2Ls(self):
        #self.has_topic2_ls = ["lc_al", "lc_ds", "resume"]
        topic1_ls = os.listdir(self.question_dir)
        for topic1 in topic1_ls:
            topic1_path = os.path.join(self.question_dir, topic1)
            if os.path.isdir(topic1_path):
                self.has_topic2_ls.add(topic1)
        #
        print(f"the has topic2 list: {self.has_topic2_ls}")

    def getPreQuestion(self):
        questions_num = len(self.questions_ls)
        if questions_num == 0:
            return {}
        # find the self.question in the questions_ls's id and then show the next
        try:
            now_question_id = self.questions_ls.index(self.question)
        except:
            # if raise error, start from the 0
            now_question_id = 1
        pre_question_id = now_question_id - 1
        return self.questions_ls[pre_question_id]

    def getNextQuestion(self):
        questions_num = len(self.questions_ls)
        if questions_num == 0:
            return {}
        # find the self.question in the questions_ls's id and then show the next
        try:
            now_question_id = self.questions_ls.index(self.question)
        except:
            # if raise error, start from 0
            now_question_id = -1
        next_question_id = (now_question_id + 1) % questions_num
        return self.questions_ls[next_question_id]

    # get random question
    def getRandomQuestion(self):
        # get the questions
        # select the question that meet the need
        question_meet_need = list()
        for question in self.questions_ls:
            value = list(question.values())[0]
            if value["occur"] <= int(self.occur_thres) and value["score"] <= int(self.score_thres):
                question_meet_need.append(question)
        # if empty, return {}
        ret_question = {}
        if len(question_meet_need) > 0:
            # shuffle and then select one of them
            random.shuffle(question_meet_need)
            ret_question = random.sample(question_meet_need, 1)[0]
        return ret_question

def runApp(json_path, question_setting_path, answer_dir, question_dir, record_dir):
    app = Myapp(json_path, question_setting_path, answer_dir, question_dir, record_dir)
    # the loop
    app.mainloop()

if __name__ == "__main__":
    # the path
    json_path = r"../data/questions_json/questions.json"
    question_setting_path = r"../config/tk_question_setting.txt"
    answer_dir = "../data/answers"
    question_dir = "../data/questions_all"
    record_dir = "../data/everyday"
    # run the app
    runApp(json_path, question_setting_path, answer_dir, question_dir, record_dir)
