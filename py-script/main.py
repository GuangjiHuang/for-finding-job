import re
import math
import time
import os
import cv2 as cv
import copy
import numpy as np
from threading import Thread
import random
from tk_question import *

#
color_tb = {"red":(0, 0, 255), "green": (0, 255, 0), "blue": (255, 0, 0), 
		"yellow": (0, 255, 255), "purple": (255, 0, 255), "black": (0, 0, 0), "white": (255, 255, 255)}
#

def progress(img_h, img_w, p_h, t_toal, t_left):
	img = 66 * np.ones((img_h, img_w, 3), np.uint8)
	# the progress width and the height
	if p_h > img_h:
		p_h = img_h
	# solve the problem that if the t_toal is the 0
	if t_toal <=0 :
		t_toal = 1
		t_left = 1
	p_w_r = math.floor(t_left / t_toal * img_w)
	p_w_l = img_w - p_w_r
	# set the value
	h1 = (img_h - p_h) // 2
	h2 = (img_h + p_h) // 2
	h1 = 0 if h1 < 0 else h1
	h2 = img_h if h2>img_h else h2
	img[h1:h2, 0:p_w_l, 1] = 255
	img[h1:h2, p_w_l:, 2] = 255
	return img

def space(num):
	return " " * num

def newline(num):
	return "\n" * num

def get_video_path(save_dir):
	# check the save_dir
	if not os.path.exists(save_dir):
		os.makedirs(save_dir)
		print(f"make the directory: {save_dir}")
	now_time = time.strftime("%Y-%m-%d %H-%M")
	save_path = f"{save_dir}{now_time}.mp4"
	return save_path
# 
def check_plan_file(record_dir, file_name_ls):
	global everyday_dir
	# get the date
	t_tm = time.localtime()
	year, month, day = t_tm.tm_year, t_tm.tm_mon, t_tm.tm_mday
	abbre_weekday = time.strftime("%a", t_tm)
	#
	everyday_dir = f"{record_dir}/{year}/{year}-{month:02}/{month:02}-{day:02}"
	if not os.path.exists(everyday_dir):
		os.makedirs(everyday_dir)
	for file_name in file_name_ls:
		# the message
		head = f"==============================\n" +\
			f"{year}-{month}-{day}{space(2)}{abbre_weekday}.{space(5)}{file_name.upper()} \n" +\
			f"=============================="
		file_path = os.path.join(everyday_dir, file_name+".txt")
		if os.path.exists(file_path):
			continue
		with open(file_path, "w", encoding="utf-8") as f:
			f.write(head)
			f.close()

def get_time_idnum(file_path):
	# to get the last time point and the items number
	content = ""
	with open(file_path, "r", encoding="utf-8") as f:
		lines = f.readlines()
	# reverse the lines
	lines.reverse()
	time_pattern = r"- *(\d{2}:\d{2})"
	idnum_pattern = r"^([PQR])(\d{1,3})(\. *)"
	is_find_time = False
	is_find_idnum = False
	time_point = ""
	idnum_str = ""
	for line in lines:
		if is_find_time and is_find_idnum:
			break
		#
		if not is_find_time:
			t_m = re.search(time_pattern, line)
			if t_m:
				time_point = t_m.group(1)
				is_find_time = True
		if not is_find_idnum:
			id_m = re.search(idnum_pattern, line)
			if id_m:
				prefix_topic = id_m.group(1)
				id_num = id_m.group(2)
				idnum_str = f"{prefix_topic}{int(id_num)+1}{id_m.group(3)}"
				is_find_idnum = True
	#
	return time_point, idnum_str

