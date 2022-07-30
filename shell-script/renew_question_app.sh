# D:\\cygwin\\bin\\bash.exe
question_all_dir="/cygdrive/c/Users/gjsq/Desktop/CV_interviews_Campus-master/questions_all"
code_dir="/cygdrive/c/Users/gjsq/Desktop/camera-show/questions"
code_files="/cygdrive/c/Users/gjsq/Desktop/camera-show/*.py"

# renew the files
#mode="download"
#scp -r $hgj_lab:$question_all_dir "../CV_interviews_Campus-master"
scp -r $hgj_lab:$code_dir "./questions/"
scp -r $hgj_lab:$code_files "./"
