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
def Open():
    global time_list
    global count
    start_time = dt.now()
    time_list.append(start_time.timestamp())
    file= open(path,"a")
    if count != 0:
        file = pd.read_csv(path)
        machine_list=list(file['Machine name'].values)
        if menu.get() in machine_list:
            messagebox.showerror("ERROR","machine already running")
            return False
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
    file.close()
    lst=[]
def Close():
    while True:
            machine = menu.get()
            file = pd.read_csv(path)
            machine_list=list(file['Machine name'].values)
            end=dt.now().timestamp()
            try:
                if file.iloc[machine_list.index(machine),3] == '0' or file.iloc[machine_list.index(machine),3] == 0 :
                    file.iloc[machine_list.index(machine),3] = dt.now().strftime("%I:%M:%S,%p")
                    file.to_csv(path, index=False)
                    file.iloc[machine_list.index(machine),-1] = str(datetime.timedelta(seconds=abs(end-time_list[machine_list.index(machine)])))
                    file.to_csv(path, index=False)
                    messagebox.showinfo("Information","Saved succesfully")
                    break
                else:
                    messagebox.showinfo("Information","Machine already closed")
                    break
            except ValueError:
                messagebox.showerror("ERROR","machine is not open yet")
                break
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
window.mainloop()
