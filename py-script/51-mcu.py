import serial
import time

# time to hex
def lsToHexLs(ls):
    hex_ls = list()
    for i in ls:
        hex_i = hex(i)[2:]
        # check the len of the hex_i
        if len(hex_i) == 1:
            hex_ls.append("0"+hex_i)
        elif len(hex_i) >= 3:
            hex_ls.append(hex_i[:2])
        else:
            hex_ls.append(hex_i)
    return " ".join(hex_ls)


# open the serial
port_name = "COM4"
fre = 9600
time_out = 5
try: 
    ser = serial.Serial(port_name, fre, timeout=time_out)
    # check if you can open the port
    if not ser.isOpen():
        print(f"Can not open the serial: {port_name}")
        exit(0)
except:
    pass


# send the message to the port
while True:
    tm = time.localtime()
    hour, mins, sec = tm.tm_hour, tm.tm_min, tm.tm_sec
    mes_head = "11 "
    mes_tail = " 0d 0a"
    mes_body = lsToHexLs([hour, mins, sec])
    mes = mes_head + mes_body + mes_tail
    print(mes)
    mes = bytes.fromhex(mes)
    ser.write(mes)
    time.sleep(1)

