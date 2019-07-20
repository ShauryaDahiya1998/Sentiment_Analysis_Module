from tkinter import *
import sentiment_mod as s
import tkinter.messagebox
import mysql.connector

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="classmate1234",
  database="sentiment"
)

mycursor = mydb.cursor()

for x in mycursor:
  print(x)


root = Tk()

root.geometry("400x250")

def answer(event):
    ans = s.sentiment(rev.get())
    conf = ans[1]
    conf = conf*100
    conf = str(conf)
    conf = conf+'%'
    print(ans)
    ans = ans[0]
    print(ans)
    if ans is "pos":
        ans="positive"
    if ans is "neg":
        ans="negative"
    tkinter.messagebox.showinfo("Review","Your review was {}".format(ans))
    mycursor.execute("INSERT INTO sent (review, category, confidance) VALUES (%s,%s,%s)",(rev.get(),ans,conf))
    mydb.commit()

label = Label(root,text="how was your review of this?")
label.config(font=("Courier", 15))
label.grid(row=0,column=0,ipady=20,ipadx=20)
rev=StringVar()
entry = Entry(root,textvariable=rev)
entry.config(width=50)
entry.grid(row=1,column=0,ipady=20,ipadx=20,padx=20)
button = Button(root,text="Submit")
button.config(bg='red',font=(20))
button.grid(row=2,column=0,pady=20)
button.bind("<Button-1>", answer)
root.mainloop()