def append_time_to_file(file_path, time_duration_sec, start_time=None):
	# add the now time
	time_duration_min = int(time_duration_sec / 60)
	if start_time is None:
		now_time = time.time()
	else:
		now_time = start_time # need the start_time is the time.time() format return
	now_time_str = time.strftime("%H:%M", time.localtime(now_time))
	next_time = now_time + time_duration_sec
	next_time_str = time.strftime("%H:%M", time.localtime(next_time))
	# get the time_point and the idnum_str
	time_point, idnum_str = get_time_idnum(file_path)
	if time_point != "":
		t1_ls = time_point.split(":")
		t2_ls = now_time_str.split(":")
		free_time_duration = (int(t2_ls[0])-int(t1_ls[0])) * 60 + int(t2_ls[1]) - int(t1_ls[1])
	# add two newline before the string
	if time_point == "":
		# no free time
		if idnum_str == "":
			first_ch = os.path.basename(file_path)[0].upper()
			idnum_str = first_ch + "1. "
		append_content = f"{newline(2)}{now_time_str}-{next_time_str}{space(5)}{time_duration_min:3} mins\n" \
						 f"{idnum_str}"
	else:
		if free_time_duration >= 60:
			free_time_str = f"{newline(2)}{time_point}-{now_time_str}{space(5)}{free_time_duration/60:.2} hours ---------- free ----------\n"
		else:
			free_time_str = f"{newline(2)}{time_point}-{now_time_str}{space(5)}{free_time_duration:2} mins  ---------- free ----------\n"
		append_content = f"{free_time_str}" \
						 f"{now_time_str}-{next_time_str}{space(5)}{time_duration_min:3} mins\n" \
						 f"{idnum_str}"
	with open(file_path, "a+", encoding="utf-8") as f:
		f.write(append_content)
		f.close()

# --------------------------------------------------
# the global var that you have to set
save_dir = r"../../study-app-data/video-save/"
video_num = 0
is_show_random = False
is_live=False
t_gap = 0.05
count_down_color = color_tb["green"]
show_time_color = color_tb["red"]
full_sc_width = 1920
full_sc_height = 1080
count_down_is_in_concentrate_mode = True
is_use_video = True
play_video_path = r"../../study-app-data/beauty/scenery.mp4"
is_load_setting = True
time_check_count = 0
time_check_threshold = 1
file_write_threshold = 5
json_path = r"../data/questions_json/questions.json"
question_setting_path = r"../config/tk_question_setting.txt"
answer_dir = "../data/answers"
question_dir = "../data/questions_all"
record_dir = "../data/everyday"
editor = "sublime" # you can choose the Gvim, sublime, notepad
# if load the setting
setting_path = r"../config/main_setting.txt"
# is_use_duplicate
is_use_duplicate_window = True
is_shine_screen = False
# if open the question and record file
is_open_question_record = False
if is_load_setting:
	with open(setting_path, "r", encoding="utf-8") as f:
		commands = f.readlines()
	print("----- command setting ---------")
	for command in commands:
		command = command.strip()
		if len(command) == 0:
			continue
		try:
			exec(command)
			print(command)
		except:
			print("there are some wrong with the command: {command}")
# today's date and the path
t_tm = time.localtime()
year, month, day = t_tm.tm_year, t_tm.tm_mon, t_tm.tm_mday
everyday_dir = f"{record_dir}/{year}/{year}-{month:02}/{month:02}-{day:02}"
file_name_ls = ["plan", "question", "record"]
# --------------------------------------------------
# test if can open the video and the camera
print("test the camera and the video!")
cap_camera = cv.VideoCapture(video_num)
cap_video = cv.VideoCapture(play_video_path)
is_valid_video = cap_video.isOpened()
is_valid_camera = cap_camera.isOpened()
if not is_valid_video and not is_valid_camera:
	print("Fail to open the video and the camera! Exit!")
	exit()
elif is_valid_camera and not is_valid_video:
	print("camera: ok! video: fail! Choose the camera!")
	is_use_video = False
	video_num = video_num
elif is_valid_video and not is_valid_camera:
	print("camera: fail! video: ok! Choose the video!")
	is_use_video = True
	video_num = play_video_path
else:
	if is_use_video:
		print("camera: ok! video: ok! Choose the video!")
		video_num = play_video_path
	else:
		print("camera: ok! video: ok! Choose the camera!")
cap_camera.release()
cap_video.release()
#
cap  = cv.VideoCapture(video_num)
# deal with the video writer
save_path = get_video_path(save_dir)
width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
if is_use_video and is_valid_video:
	width = 640
	height = 480
print(f"the video's width: {width}, height: {height}")
fourcc = cv.VideoWriter_fourcc(*'mp4v')
fps = 25
#
if not os.path.exists(save_dir):
	os.mkdir(save_dir)
	print("make the directory ./veio_save")
