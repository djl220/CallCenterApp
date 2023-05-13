import customtkinter as ctk
import sqlite3
from datetime import datetime
import pyodbc


#azure connection
Driver='{ODBC Driver 18 for SQL Server}'
Server='dannytest1.database.windows.net'
Database='CALLS'
Uid=''
Pwd=''

cnxn =  pyodbc.connect('DRIVER='+Driver+';SERVER=tcp:'+Server+';PORT=1433;DATABASE='+Database+';UID='+Uid+';PWD='+ Pwd) 
cursor = cnxn.cursor()
#end azure DB connection

window = ctk.CTk()
window.geometry("700x550")
window.title("Call Logging")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

phoneLbl = ctk.CTkLabel(master=window, text="Phone Number")
phoneLbl.grid(row=0, column=2, padx=50)
phoneEnt = ctk.CTkEntry(master=window, placeholder_text="123-456-7890")
phoneEnt.grid(row=1, column=2, padx=50)
cNameLbl = ctk.CTkLabel(master=window, text="Caller Name")
cNameLbl.grid(row=2, column=2, padx=50)
cNameEnt = ctk.CTkEntry(master=window, placeholder_text="Caller Name")
cNameEnt.grid(row=3, column=2, padx=50)
agentLbl = ctk.CTkLabel(master=window, text="Agent Name")
agentLbl.grid(row=4, column=2, padx=50)
agentEnt = ctk.CTkEntry(master=window, placeholder_text="Agent Name")
agentEnt.grid(row=5, column=2, padx=50)

commLbl = ctk.CTkLabel(master=window, text="Comments")
commLbl.place(in_=agentEnt, relx=0.25, rely = 1.0, y=15)

commEnt = ctk.CTkTextbox(master=window, width = 200)
commEnt.place(in_=commLbl, relx=-1, rely = 1.0, y=15)

logBox = ctk.CTkTextbox(master=window, width=200, corner_radius=0)
logBox.grid(row=7, column=0, columnspan = 2, sticky = ctk.W+ctk.E)
logBox.insert("0.0", "Welcome to the Thresholds Call Center Logger!")

def getTime():
    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
    return dt_string


def submit_press(wrapCode):
    currTime = getTime()
    currNumber = phoneEnt.get()
    currAName = agentEnt.get()
    currComment = commEnt.get("0.0", "end")
    currCName = cNameEnt.get()
    currCode = wrapCode

    #insert into AzureAD DB
    cursor.execute("insert into CALLS(TIME,ANAME,CNAME,CNUM,WRAP,COMMENT) values (?,?,?,?,?,?)", currTime,currAName,currCName,currNumber,currCode,currComment)
    cnxn.commit()

    #populate the log box with the submitted information
    logBox.delete("0.0","end")
    logBox.insert("0.0", "Entry Successfully Submitted! \n\n" + "Caller Number: " + currNumber + "\nCaller Name: " + currCName + "\nWrap Reason: " + currCode + "\nComments: " + currComment)


    #delete current text except for agent name
    phoneEnt.delete(0,"end")
    commEnt.delete("0.0", "end")
    cNameEnt.delete(0, "end")



window.grid_rowconfigure(0, weight=0)
window.grid_columnconfigure((0, 1), weight=0)
window.grid_location(100,100)

adminBtn = ctk.CTkButton(master=window, text="Administrative", command= lambda: submit_press('Administrative'), width=150)
adminBtn.grid(row=0, column=0, padx=(10,0), pady=(10,0))
ccbhcBtn = ctk.CTkButton(master=window, text="CCBHC", command= lambda: submit_press('CCBHC'), width=150)
ccbhcBtn.grid(row=0, column=1, padx=(10,0), pady=(10,0))
crisisBtn = ctk.CTkButton(master=window, text="Crisis", command= lambda: submit_press('Crisis'), width=150)
crisisBtn.grid(row=1, column=0, padx=(10,0), pady=(10,0))
curMemBtn = ctk.CTkButton(master=window, text="Current Member", command= lambda: submit_press('Current Member'), width=150)
curMemBtn.grid(row=1, column=1, padx=(10,0), pady=(10,0))
dirAsBtn = ctk.CTkButton(master=window, text="Directory Assistance", command= lambda: submit_press('Directory Assistance'), width=150)
dirAsBtn.grid(row=2, column=0, padx=(10,0), pady=(10,0))
doesNotBtn = ctk.CTkButton(master=window, text="Does Not Meet Criteria", command= lambda: submit_press('Does Not Meet Criteria'), width=150)
doesNotBtn.grid(row=2, column=1, padx=(10,0), pady=(10,0))
hangBtn = ctk.CTkButton(master=window, text="Hang Up", command= lambda: submit_press('Hang Up'), width=150)
hangBtn.grid(row=3, column=0, padx=(10,0), pady=(10,0))
houseBtn = ctk.CTkButton(master=window, text="Housing", command= lambda: submit_press('Housing'), width=150)
houseBtn.grid(row=3, column=1, padx=(10,0), pady=(10,0))
mcHenBtn = ctk.CTkButton(master=window, text="McHenry", command= lambda: submit_press('McHenry'), width=150)
mcHenBtn.grid(row=4, column=0, padx=(10,0), pady=(10,0))
referBtn = ctk.CTkButton(master=window, text="Referral", command= lambda: submit_press('Referral'), width=150)
referBtn.grid(row=4, column=1, padx=(10,0), pady=(10,0))
substBtn = ctk.CTkButton(master=window, text="Substance Use", command= lambda: submit_press('Substance Use'), width=150)
substBtn.grid(row=5, column=0, padx=(10,0), pady=(10,0))
vetsBtn = ctk.CTkButton(master=window, text="Vets", command= lambda: submit_press('Veterans'), width=150)
vetsBtn.grid(row=5, column=1, padx=(10,0), pady=(10,0))
willColBtn = ctk.CTkButton(master=window, text="Williams/Colbert", command= lambda: submit_press('Williams/Colbert'), width=150)
willColBtn.grid(row=6, column=0, padx=(10,0), pady=(10,0))
youthBtn = ctk.CTkButton(master=window, text="Youth", command= lambda: submit_press('Youth'), width=150)
youthBtn.grid(row=6, column=1, padx=(10,0), pady=(10,0))

window.mainloop()

