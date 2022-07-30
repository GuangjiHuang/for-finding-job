# -*- coding: utf-8 -*-
import calendar
import tkinter as tk
import tkinter.font as tkFont
import glob
import os
from threading import Thread
from tkinter import ttk

datetime = calendar.datetime.datetime
timedelta = calendar.datetime.timedelta
editor = "sublime"

class Calendar:

    def __init__(self, point=None, position=None, main_window=None, everyday_dir=None):
        # point    提供一个基点，来确定窗口位置
        # position 窗口在点的位置 'ur'-右上, 'ul'-左上, 'll'-左下, 'lr'-右下
        # self.master = tk.Tk()
        #self.main_window = ShowBoard("./everyday/")
        self.main_window = main_window
        self.__init_list_box__()
        #
        self.everyday_dir = everyday_dir if everyday_dir is not None else r"./everyday/"
        #k
        self.master = tk.Toplevel()
        self.master.withdraw()
        fwday = calendar.SUNDAY

        year = datetime.now().year
        month = datetime.now().month
        locale = None
        sel_bg = '#ecffc4'
        sel_fg = '#05640e'

        self._date = datetime(year, month, 1)
        self._selection = None  # 设置为未选中日期

        self.G_Frame = ttk.Frame(self.master)

        self._cal = self.__get_calendar(locale, fwday)

        self.__setup_styles()  # 创建自定义样式
        self.__place_widgets()  # pack/grid 小部件
        self.__config_calendar()  # 调整日历列和安装标记
        # 配置画布和正确的绑定，以选择日期。
        self.__setup_selection(sel_bg, sel_fg)

        # 存储项ID，用于稍后插入。
        self._items = [self._calendar.insert('', 'end', values='') for _ in range(6)]

        # 在当前空日历中插入日期
        self._update()

        self.G_Frame.pack(expand=1, fill='both')
        self.master.overrideredirect(1)
        self.master.update_idletasks()
        width, height = self.master.winfo_reqwidth(), self.master.winfo_reqheight()
        if point and position:
            if position == 'ur':
                x, y = point[0], point[1] - height
            elif position == 'lr':
                x, y = point[0], point[1]
            elif position == 'ul':
                x, y = point[0] - width, point[1] - height
            elif position == 'll':
                x, y = point[0] - width, point[1]
        else:
            x, y = (self.master.winfo_screenwidth() - width) / 2, (self.master.winfo_screenheight() - height) / 2
        self.master.geometry('%dx%d+%d+%d' % (width, height, x, y))  # 窗口位置居中
        self.master.after(300, self._main_judge)
        self.master.deiconify()
        self.master.focus_set()
        self.master.wait_window()  # 这里应该使用wait_window挂起窗口，如果使用mainloop,可能会导致主程序很多错误

    def __init_list_box__(self):
        # the window to show the information
        self.n_window = tk.Tk()
        title_text = f"Daily Study - Author: gj & sq"
        self.n_window.title(title_text)
        self.n_window.attributes("-topmost", 1)
        self.win_width = 460
        self.win_height = 210
        self.pos_x = 1000
        self.pos_y = 820
        #
        self.n_window.geometry(f"{self.win_width}x{self.win_height}+{self.pos_x}+{self.pos_y}")
        # the label to show the title
        lb_info_text = "date"
        self.lb_info = tk.Label(self.n_window, text=lb_info_text, width=self.win_width, font=("", 15), justify="center", height=1, bg='gray')
        self.lb_info.pack(side=tk.TOP)
        self.lb_info.bind("<Double-1>", lambda e: self.jump_to_all())
        self.lb_info.bind("<Button-3>", lambda e: self.exit_win())
        # the listbox
        lb_font = tkFont.Font(family='Fixdsys', size=11, weight=tkFont.BOLD)
        self.lb = tk.Listbox(self.n_window, width=self.win_width, font=lb_font)
        self.lb.pack()
        self.lb.bind("<Button-3>", lambda e: self.on_jump_to_answer(e))
        # the data
        self.select_dir = ""

    def exit_win(self):
        self.n_window.destroy()

    def count_questions_num(self, file_path):
        if not os.path.exists(file_path):
            return 0
        with open(file_path, "r") as f:
            lines = f.readlines()
        count = 0
        add_flag = False
        for i, line in enumerate(lines):
            line = line.strip(" ")
            if line != "\n":
                add_flag = True
                if i == len(lines) - 1:
                    count += 1
            elif add_flag:
                count += 1
                add_flag = False
        return count

    def jump_to_all(self):
        print("jump to all questions!")
        all_file_dir = os.path.join(self.everyday_dir, "all")
        if not os.path.exists(all_file_dir):
            os.makedirs(all_file_dir)
        #
        files = os.listdir(all_file_dir)
        self.lb.delete(0, tk.END)
        if len(files) == 0:
            self.lb.insert(tk.END, "NONE")
        else:
            files.sort()
            for file in files:
                file_name = file.split(".")[0]
                # add the question num
                questions_num = self.count_questions_num(os.path.join(all_file_dir, file_name+".txt"))
                if questions_num == 0:
                    continue
                item_show = f"{file_name:15}{self._space_(3)}#{self._space_(4)}{questions_num} items"
                self.lb.insert(tk.END, item_show)
                self.lb.insert(tk.END, "")
        # renew the lb_info
        lb_info_text = f"ALL"
        self.lb_info.config(text=lb_info_text)
        # renew the select_dir
        self.select_dir = all_file_dir

    def on_jump_to_answer(self, Event):
        # get the file name that you have selected
        ret_get = self.lb.curselection()
        if len(ret_get) == 0:
            return
        index = ret_get[0]
        # renew the question
        item_show = self.lb.get(index)
        if item_show == "NONE" or item_show.strip(" \n") == "":
            return
        # use the vim to open the result
        file_name = item_show.split("#")[0].strip(" \n")
        file_path = os.path.join(self.select_dir, f"{file_name}.txt")
        Thread(target=lambda: os.system(f"{editor} {file_path}")).start()

    def _space_(self, num):
        return " " * num

    def _renew_list_box(self, year, month, day):
        self.select_dir = f"{self.everyday_dir}/{year}-{month:02d}/{month:02d}-{day:02d}/"
        self.lb.delete(0, tk.END)
        if not os.path.exists(self.select_dir):
            self.lb.insert(tk.END, "NONE")
        else:
            files = os.listdir(self.select_dir)
            files.sort()
            for file in files:
                file_name = file.split(".")[0]
                # add the question num
                questions_num = self.count_questions_num(os.path.join(self.select_dir, file_name+".txt"))
                if questions_num == 0:
                    continue
                item_show = f"{file_name:15}{self._space_(3)}#{self._space_(4)}{questions_num} items"
                self.lb.insert(tk.END, item_show)
                self.lb.insert(tk.END, "")
        # renew the lb_info
        lb_info_text = f"{year}-{month}-{day}"
        self.lb_info.config(text=lb_info_text)

    def _hide_list_box(self):
        self.n_window.withdraw()

    def _show_list_box(self):
        #self.n_window.update()
        self.n_window.deiconify()

    def __get_calendar(self, locale, fwday):
        # 实例化适当的日历类
        if locale is None:
            return calendar.TextCalendar(fwday)
        else:
            return calendar.LocaleTextCalendar(fwday, locale)

    def __setitem__(self, item, value):
        if item in ('year', 'month'):
            raise AttributeError("attribute '%s' is not writeable" % item)
        elif item == 'selectbackground':
            self._canvas['background'] = value
        elif item == 'selectforeground':
            self._canvas.itemconfigure(self._canvas.text, item=value)
        else:
            self.G_Frame.__setitem__(self, item, value)

    def __getitem__(self, item):
        if item in ('year', 'month'):
            return getattr(self._date, item)
        elif item == 'selectbackground':
            return self._canvas['background']
        elif item == 'selectforeground':
            return self._canvas.itemcget(self._canvas.text, 'fill')
        else:
            r = ttk.tclobjs_to_py({item: ttk.Frame.__getitem__(self, item)})
            return r[item]

    def __setup_styles(self):
        # 自定义TTK风格
        style = ttk.Style(self.master)
        arrow_layout = lambda dir: (
            [('Button.focus', {'children': [('Button.%sarrow' % dir, None)]})]
        )
        style.layout('L.TButton', arrow_layout('left'))
        style.layout('R.TButton', arrow_layout('right'))

    def __place_widgets(self):
        # 标头框架及其小部件
        Input_judgment_num = self.master.register(self.Input_judgment)  # 需要将函数包装一下，必要的
        hframe = ttk.Frame(self.G_Frame)
        gframe = ttk.Frame(self.G_Frame)
        bframe = ttk.Frame(self.G_Frame)
        hframe.pack(in_=self.G_Frame, side='top', pady=5, anchor='center')
        gframe.pack(in_=self.G_Frame, fill=tk.X, pady=5)
        bframe.pack(in_=self.G_Frame, side='bottom', pady=5)

        lbtn = ttk.Button(hframe, style='L.TButton', command=self._prev_month)
        lbtn.grid(in_=hframe, column=0, row=0, padx=12)
        rbtn = ttk.Button(hframe, style='R.TButton', command=self._next_month)
        rbtn.grid(in_=hframe, column=5, row=0, padx=12)

        self.CB_year = ttk.Combobox(hframe, width=5, values=[str(year) for year in
                                                          range(datetime.now().year, datetime.now().year - 11, -1)],
                                 validate='key', validatecommand=(Input_judgment_num, '%P'))
        self.CB_year.current(0)
        self.CB_year.grid(in_=hframe, column=1, row=0)
        self.CB_year.bind('<KeyPress>', lambda event: self._update(event, True))
        self.CB_year.bind("<<ComboboxSelected>>", self._update)
        tk.Label(hframe, text='年', justify='left').grid(in_=hframe, column=2, row=0, padx=(0, 5))

        self.CB_month = ttk.Combobox(hframe, width=3, values=['%02d' % month for month in range(1, 13)], state='readonly')
        self.CB_month.current(datetime.now().month - 1)
        self.CB_month.grid(in_=hframe, column=3, row=0)
        self.CB_month.bind("<<ComboboxSelected>>", self._update)
        tk.Label(hframe, text='月', justify='left').grid(in_=hframe, column=4, row=0)

        # 日历部件
        self._calendar = ttk.Treeview(gframe, show='', selectmode='none', height=7)
        self._calendar.pack(expand=1, fill='both', side='bottom', padx=5)

        ttk.Button(bframe, text="确 定", width=6, command=lambda: self._exit(True)).grid(row=0, column=0, sticky='ns',
                                                                                    padx=20)
        ttk.Button(bframe, text="取 消", width=6, command=self._exit).grid(row=0, column=1, sticky='ne', padx=20)

        tk.Frame(self.G_Frame, bg='#565656').place(x=0, y=0, relx=0, rely=0, relwidth=1, relheigh=2 / 200)
        tk.Frame(self.G_Frame, bg='#565656').place(x=0, y=0, relx=0, rely=198 / 200, relwidth=1, relheigh=2 / 200)
        tk.Frame(self.G_Frame, bg='#565656').place(x=0, y=0, relx=0, rely=0, relwidth=2 / 200, relheigh=1)
        tk.Frame(self.G_Frame, bg='#565656').place(x=0, y=0, relx=198 / 200, rely=0, relwidth=2 / 200, relheigh=1)

    def __config_calendar(self):
        # cols = self._cal.formatweekheader(3).split()
        cols = ['日', '一', '二', '三', '四', '五', '六']
        self._calendar['columns'] = cols
        self._calendar.tag_configure('header', background='grey90')
        self._calendar.insert('', 'end', values=cols, tag='header')
        # 调整其列宽
        font = tkFont.Font()
        maxwidth = max(font.measure(col) for col in cols)
        for col in cols:
            self._calendar.column(col, width=maxwidth, minwidth=maxwidth,
                               anchor='center')

    def __setup_selection(self, sel_bg, sel_fg):
        def __canvas_forget(evt):
            canvas.place_forget()
            self._selection = None

        self._font = tkFont.Font()
        self._canvas = canvas = tk.Canvas(self._calendar, background=sel_bg, borderwidth=0, highlightthickness=0)
        canvas.text = canvas.create_text(0, 0, fill=sel_fg, anchor='w')

        canvas.bind('<Button-1>', __canvas_forget)
        self._calendar.bind('<Configure>', __canvas_forget)
        self._calendar.bind('<Button-1>', self._pressed)

    def _is_day_has_files(self, year, month, day):
        file_dir = f"{self.everyday_dir}/{year}-{month:02d}/{month:02d}-{day:02d}"
        file_path_ls = glob.glob(f"{file_dir}/*.txt")
        flag = False
        if len(file_path_ls) == 0:
            return False
        else:
            for file_path in file_path_ls:
                with open(file_path, "r")  as f:
                    if f.read().strip(" \n\t") == "":
                        f.close()
                        # then remove the f
                        os.remove(file_path)
                    else:
                        flag = True
        return flag

    def _build_calendar(self):

        year, month = self._date.year, self._date.month

        # update header text (Month, YEAR)
        header = self._cal.formatmonthname(year, month, 0)

        # 更新日历显示的日期
        cal = self._cal.monthdayscalendar(year, month)
        for indx, item in enumerate(self._items):
            week = cal[indx] if indx < len(cal) else []
            #fmt_week = [('%02d' % day) if day else '' for day in week]
            fmt_week = list()
            for day in week:
                if day:
                    if not self._is_day_has_files(year, month, day):
                        fmt_week.append(f"{day:02d}")
                    else:
                        fmt_week.append(f"+{day:02d}")
                else:
                    fmt_week.append('')
            self._calendar.item(item, values=fmt_week)

    def _show_select(self, text, bbox):
        """为新的选择配置画布。"""
        x, y, width, height = bbox

        textw = self._font.measure(text)

        canvas = self._canvas
        canvas.configure(width=width, height=height)
        canvas.coords(canvas.text, (width - textw) / 2, height / 2 - 1)
        canvas.itemconfigure(canvas.text, text=text)
        canvas.place(in_=self._calendar, x=x, y=y)

    def _pressed(self, evt=None, item=None, column=None, widget=None):
        """在日历的某个地方点击。"""
        if not item:
            x, y, widget = evt.x, evt.y, evt.widget
            item = widget.identify_row(y)
            column = widget.identify_column(x)

        if not column or not item in self._items:
            # 在工作日行中单击或仅在列外单击。
            return

        item_values = widget.item(item)['values']
        if not len(item_values):  # 这个月的行是空的。
            return

        text = item_values[int(column[1]) - 1]
        # <hgj> add
        day = text
        if not text:  # 日期为空
            return

        bbox = widget.bbox(item, column)
        if not bbox:  # 日历尚不可见
            self.master.after(20, lambda: self._pressed(item=item, column=column, widget=widget))
            return
        text = '%02d' % text
        self._selection = (text, item, column)
        self._show_select(text, bbox)
        # get the year, month, day, and then renew the listbox
        print("you are clicking the date, do something now!")
        self._renew_list_box(self._date.year, self._date.month, day)

    def _prev_month(self):
        """更新日历以显示前一个月。"""
        self._canvas.place_forget()
        self._selection = None

        self._date = self._date - timedelta(days=1)
        self._date = datetime(self._date.year, self._date.month, 1)
        self.CB_year.set(self._date.year)
        self.CB_month.set(self._date.month)
        self._update()

    def _next_month(self):
        """更新日历以显示下一个月。"""
        self._canvas.place_forget()
        self._selection = None

        year, month = self._date.year, self._date.month
        self._date = self._date + timedelta(
            days=calendar.monthrange(year, month)[1] + 1)
        self._date = datetime(self._date.year, self._date.month, 1)
        self.CB_year.set(self._date.year)
        self.CB_month.set(self._date.month)
        self._update()

    def _update(self, event=None, key=None):
        """刷新界面"""
        if key and event.keysym != 'Return': return
        year = int(self.CB_year.get())
        month = int(self.CB_month.get())
        if year == 0 or year > 9999: return
        self._canvas.place_forget()
        self._date = datetime(year, month, 1)
        self._build_calendar()  # 重建日历

        if year == datetime.now().year and month == datetime.now().month:
            day = datetime.now().day
            for _item, day_list in enumerate(self._cal.monthdayscalendar(year, month)):
                if day in day_list:
                    item = 'I00' + str(_item + 2)
                    column = '#' + str(day_list.index(day) + 1)
                    self.master.after(100, lambda: self._pressed(item=item, column=column, widget=self._calendar))

    def _exit(self, confirm=False):
        """退出窗口"""
        if not confirm: self._selection = None
        self.master.destroy()

    def _main_judge(self):
        """判断窗口是否在最顶层"""
        try:
            # self.master 为 TK 窗口
            # if not self.master.focus_displayof(): self._exit()
            # else: self.master.after(10, self._main_judge)

            # self.master 为 toplevel 窗口
            if self.master.focus_displayof() == None or 'toplevel' not in str(self.master.focus_displayof()):
                self._exit()
            else:
                self.master.after(10, self._main_judge)
        except:
            self.master.after(10, self._main_judge)

        # self.master.tk_focusFollowsMouse() # 焦点跟随鼠标

    def selection(self):
        """返回表示当前选定日期的日期时间。"""
        if not self._selection: return None

        year, month = self._date.year, self._date.month
        return str(datetime(year, month, int(self._selection[0])))[:10]

    def Input_judgment(self, content):
        """输入判断"""
        # 如果不加上==""的话，就会发现删不完。总会剩下一个数字
        if content.isdigit() or content == "":
            return True
        else:
            return False


if __name__ == '__main__':
    root = tk.Tk()

    width, height = root.winfo_reqwidth() + 50, 50  # 窗口大小
    x, y = (root.winfo_screenwidth() - width) / 2, (root.winfo_screenheight() - height) / 2
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))  # 窗口位置居中

    date_str = tk.StringVar()
    date = ttk.Entry(root, textvariable=date_str)
    date.place(x=0, y=0, relx=5 / 20, rely=1 / 6, relwidth=14 / 20, relheigh=2 / 3)

    # Calendar((x, y), 'ur').selection() 获取日期，x,y为点坐标
    main_app = None
    date_str_gain = lambda: [
        date_str.set(date)
        for date in [Calendar((x, y), 'ur', main_app).selection()]
        if date]
    tk.Button(root, text='日期:', command=date_str_gain).place(x=0, y=0, relx=1 / 20, rely=1 / 6, relwidth=4 / 20,
                                                             relheigh=2 / 3)
    root.mainloop()