#
is_save = False
is_record = False
is_end = True
# set the window to the top
window_name = "study"
cv.namedWindow(window_name, cv.WINDOW_AUTOSIZE | cv.WINDOW_FREERATIO)
cv.setWindowProperty(window_name, cv.WND_PROP_TOPMOST, 1)
#cv.setWindowProperty(window_name, cv.WND_PROP_FULLSCREEN, cv.WINDOW_NORMAL)
# the change flag
bg_change_flag = True
has_thread = False
while (True):
	# add the time_check_count and then check if you have the plan
	time_check_count += 1
	if time_check_count == time_check_threshold:
		time_check_count = 0
		# then check the plan file
		# check file if exists
		# check if you have make the plan
		check_plan_file(record_dir, file_name_ls)

	if is_live:
		if bg_change_flag:
			print("change to the live!")
			cv.moveWindow(window_name, full_sc_width-30-width, full_sc_height-70-height)
			bg_change_flag = False
		ret, img = cap.read()
		if is_use_video and is_valid_video: # then resize the video size to the 640 x 480
			img = cv.resize(img, (640, 480))
		if (not ret):
			cap.release()
			print("can not read the image!")
			if is_use_video and is_valid_video:
				# open the video again
				video_num = play_video_path
				cap = cv.VideoCapture(video_num)
			else:
				# there is something wrong with the camera
				if is_valid_video:
					video_num = play_video_path
					cap = cv.VideoCapture(video_num)
				exit()
	else:
		if bg_change_flag:
			if is_debug:
				print("change to the time!")
			cv.moveWindow(window_name, int(full_sc_width-30-width*0.6), int(full_sc_height-70-height*0.1))
			bg_change_flag = False
		img = 166 * np.ones((int(height*0.1), int(width * 0.6), 3), np.uint8)
