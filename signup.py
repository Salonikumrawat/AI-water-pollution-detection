
from tkinter import *
from PIL import ImageTk
from PIL import Image, ImageColor
from tkinter import messagebox
import pymysql

# Functionality part 
def clear():
    EmailEntry.delete(0,END)
    UsernameEntry.delete(0,END)
    PasswordEntry.delete(0,END)
    ConfPasswordEntry.delete(0,END)
    check.set(0)


def connectt_database():
    if EmailEntry.get()=='' or UsernameEntry.get()=='' or PasswordEntry.get()=='' or ConfPasswordEntry.get()=='':
        messagebox.showerror('Error','all fields are required')
    elif PasswordEntry.get() != ConfPasswordEntry.get():
        messagebox.showerror('Error','Password mismatched')
    elif check.get()==0:
        messagebox.showerror('Error','Please accept the terms and conditions')
    else:
        try:
            con=pymysql.connect(host='localhost',user='root',password='K24#2001@jqir#')
            mycursor=con.cursor()
        except:
              messagebox.showerror('Error','Database Connectivity Issue,Please try again')
              return
        
        try:
           query='create database userdata'
           mycursor.execute(query)
           query='use userdata'
           mycursor.execute(query)
           query='create table Signupdata(id int auto_increment primary key not null,Email varchar(50),Username varchar(100),Password varchar(20))'
           mycursor.execute(query)
        except:
            mycursor.execute('use userdata')

        query='select * from signupdata where username=%s'
        mycursor.execute(query,(UsernameEntry.get()))

        row=mycursor.fetchone()
        if row != None:
             messagebox.showerror('Error','The username already exists')
        else:

             query='insert into signupdata(Email,Username,Password) values(%s,%s,%s)'
             mycursor.execute(query,(EmailEntry.get(),UsernameEntry.get(),PasswordEntry.get()))
             con.commit()
             con.close()
             messagebox.showinfo('success','Resgistration Is Successful')
             clear()
             Signuproot.destroy()
             import login




def login_page():
     Signuproot.destroy()
     import login

def Email_enter(event):
    if EmailEntry.get() == 'Email':
       EmailEntry.delete(0, END)

def user_enter(event):
    if UsernameEntry.get() == 'Username':
        UsernameEntry.delete(0, END)

def password_enter(event):
    if PasswordEntry.get() == 'Password':
        PasswordEntry.delete(0, END)

def hide():
    openeye.config(file='closeye.png')
    PasswordEntry.config(show='*')
    eyeButton.config(command=show)
def show():
    openeye.config(file='openeye.png')
    PasswordEntry.config(show='')
    eyeButton.config(command=hide)


def Confpassword_enter(event):
    if ConfPasswordEntry.get() == 'ConfirmPassword':
        ConfPasswordEntry.delete(0, END)

def hide1():
    openeye1.config(file='closeye1.png')
    ConfPasswordEntry.config(show='*')
    eyeButton1.config(command=show1)
def show1():
    openeye1.config(file='openeye1.png')
    ConfPasswordEntry.config(show='')
    eyeButton1.config(command=hide1)



# GUI
Signuproot = Tk()
Signuproot.resizable(0, 0)
Signuproot.title('SignUp Page')

bgImage = ImageTk.PhotoImage(file='bg12.png')
bgLabel = Label(Signuproot, image=bgImage)
bgLabel.grid(row=0, column=0)


heading = Label(Signuproot, text='SignUp', font=('Microsoft Yahei UI Light', 25, 'bold'), bg='white', fg='grey')
heading.place(x=600, y=120)

# Email create
EmailEntry = Entry(Signuproot, width=25, font=('Microsoft Yahei UI Light', 12, 'bold'), bd=0, fg='grey')
EmailEntry.place(x=550, y=200)
EmailEntry.insert(0, 'Email')
EmailEntry.bind('<FocusIn>', Email_enter)

Frame1 = Frame(Signuproot, width=250, height=2, bg='grey')  # Line under the Email created using frame
Frame1.place(x=550, y=222)

# Username create
UsernameEntry = Entry(Signuproot, width=25, font=('Microsoft Yahei UI Light', 12, 'bold'), bd=0, fg='grey')
UsernameEntry.place(x=550, y=250)
UsernameEntry.insert(0, 'Username')
UsernameEntry.bind('<FocusIn>', user_enter)

Frame2 = Frame(Signuproot, width=250, height=2, bg='grey')  # Line under the username created using frame
Frame2.place(x=550, y=272)

# Password create
PasswordEntry = Entry(Signuproot, width=25, font=('Microsoft Yahei UI Light', 12, 'bold'), bd=0, fg='grey')
PasswordEntry.place(x=550, y=300)
PasswordEntry.insert(0, 'Password')
PasswordEntry.bind('<FocusIn>', password_enter)

Frame3 = Frame(Signuproot, width=250, height=2, bg='grey')  # Line under the password created using frame
Frame3.place(x=550, y=322)

openeye=PhotoImage(file='openeye.png')
eyeButton=Button(Signuproot,image=openeye,bd=0,bg="white",cursor='hand2',command=hide)
eyeButton.place(x=780,y=295)

#  confirm Password create
ConfPasswordEntry = Entry(Signuproot, width=25, font=('Microsoft Yahei UI Light', 12, 'bold'), bd=0, fg='grey')
ConfPasswordEntry.place(x=550, y=350)
ConfPasswordEntry.insert(0, 'ConfirmPassword')
ConfPasswordEntry.bind('<FocusIn>',Confpassword_enter)

Frame4 = Frame(Signuproot, width=250, height=2, bg='grey')  # Line under the Confirmpassword created using frame
Frame4.place(x=550, y=372)

openeye1=PhotoImage(file='openeye1.png')
eyeButton1=Button(Signuproot,image=openeye,bd=0,bg="white",cursor='hand2',command=hide1)
eyeButton1.place(x=780,y=345)


#terms and condition

check=IntVar()

termsandcondition=Checkbutton(Signuproot,text='I agree to the Terms and Condition',bg="white",fg='grey',variable=check)
termsandcondition.place(x=550,y=380)


#create button
CreateButton=Button(Signuproot,text='SignUp',font=('open sans',13,'bold'),bd=0,bg='grey',cursor='hand2',fg='White',width=7,
                    relief="groove",command=connectt_database)
CreateButton.place(x=630, y=440)

#Back to login page button


signinLabel=Label(Signuproot,text="Go back to Login page?→",font=('open sans',10 ),bg='white',fg='Black')
signinLabel.place(x=550, y=500)

signinButton=Button(Signuproot,text='login',font=('open sans',13,'bold'),bd=0,bg='White',cursor='hand2',fg='Black',width=7,
                    relief="groove",command=login_page)
signinButton.place(x=720, y=498)


Signuproot.mainloop()
