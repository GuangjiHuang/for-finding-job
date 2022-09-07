import re
#str = "输入_test@qq.com测试ha-ha.wang@SINA.COM.CN"
#str = "输入@qq.com"
str = "测试样例hello-world@qq.com-cn"
#str = input()
pattern = re.compile(r'([a-zA-Z0-9_][a-zA-Z0-9_.-]{1,}@[0-9a-zA-Z]*(\.[0-9a-zA-Z]{2,}){1,})')
ret_ls = pattern.findall(str)

ans = list()
for ret in ret_ls:
    ans.append(ret[0])
if len(ans) == 0:
    print("false")
else:
    ret_str = "true " + " ".join(ans)
    print(ret_str)