# put the text in the image
	text = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	if is_live:
		cv.putText(img, text, (int(0.4*width), 30), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)
	else:
		cv.putText(img, text, (10, 30), cv.FONT_HERSHEY_COMPLEX, 1, show_time_color, 2)
	if is_record:
		text_rec = "REC"
		img_show = copy.copy(img)
		cv.putText(img_show, text_rec, (30, 30), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
# show the image
	img_show = img_show if is_record else img
	cv.imshow(window_name, img_show)
	key_val_0 = cv.waitKey(25) & 0xff
	# the interview mode
	if key_val_0 in [ord('i'), ord('I')]:
		if key_val_0 == ord('I'):
			# open the question.setting
			if os.path.exists(question_setting_path):
				# use the gvim to open the file
				try:
					ret = os.system(f"gvim {question_setting_path}")
					if ret == 1:
						print("can not use the gvim, so use the notepad instead!")
						os.system(f"notepad {question_setting_path}")
				except:
					pass
		# get the message
		# show the window
		Thread(target=runApp, args=(json_path, question_setting_path, answer_dir, question_dir, record_dir)).start()
		has_thread = True

	if key_val_0 == ord('t'):
		is_live = (not is_live)
		# set the bg_change_flag again
		bg_change_flag = True
	if key_val_0 == ord('x'): # change the video source
		if is_use_video and is_valid_video:
			# change to the camera
			if is_valid_camera:
				is_use_video = False
				cap.release()
				video_num = 0
				cap = cv.VideoCapture(video_num)
				print("video -> camera: ok!")
		else:
			# change to the video
			if is_valid_video:
				is_use_video = True
				cap.release()
				video_num = play_video_path
				cap = cv.VideoCapture(video_num)
				print("camera -> video: ok!")
			else:
				print("camera -> video: fail. Can not open the video!")
	if key_val_0 == ord('s'):
		if not is_end:
			try:
				out.release()
				os.remove(save_path)
			except:
				pass
			is_end = True
		save_path = get_video_path(save_dir)
		out = cv.VideoWriter(save_path, fourcc, 30, (width, height))
		print("save the video now ......")
		is_save = True
		is_record = True
		is_end = False
	elif key_val_0 == ord('p'):
		# renew the questions
		renew_question_command = "python get_json.py"
		c_ret = os.system(renew_question_command)
		if c_ret == 0:
			print(f"run {renew_question_command} successfully!")
		else:
			print(f"fail to run {renew_question_command}")
	elif key_val_0 == ord('q'):
		print("quit the video!")
		if is_save:
			is_record = False
			is_end = True
			out.release()
		cap.release()
		cv.destroyAllWindows()
		# quit the tk windoiw
		exit()
	elif key_val_0 == ord('e'):
		if is_save:
			is_save = False
			is_record = False
			is_end = True
			print("ending save!")
			out.release()
		else:
			print("Not starting to record the video!")
	elif key_val_0 == ord('c'):
		if is_save:
			is_save = False
			is_record = False
			print("cancle!")
			out.release()
			os.remove(save_path)
			is_end = True
#
	elif key_val_0 == ord(':'):
		# record the old_play_video_path
		old_play_video_path = play_video_path
		# setting the parameter
		if os.path.exists(setting_path):
			# use the gvim to open the file
			try:
				ret = os.system(f"gvim {setting_path}")
				if ret == 1:
					print("can not use the gvim, so use the notepad instead!")
					os.system(f"notepad {setting_path}")
			except:
				pass
			with open(setting_path, "r", encoding="utf-8") as f:
				commands = f.readlines()

			print("----- command setting ---------")
			for command in commands:
				command = command.strip()
				if len(command) == 0:
					continue
				try:
					exec(command)
					print(command)
				except:
					print("there are some wrong with the command: {command}")
		# check the new video path
		if not cv.VideoCapture(play_video_path).isOpened():
			play_video_path = old_play_video_path
		else:
			if is_use_video and is_valid_video:
				# change the video
				cap.release()
				cap = cv.VideoCapture(play_video_path)
				print(f"change the video: {old_play_video_path} -> {play_video_path}")
		# the bg_change_flag <hgj : why use the change flag?>
		bg_change_flag = False
#
	elif key_val_0 == ord('n'):
		if not video_num.isdigit():
			print("Now you are using the video source! Not the camera! Quit!")
		new_video_num = (video_num + 1)  %  2
		cap_new = cv.VideoCapture(new_video_num)
		if cap_new.isOpened():
			ret, frame = cap_new.read()
			if not ret:
				while 1:
					print("cap_new can not read the image!")
		cap.release()
		cap = cap_new
		print(f"{video_num} switch the camera {new_video_num}!")
		#cap.release()
		if is_save:
			out.release()
		is_save = False
		is_end = True
		is_record = False
		#if not cap.isOpened():
		#	print("Can not open the video, keep the original video!")
		#	cap.release()
		#	cap = cv.VideoCapture(video_num)
		#else:
		video_num = new_video_num

	elif key_val_0 == ord('h'):
		# this is the help
		# read the help text
		help_path = "../config/main_help.txt"
		help_list = list()
		with open(help_path, "r", encoding="utf-8") as f:
			help_list = f.readlines()
		# make the show image
		help_img = 33 * np.ones((height, width, 3), np.uint8)
		# put the Text in the image
		help_list = [i.strip("\n") for i in help_list if len(i)>0]
		help_text_len = len(help_list)
		height_step = int(width // (help_text_len+5))
		# add the first line to -- help information ---
		help_information = "------ help information (Author: hgj&ysq) ------"
		cv.putText(help_img, help_information, (int(0.1*width), 15), cv.FONT_HERSHEY_COMPLEX, 0.5, color_tb["red"], 1)
		for i, item in enumerate(help_list):
			cv.putText(help_img, item, (20, height_step*(i+1)), cv.FONT_HERSHEY_COMPLEX, 0.5, color_tb["yellow"], 1)
		# show teh image
		cv.moveWindow(window_name, full_sc_width-30-width, full_sc_height-70-height)
		cv.imshow(window_name, help_img)
		cv.waitKey(0)
		# here have to set the bg change flag
		bg_change_flag = True
	elif key_val_0 in [ord(str(i)) for i in range(10)]:
		t_num = key_val_0 - ord('0')
		if t_num == 0:
			t_num = 10
		count_tm = t_num * 60 * t_gap
		count_tm_copy = count_tm
		# if the count_tm gt 10 min, you need to have the plan
		quit_flag = False
		if  count_tm >= 10 * 60:
			# pop the window to ask you to make the plan
			# the pop text
			timer_text = f"{count_tm//60}min."
			plan_text = f"Do you have plan? Yes[a], Think[b], Quit[q]!"
			# make the new window
			cv.namedWindow("Information")
			cv.moveWindow("Information", int(0.5*full_sc_width), int(0.1*full_sc_height))  # move the window to the middle
			infor_width = int(0.3 * full_sc_width)
			infor_height = int(0.2 * full_sc_height)
			information_img = np.zeros((infor_height, infor_width, 3), np.uint8)
			cv.putText(information_img, plan_text, (int(0.1*infor_width), int(0.3*infor_height)), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 255), 1)
			cv.putText(information_img, timer_text, (int(0.1*infor_width), int(0.3*infor_height+30)), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 255), 1)
			# show the image and then give you time to think
			while True:
				cv.imshow("Information", information_img)
				key_val_infor = cv.waitKey(0)
				if key_val_infor == ord('a'):
					break
				elif key_val_infor == ord('b'):
					thinking_time = 20
					cv.putText(information_img, f"thinking {thinking_time}s ...", (int(0.1*infor_width), int(0.4*infor_height+60)), cv.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 255), 1)
					cv.imshow("Information", information_img)
					cv.waitKey(thinking_time * 1000)
					break
				elif key_val_infor == ord('q'):
					quit_flag = True
					break
			# destory the window
			cv.destroyWindow("Information")
		# if you chose the quit, then continue
		if quit_flag:
			continue
		# set the count after showing finish
		count = int(count_tm / 5)
		count_total = count
		img_o = img
		# resive the window
		c_w, c_h = 266, 100
		#cv.resizeWindow(window_name, c_h, c_w)
		# move window to the right bottom conner
		cv.moveWindow(window_name, full_sc_width-30-c_w, full_sc_height-70-c_h)
		# the end flag
		is_count_end = False
		# here set the flag that mark if you need to record
		is_need_to_write_file = False
		if count_tm >= 60 * file_write_threshold:
			is_need_to_write_file = True
			# then open the plan file to write the
			plan_path = os.path.join(everyday_dir, "plan.txt")
			question_path = os.path.join(everyday_dir, "question.txt")
			record_path = os.path.join(everyday_dir, "record.txt")
			#for _path in [plan_path, question_path, record_path]:
			append_time_to_file(plan_path, count_tm)

			os.system(f"{editor} {plan_path}")
		while count_tm>0:
			img_bg = np.zeros((c_h, c_w, 3), np.uint8)
			min_digit = int(count_tm // 60)
			sec_digit = int(count_tm - 60 * min_digit)
			count_down_show = f"{min_digit:0>2} : {sec_digit:0>2}"
			cv.putText(img_bg, count_down_show, (int(0.3*c_w), int(0.5*c_h)), cv.FONT_HERSHEY_COMPLEX, 1, count_down_color, 3)
			cv.imshow(window_name, img_bg)
			key_val_1 = cv.waitKey(1) & 0xff
			if key_val_1 == ord('q'):
				print("quit the countdown!")
				# set the quit flag
				quit_flag = True
				if is_need_to_write_file:
					# change the bg
					img_bg = np.zeros((c_h, c_w, 3), np.uint8)
					quit_text_1 = "finish or terminate?"
					quit_text_2 = "finish[a], terminate[b]."
					cv.putText(img_bg, quit_text_1, (int(0.1 * c_w), int(0.3 * c_h)), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 255), 1)
					cv.putText(img_bg, quit_text_2, (int(0.1 * c_w), int(0.8 * c_h)), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)
					cv.imshow(window_name, img_bg)
					key_val_quit = cv.waitKey() & 0xff
					if key_val_quit not in [ord('a'), ord('b')]:
						break
					else:
						# here open the file
						lines = []
						with open(plan_path, "r", encoding="utf-8") as f:
							lines = f.readlines()
						#
						if key_val_quit == ord('a'):
							# change the last time to now
							time_that_write_plan = time.time()
							change_time = time.strftime("%H:%M", time.localtime())
							time_pattern = r"- *(\d{2}:\d{2})"
							for i in range(len(lines)):
								line = lines[len(lines)-i-1]
								t_m = re.search(time_pattern, line)
								if t_m:
									time_point = t_m.group(1)
									line = line.replace(time_point, change_time)
									# renew the lines
									lines[len(lines)-i-1] = line
									# then break
									break
							# still need to add the content to the question and the record
							is_need_to_write_file = True
							is_count_end = True
						elif key_val_quit == ord('b'):
							flag_new_line = False
							flag_item = False
							# delete the plan's content of the last line
							for i in range(len(lines)):
								last_line = lines[-1]
								last_line = last_line.strip("\n ")
								if len(last_line) > 0:
									flag_item = True
									if flag_new_line:
										lines[-1] = last_line
										break
									else:
										lines.pop()
								else:
									lines.pop()
									if flag_item:
										flag_new_line = True
							# write the content to the file
							with open(plan_path, "w", encoding="utf-8") as f:
								f.write("".join(lines))
							# set is_need_to_write_file to False
							is_need_to_write_file = False
						# at last, will break the loop
				break
			elif key_val_1 == ord('x'): ## contenctrate, cover the weixin and the qq
				count_down_is_in_concentrate_mode = not count_down_is_in_concentrate_mode
				if count_down_is_in_concentrate_mode:
					cv.moveWindow(window_name, full_sc_width-30-c_w, full_sc_height-20-c_h) # height -70 -> -20
				else:
					cv.moveWindow(window_name, full_sc_width-30-c_w, full_sc_height-70-c_h) # move back
			elif key_val_1 == ord('s'):
				cv.putText(img_bg, "stop! key 'c' to go!", (int(0.2*c_w), int(0.8*c_h)), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)
				while True:
					cv.imshow(window_name, img_bg)
					key_val_2 = cv.waitKey(1000) & 0xff
					if key_val_2 == ord('c'):
						print("continue!")
						break
			# sleep
			time.sleep(1)
			count_tm -= 1
			if count_tm == 0:
				is_count_end = True
		# recover the window size
		if is_count_end:
			count_end_named_window = "full screen"
			cv.namedWindow(count_end_named_window, cv.WINDOW_NORMAL)
			cv.moveWindow(count_end_named_window, 0, 0)
			cv.setWindowProperty(count_end_named_window, cv.WND_PROP_TOPMOST, 1)
			cv.setWindowProperty(count_end_named_window, cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
			if is_use_duplicate_window:
				count_end_named_window_dp = "full screen dp"
				cv.namedWindow(count_end_named_window_dp, cv.WINDOW_NORMAL)
				cv.moveWindow(count_end_named_window_dp, 1920, 0)
				cv.setWindowProperty(count_end_named_window_dp, cv.WND_PROP_TOPMOST, 1)
				cv.setWindowProperty(count_end_named_window_dp, cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
			    #move the window to the rigth screen
			if not is_show_random:
				scenery_video_path = play_video_path
				# check if the path is exist and if the path can open
				scen_cap = cv.VideoCapture(scenery_video_path)
				if scen_cap.isOpened():
					scen_img_num = scen_cap.get(cv.CAP_PROP_FRAME_COUNT)
					scen_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
					scen_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
				else:
					is_show_random = True
					# fail to open the video, 1) the path not exists; 2) there is some problem with the video
					if not os.path.exists(scenery_video_path):
						print(f"video path {scenery_video_path} not exists! So choose the random images!")
					else:
						print(f"can not open the {scenery_video_path}, so show the random images!")
					scen_cap.release()
			while True:
				# show the full red screen
				if is_show_random:
					full_screen = 22 * np.ones((full_sc_height, full_sc_width, 3), np.uint8)
					full_screen[..., 0] = random.randint(0, 255)
					full_screen[..., 1] = random.randint(0, 255)
					full_screen[..., 2] = random.randint(0, 255)
				else:
					select_scen_num = random.randint(1, scen_img_num)
					scen_cap.set(cv.CAP_PROP_POS_FRAMES, select_scen_num)
					_, full_screen = scen_cap.read()
					if (full_sc_width / scen_width) > (full_sc_height / scen_height):
						scale_sz = full_sc_height / scen_height
					else:
						scale_sz = full_sc_width / scen_width
					#full_screen = cv.resize(full_screen, (int(scale_sz*scen_width*0.9), int(scale_sz*scen_height*0.9)))
					full_screen = cv.resize(full_screen, (full_sc_width, full_sc_height))
				cv.imshow(count_end_named_window, full_screen)
				if is_use_duplicate_window:
					full_screen_dp = progress(full_sc_height, full_sc_width, int(full_sc_height/66), count_total, count)
					cv.imshow(count_end_named_window_dp, full_screen_dp)
				key_val_3 = cv.waitKey(1000) & 0xff
				count -= 1
				if key_val_3 == ord('q') or count<0:
					break
		if is_count_end and not is_show_random:
			scen_cap.release()
		# if count < 0, then show the other image instead of the camera's image
		if count < 0:
			waiting_img = np.zeros((full_sc_height, full_sc_width, 3), np.uint8)
			cv.putText(waiting_img, "To be continued!", (int(0.3*full_sc_width), int(0.5*full_sc_height)), cv.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 3)
			# wait_time
			wait_time = 2
			while True:
				cv.imshow(count_end_named_window, waiting_img)
				if is_use_duplicate_window:
					cv.imshow(count_end_named_window_dp, waiting_img)
				key_val_4 = cv.waitKey(1000)
				wait_time -= 1
				if wait_time <0 or key_val_4 in [ord(' '), ord('c'), ord('q'), ord('e')]:
					break
			if wait_time < 0:
				# enter the emergency mode
				init_wt = 399
				init_col = 22
				n = 1
				while True:
					if n < 0 and init_wt == 1:
						n = 1
						init_wt = 399
						init_col = 22
					# renew the wt and the color
					if init_wt > 100:
						init_wt -= 0.06 * n
					elif init_wt > 80:
						init_wt -= 0.05 * n
					elif init_wt > 60:
						init_wt -= 0.04 * n
					elif init_wt > 30:
						init_wt -= 0.04 * n
					else:
						init_wt -= 0.02* n
					init_wt = int(init_wt)
					if init_wt < 1:
						init_wt = 1
					init_col += 0.05 * n
					init_col = int(init_col)
					if init_col > 255:
						init_col = 255
					w_full_screen =  np.ones((full_sc_height, full_sc_width, 3), np.uint8)
					w_full_screen[..., 0] = col_b = random.randint(0, init_col)
					w_full_screen[..., 1] = col_g = random.randint(0, init_col)
					w_full_screen[..., 2] = col_r = random.randint(0, init_col)
					# here copy the img to the be used by the duplicated window!
					if is_use_duplicate_window:
						w_full_screen_cp = w_full_screen.copy()
						cv.putText(w_full_screen_cp, "Time Out!", (int(0.3*full_sc_width), int(0.5*full_sc_height)), cv.FONT_HERSHEY_COMPLEX, 3, (255-col_b, 255-col_g, 255-col_r), 5)
						cv.imshow(count_end_named_window_dp, w_full_screen_cp)
					cv.putText(w_full_screen, "Need Working!", (int(0.3*full_sc_width), int(0.5*full_sc_height)), cv.FONT_HERSHEY_COMPLEX, 3, (255-col_b, 255-col_g, 255-col_r), 5)
					cv.imshow(count_end_named_window, w_full_screen)
					# is_shine_screen = False, set the inti_wt to 0
					if not is_shine_screen:
						init_wt = 0
					key_val_5 = cv.waitKey(init_wt)
					if key_val_5 in [ord(' '), ord('c'), ord('q'), ord('e')]:
						break
					if init_wt == 1:
						n -= 0.2
					else:
						n += 1
		# here destroy the count_end_named_window, this is very important
		if is_count_end:
			cv.destroyWindow(count_end_named_window)
			if is_use_duplicate_window:
				cv.destroyWindow(count_end_named_window_dp)
		if is_need_to_write_file:
			if is_open_question_record:
				# first, write the time
				question_path = os.path.join(everyday_dir, "question.txt")
				record_path = os.path.join(everyday_dir, "record.txt")
				write_question_record_time_duration = count_tm_copy - count_tm
				for _path in [question_path, record_path]:
					append_time_to_file(_path, write_question_record_time_duration, start_time=time_that_write_plan)
				# end the countdown, open the record file and the question file
				# here use the threads to open the file
				def run_two_files():
					os.system(f"{editor} {question_path}")
					os.system(f"{editor} {record_path}")
				Thread(target=run_two_files, args=()).start()
				# after writing, set the is_need_to_write_file to false
			else:
				# open the plan file
				Thread(target=lambda: os.system(f"{editor} {plan_path}"), args=()).start()

			is_need_to_write_file = False
		# here have to set the bg change flag
		bg_change_flag = True
		# move window to the right bottom conner
		cv.moveWindow(window_name, full_sc_width - 30 - width, full_sc_height - 70 - height)
		cv.imshow(window_name, img_o)
	if is_save:
		out.write(img)