from tkinter import *
from PIL import ImageTk
from PIL import Image, ImageColor
from tkinter import messagebox
import pymysql

# Functionality part 
def Signup_page():
    root.destroy()
    import signup

def login_user():
    if UsernameEntry.get()=='' or PasswordEntry.get()=='':
        messagebox.showerror('Error','all field is required')
    else:
        try:
            con=pymysql.connect(host='localhost',user='root',password='K24#2001@jqir#')
            mycursor=con.cursor()  
        except:
            messagebox.showerror('error','the connection is not established try again' )
            return
        query='use userdata'
        mycursor.execute(query)
        query='select * from signupdata where username=%s and password=%s'
        mycursor.execute(query,(UsernameEntry.get(),PasswordEntry.get()))
        row=mycursor.fetchone()
        if row==None:
            messagebox.showerror('error','invalid username or password')
        else:
            messagebox.showinfo('success','Login is successful')
            root.destroy()  # Close the login window
           
            import loggedinmain

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

def animate_text():
    text = "HydroSentry"
    for i in range(len(text) + 1):
        animated_label.config(text=text[:i])
        root.update()
        root.after(100)  # Adjust the delay (in milliseconds) based on your preference


# GUI
root = Tk()
root.resizable(0, 0)
root.title('Login Page')

bgImage = ImageTk.PhotoImage(file='bg12.png')
bgLabel = Label(root, image=bgImage)
bgLabel.grid(row=0, column=0)

#animaion part

animated_label = Label(root, text='HydroSentry', font=('Helvetica-Bold', 30, 'bold'), bg='white'
                      ,fg='grey')
animated_label.place(x=550, y=121)
animate_text()


heading = Label(root, text='USER LOGIN', font=('Microsoft Yahei UI Light', 25, 'bold'), bg='white', fg='grey')
heading.place(x=567, y=180)

# Username create
UsernameEntry = Entry(root, width=25, font=('Microsoft Yahei UI Light', 12, 'bold'), bd=0, fg='grey')
UsernameEntry.place(x=550, y=270)
UsernameEntry.insert(0, 'Username')
UsernameEntry.bind('<FocusIn>', user_enter)

Frame1 = Frame(root, width=250, height=2, bg='grey')  # Line under the username created using frame
Frame1.place(x=550, y=292)

# Password create
PasswordEntry = Entry(root, width=25, font=('Microsoft Yahei UI Light', 12, 'bold'), bd=0, fg='grey')
PasswordEntry.place(x=550, y=330)
PasswordEntry.insert(0, 'Password')
PasswordEntry.bind('<FocusIn>', password_enter)

Frame2 = Frame(root, width=250, height=2, bg='grey')  # Line under the password created using frame
Frame2.place(x=550, y=352)

openeye=PhotoImage(file='openeye.png')
eyeButton=Button(root,image=openeye,bd=0,bg="white",cursor='hand2',command=hide)
eyeButton.place(x=770,y=325)

forgetButton=Button(root,text='forget password?',bd=0,bg='white',cursor='hand2',fg='grey')
forgetButton.place(x=700,y=370)
#login and create button
LoginButton=Button(root,text='Login',font=('open sans',16,'bold'),bd=0,bg='grey',cursor='hand2',fg='white',width=10,command=login_user)
LoginButton.place(x=600, y=410)

orlabel=Label(root,text='..................OR..................',font=('open sans',16,'bold'))
orlabel.place(x=540,y=460)

signupLabel=Label(root,text="don't have an account?→",font=('open sans',10 ),bg='white',fg='grey')
signupLabel.place(x=550, y=525)

CreateButton=Button(root,text='SignUp',font=('open sans',13,'bold'),bd=0,bg='White',cursor='hand2',fg='grey',width=7,
                    relief="groove",command=Signup_page)
CreateButton.place(x=700, y=520)

root.mainloop()
