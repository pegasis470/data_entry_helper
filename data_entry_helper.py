from csv import *
from tkinter import *
from tkinter import messagebox
from datetime import datetime as dt
import pandas as pd
import datetime
import os
today=datetime.date.today()
window=Tk()
window.title('Data entry')
menu= StringVar()
menu.set('Choose machine name')
options = ['tony stark','peter parker','spiderman','ironman']
count = 0
name=str(f"{today}_{dt.now().strftime('%p')}_data_entry.csv")
path = os.path.join(os.getcwd(),name)
time_list=[]
repeat=0
def Open():
    global time_list
    global count
    global temp_time_lst
    global path
    start_time = dt.now()
    time_list.append(start_time.timestamp())
    file= open(path,"a")
    if count != 0:
        file = pd.read_csv(path)
        machine_list=list(file['Machine name'].values)
        try:
            if menu.get() in machine_list and file.iloc[machine_list.index(menu.get()),3] == '0' or file.iloc[machine_list.index(menu.get()),3] == 0 :
                messagebox.showerror("ERROR","machine already running")
                return False
            elif menu.get() in machine_list and file.iloc[machine_list.index(menu.get()),3] != '0' or file.iloc[machine_list.index(menu.get()),3] != 0:
                global repeat 
                repeat = 1
                pass
            
        except ValueError:
            pass
    else:
        pass 
    lst=[menu.get(),Username.get(),dt.now().strftime('%I:%M:%S,%p'),0,0]
    main_lst=[]
    main_lst.append(lst)
    Username.delete(0,END)
    file= open(path,"a")
    Writer=writer(file)
    if count == 0:
        Writer.writerow(["Machine name","username","Open time",'Close time','Up time'])
        count = count+1
    Writer.writerows(main_lst)
    messagebox.showinfo("Information","Saved succesfully")
    temp_time_lst=time_list
    file.close()
    lst=[]
            
def Close():
        global repeat
        global path
        machine = menu.get()
        file = pd.read_csv(path)
        machine_list=list(file['Machine name'].values)
        end_time=dt.now().timestamp()
        try:
                if repeat == 1 :
                    index_pos = len(machine_list) - machine_list[::-1].index(machine) - 1
                    file.iloc[index_pos,3] = dt.now().strftime("%I:%M:%S,%p")
                    file.iloc[index_pos,-1] = str(datetime.timedelta(seconds=abs(end_time-time_list[index_pos])))
                    file.to_csv(path, index=False)
                    repeat=0
                
                    messagebox.showinfo("Information","Saved succesfully")
                elif repeat!=1 and file.iloc[machine_list.index(machine),3] == '0' or file.iloc[machine_list.index(machine),3] == 0 :
                    file.iloc[machine_list.index(machine),3] = dt.now().strftime("%I:%M:%S,%p")
                    file.to_csv(path, index=False)
                    file.iloc[machine_list.index(machine),-1] = str(datetime.timedelta(seconds=abs(end_time-time_list[machine_list.index(machine)])))
                    file.to_csv(path, index=False)
                    messagebox.showinfo("Information","Saved succesfully")
                else:
                    messagebox.showerror("Information","Machine already closed")
        except ValueError:
                messagebox.showerror("ERROR","machine is not open yet")
def file_backup():
        print("called")
        global path
        global time_list
        try:
            file=pd.read_csv(path)
        except FileNotFoundError:
            file90=open(path,'w')
        current_hour,current_min=dt.now().strftime("%I"),dt.now().strftime("%M")
        temp_time_lst=time_list
        if current_hour == '12' and current_min == '00':
            print("satisfied")
            new_name=str(f"{today}_{dt.now().strftime('%p')}_data_entry.csv") #{dt.now().strftime('%p')}
            new_path = os.path.join(os.getcwd(),new_name)
            new_file=file.loc[file['Close time']== '0']
            try:
                new_file['Open time']= dt.now().strftime('%I:%M:%S,%p')
            except OSerror:
                file69=open(new_path,'w')
            new_file.to_csv(new_path, index=False)
            new_machine_lst=list(new_file['Machine name'].values)
            new_time_lst=[]
            file2=pd.read_csv(new_path)
            for i in range(len(new_file['Machine name'].values)):
                new_time_lst.append(dt.now().timestamp())
            time_list=new_time_lst
            temp_lst=[]
            for i in list(file2['Machine name'].values):
                temp_lst.append(int(file[file['Machine name']==i].index.values))
            diff_lst=[]
            final_uptime_lst=[]
            for i in temp_lst:
                diff_lst.append(temp_time_lst[i])
            for i in diff_lst:
                final_uptime_lst.append(datetime.timedelta(seconds=dt.now().timestamp()-i))
            for i in list(file[file["Close time"]=='0'].index.values):
                file.at[i,'Close time']=dt.now().strftime('%I:%M:%S %p')
            for i in list(file[file["Up time"]=='0'].index.values):
                for j in final_uptime_lst:
                    file.at[i,'Up time'] = j
            file.to_csv(path,index=False)
            time_list=new_time_lst
            path=new_path
        else:
            window.after(60000,file_backup)
label1=Label(window,text="Username: ",padx=20,pady=10)
label2=Label(window,text="Machine name",padx=20,pady=10)
Username=Entry(window,width=30,borderwidth=5)
Machine=OptionMenu(window,menu,*options)
add=Button(window,text="Open",command=Open)
close=Button(window , text="Close",command=Close)
label1.grid(row=0,column=0)
label2.grid(row=1,column=0)
Username.grid(row=0,column=1)
Machine.grid(row=1,column=1)
add.grid(row=3,column=0)
close.grid(row=3,column=2)
file_backup()
window.mainloop()

