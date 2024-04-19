import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msg
import serial 
import time

# main 윈도우 선언
window = tk.Tk()
window.geometry("400x700")
window.title("servo_con")
###################################

#선택된 port 및 com1,2,3,4 선택 가능한 combobox
port_selected = ''

values=['COM1','COM2','COM3','COM4']; 


lb1 = tk.Label(window,text="PORT_SELECTION")
lb1.place(x=0,y=0)




combobox=ttk.Combobox(window, height=20,width=20, values=values)
combobox.place(x=0,y=20);

combobox.set("")
####################################

global py_serial

#com port 연결 on py_serial
# 연결 후 msg box 출력 
def serial_on_click():
    global py_serial
    port_selected = combobox.get()
    py_serial = serial.Serial(

    port=port_selected,
    # 선택 된 com x번을 사용해서 serial 통신
    baudrate=115200,
    )
    if(py_serial.is_open) :
        msg.showinfo("Info","Connected")

        
# 연결 close
def serial_off_click():
    global py_serial
    if(py_serial.is_open) :
        py_serial.close()
        msg.showinfo("Info","Closed")
####################################################        
    
s_connet_button = tk.Button(window, text = "SERIAL CONNECT",overrelief="solid", width=15, command=serial_on_click, repeatdelay=1000, repeatinterval=100)
s_connet_button.place(x=40,y=60)

s_disconnet_button = tk.Button(window, text = "DISCONNECT",overrelief="solid", width=15, command=serial_off_click, repeatdelay=1000, repeatinterval=100)
s_disconnet_button.place(x=200,y=60)


##########################################################

# 각 Scale bar 및 값이 저장될 value (IntVar) 선언

base_scale_value =tk.IntVar()

base_scale=tk.Scale(window, variable=base_scale_value,  orient="horizontal", showvalue=True, tickinterval=50, to=200, length=380)
base_scale.place(x=0,y=160)

label=tk.Label(window, text="Base_angle")
label.place(x=0,y=140)


sd_scale_value =tk.IntVar()

sd_scale=tk.Scale(window, variable=sd_scale_value,  orient="horizontal", showvalue=True, tickinterval=50, to=200, length=380)
sd_scale.place(x=0,y=250)

label=tk.Label(window, text="Sd_angle")
label.place(x=0,y=230)


upper_scale_value =tk.IntVar()

upper_scale=tk.Scale(window, variable=upper_scale_value,  orient="horizontal", showvalue=True, tickinterval=50, to=200, length=380)
upper_scale.place(x=0,y=340)

label=tk.Label(window, text="Upper_angle")
label.place(x=0,y=320)


fore_scale_value =tk.IntVar()

fore_scale=tk.Scale(window, variable=fore_scale_value,  orient="horizontal", showvalue=True, tickinterval=50, to=200, length=380)
fore_scale.place(x=0,y=430)

label=tk.Label(window, text="Fore_angle")
label.place(x=0,y=410)
#########################################################################3

#기본 list 선언 및 초기화
stat_listbox = tk.Listbox(window, selectmode='extended', height=0)
stat_listbox.place(x=0,y=500)

for i in range(4):
    stat_listbox.insert(i," ")
###########################################################################
    
# 스크롤바로 저장된 각 scale value를 아두이노로 update(write)
def run():
    
    commend = "a"+str(base_scale_value.get())+"b"+str(sd_scale_value.get())+"c"+str(upper_scale_value.get())+"d"+str(fore_scale_value.get())
    py_serial.write(commend.encode())
    # commend 를 encode해서 bit로 serial write
    time.sleep(0.1)




        

run_button = tk.Button(window, text = "RUN",overrelief="solid", width=15, command=run, repeatdelay=1000, repeatinterval=100)
run_button.place(x=150,y=600)

def stop():
    print("stop")

stop_button = tk.Button(window, text = "STOP",overrelief="solid", width=15, command=stop, repeatdelay=1000, repeatinterval=100)
stop_button.place(x=270,y=600)

########################################################################

# Stat_update 실행 될 떄 아두이노 쪽으로 stat_update command 보낸 후 리턴 받아서 list box update
global v
v = 0
global pos
pos = 0

def stat_update():
    commend = "stat_update"
    py_serial.write(commend.encode())
    # commend 를 encode해서 bit로 serial write
    time.sleep(0.1)
    if(py_serial.readable()):

        # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
        # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
        response = py_serial.readline()
        
        
        stat_listbox.delete(0,3)
        # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
        for temp in response[:len(response)-1].decode():
          global v
          global pos
          
          if(temp == str(' ')):
            stat_listbox.insert(pos,v)
            v = 0
            pos +=1
          elif(temp == str('\r') or temp == str('\n')):
            print(temp)
          else:
            v = v*10 + int(temp)
                  
            

    

stat_update_button = tk.Button(window, text = "Current Status",overrelief="solid", width=15, command=stat_update, repeatdelay=1000, repeatinterval=100)
stat_update_button.place(x=0,y=600)
#################################################################

window.mainloop()

