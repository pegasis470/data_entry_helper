# !/bin/python3
# GNU General Public License v3.0-or-later
# (c) pegasis470 (Sumant Dhere) <www.sumantdhere@gamil.com>
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
main_lst=[]
def Open():
    global time_list
    global count
    global temp_time_lst
    start_time = dt.now()
    time_list.append(start_time.timestamp())
    try:
        file=pd.read_csv(path)
    except pd.errors.EmptyDataError :
        open_file=open(path,'a')
        Writer=writer(open_file)
        Writer.writerow(["Machine name","username","Open time",'Close time','Up time'])
        open_file.close()
    file=pd.read_csv(path)
    machine_list=list(file["Machine name"].values)
    try:
        if menu.get() in machine_list and file.iloc[machine_list.index(menu.get()),3] == '0' or file.iloc[machine_list.index(menu.get()),3] == 0 :
            messagebox.showerror("Information","Machine Already Running")
            return False
        elif menu.get() in machine_list and file.iloc[machine_list.index(menu.get()),3] != '0' or file.iloc[machine_list.index(menu.get()),3] != 0:
            global repeat
            repeat = 1
    except ValueError:
        pass
    lst=[menu.get(),Username.get(),dt.now().strftime('%I:%M:%S,%p'),'0','0']
    file.loc[len(file)]=lst
    try:
        file.to_csv(path,index=False)
    except PermissionError:
        messagebox.showerror("ERROR","the exel file is open in other program close it and try agian")
        return False
    messagebox.showinfo("Information","Saved succesfully")
    Username.delete(0,END)
    lst=[]
def Close():
        global repeat
        machine = menu.get()
        file = pd.read_csv(path)
        machine_list=list(file['Machine name'].values)
        end_time=dt.now().timestamp()
        try:
                if repeat == 1 :
                    index_pos = len(machine_list) - machine_list[::-1].index(machine) - 1
                    file.iloc[index_pos,3] = dt.now().strftime("%I:%M:%S,%p")
                    file.iloc[index_pos,-1] = str(datetime.timedelta(seconds=abs(end_time-time_list[index_pos])))
                    try:
                        file.to_csv(path, index=False)
                    except PermissionError:
                        messagebox.showerror("ERROR","the exel file is open in other program close it and try agian")
                    repeat=0
                    messagebox.showinfo("Information","Saved succesfully")
                elif repeat!=1 and file.iloc[machine_list.index(machine),3] == '0' or file.iloc[machine_list.index(machine),3] == 0 :
                    file.iloc[machine_list.index(machine),3] = dt.now().strftime("%I:%M:%S,%p")
                    try:
                        file.to_csv(path, index=False)
                    except PermissionError:
                        messagebox.showerror("ERROR","the exel file is open in other program close it and try agian")
                        return False
                    file.iloc[machine_list.index(machine),-1] = str(datetime.timedelta(seconds=abs(end_time-time_list[machine_list.index(machine)])))
                    try:
                        file.to_csv(path, index=False)
                    except PermissionError:
                        messagebox.showerror("ERROR","the exel file is open in other program close it and try agian")
                        return False
                    messagebox.showinfo("Information","Saved succesfully")
                else:
                    messagebox.showerror("Information","Machine already closed")
        except ValueError:
                messagebox.showerror("ERROR","machine is not open yet")
def file_backup():
        global path
        global time_list
        try:
            file=pd.read_csv(path)
        except FileNotFoundError:
            file90=open(path,'w')
            file90.close()
        current_hour,current_min=dt.now().strftime("%I"),dt.now().strftime("%M")
        temp_time_list=time_list
        if current_hour == '12' and current_min == '00':
            new_name=str(f"{datetime.date.today()}_{dt.now().strftime('%p')}_data_entry.csv") #{dt.now().strftime('%p')}
            new_path = os.path.join(os.getcwd(),new_name)
            new_file=file.loc[(file['Close time']== '0')| (file['Close time']== 0)]
            new_file['Open time']= dt.now().strftime('%I:%M:%S,%p')
            new_file.to_csv(new_path, index=False)
            new_time_list=[]
            new_machine_lst=list(new_file['Machine name'].values)
            try:
                for i in list(new_file["Machine name"].values):
                     file.at[int(file[(file["Machine name"]==i) & (file["Close time"]==0)].index.values),"Close time"]=dt.now().strftime("%I:%M:%S,%p")
            except TypeError:
                try:
                    for i in list(new_file["Machine name"].values):
                         file.at[int(file[(file["Machine name"]==i) & (file["Close time"]=='0')].index.values),"Close time"]=dt.now().strftime("%I:%M:%S,%p")
                except TypeError:
                    pass
            file.to_csv(path,index=False)
            for i in range(len(new_machine_lst)):
                  new_time_list.append(dt.now().timestamp())
            diff_list=[]
            for i in temp_time_list:
                  diff_list.append(datetime.timedelta(seconds=abs(dt.now().timestamp()-i)))
            try:
                for i in list(new_file["Machine name"].values):
                     file.at[int(file[(file["Machine name"]==i) & (file["Up time"]==0)].index.values),"Up time"]=diff_list[int(file.loc[(file["Machine name"]==i) & (file["Up time"]==0)].index.values)]
            except TypeError:
                try:
                    for i in list(new_file["Machine name"].values):
                         file.at[int(file[(file["Machine name"]==i) & (file["Up time"]=='0')].index.values),"Up time"]=diff_list[int(file.loc[(file["Machine name"]==i) & (file["Up time"]=='0')].index.values)]
                except TypeError:
                    pass    
            file.to_csv(path,index=False)

            time_list=new_time_list
            path=new_path
            window.after(60000,file_backup)
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
