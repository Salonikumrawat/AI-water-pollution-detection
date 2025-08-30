from tkinter import *
import numpy as np
from customtkinter import *
from tkinter import PhotoImage
from tkinter import messagebox
import pymysql
from datetime import datetime
import matplotlib.pyplot as plt
import subprocess


#push button function

def push_data():
    try:
        # Connect to the database
        con = pymysql.connect(host='localhost', user='root', password='K24#2001@jqir#', database='userdata')
        cursor = con.cursor()

        # Join riverdata table with oldriverdata table and truncate riverdata table
        query = """
        INSERT INTO oldriverdata (river, date, ph, temp, turbidity, conductivity)
        SELECT river, date, ph, temp, turbidity, conductivity
        FROM riverdata
        """
        cursor.execute(query)

        # Truncate riverdata table
        truncate_query = "TRUNCATE TABLE riverdata"
        cursor.execute(truncate_query)

        con.commit()
        messagebox.showinfo('Success', 'Data pushed successfully and riverdata table truncated.')

    except pymysql.Error as e:
        messagebox.showerror('Error', f'Database Error: {e}')

    finally:
        # Close the database connection
        if con:
            con.close()


def perform_prediction():
    try:
        # Call the prediction script using subprocess
        subprocess.run(["python", "mainprediction.py"])
    except Exception as e:
        messagebox.showerror('Error', f'Prediction Error: {e}')

# Function to connect to the database, create tables, and insert sensor data


def connect_database():
    river_name = river_entry.get()
    if river_name == '':
        messagebox.showerror('Error', 'All fields are required')
        return

    try:
        con = pymysql.connect(host='localhost', user='root', password='K24#2001@jqir#', database='userdata')
        mycursor = con.cursor()
    except pymysql.Error as e:
        messagebox.showerror('Error', f'Database Connectivity Issue: {e}')
        return

    try:
        # Create table if not exists
        query = "CREATE TABLE IF NOT EXISTS riverdata (id INT AUTO_INCREMENT PRIMARY KEY, river VARCHAR(50), date DATE, ph FLOAT, temp FLOAT, turbidity FLOAT, conductivity FLOAT)"
        mycursor.execute(query)

        # Get manual input for pH, date, temperature, turbidity, and conductivity
        ph = float(ph_entry.get())
        date_str = date_entry.get()
        temp = float(temp_entry.get())
        turbidity = float(turbidity_entry.get())
        conductivity = float(conductivity_entry.get())

        # Convert date string to date object
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

        # Insert data into the table
        insert_query = "INSERT INTO riverdata (river, date, ph, temp, turbidity, conductivity) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (river_name, date_obj, ph, temp, turbidity, conductivity)
        mycursor.execute(insert_query, data)

        
        con.commit()

        messagebox.showinfo('Success', 'Data inserted successfully.')

    except Exception as e:
        messagebox.showerror('Error', f'Database Error: {e}')

    finally:
        # Close the database connection
        if con:
            con.close()



# Function to plot the graph
def plot_graph():
    # Fetch data from both tables
    river_name = river_entry.get()

    try:
        # Connect to the database
        con = pymysql.connect(host='localhost', user='root', password='K24#2001@jqir#', database='userdata')
        cursor = con.cursor()

        # Fetch data from riverdata table
        query_riverdata = "SELECT date, ph FROM riverdata WHERE river = %s"
        cursor.execute(query_riverdata, (river_name,))
        result_riverdata = cursor.fetchall()

        # Fetch data from oldriverdata table
        query_oldriverdata = "SELECT date, ph FROM oldriverdata WHERE river = %s"
        cursor.execute(query_oldriverdata, (river_name,))
        result_oldriverdata = cursor.fetchall()

        # Combine results from both tables and sort by pH value
        combined_results = list(result_riverdata) + list(result_oldriverdata)
        combined_results.sort(key=lambda x: float(x[1]))  # Sort by pH value

        if combined_results:
            # Extract year and pH values from the combined results
            years = [data[0].year for data in combined_results]
            ph_values = [data[1] for data in combined_results]

            # Plot the graph
            plt.plot(years, ph_values, marker='o', linestyle='-')
            plt.xlabel('Year')
            plt.ylabel('pH')
            plt.title(f'Combined pH Variation Over Years for River {river_name}')
            plt.grid(True)
            plt.ylim(0, 10)  # Set y-axis range from 0 to 10
            plt.gca().invert_yaxis()  # Reverse the y-axis
            plt.show()
        else:
            messagebox.showinfo('Info', 'No data found for the selected river.')

    except pymysql.Error as e:
        messagebox.showerror('Error', f'Database Error: {e}')

    finally:
        # Close the database connection
        if con:
            con.close()



def river_enter(event):
    if river_entry.get() == 'rivername':
        river_entry.delete(0, END)

loggedroot = CTk()
loggedroot.geometry("1280x725")
loggedroot.resizable(0, 0)
loggedroot.title('Logged Page')

# Load the background image
background_image =PhotoImage(file="bg123.png")
background_label = CTkLabel(master=loggedroot, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

heading1 = Label(loggedroot, text='HYDROSENTRY', font=('TIMES NEW ROMAN', 30, 'bold'), bg='#606190', fg='WHITE')
heading1.place(x=730, y=100)

frame_3 = CTkFrame(master=loggedroot, fg_color="#606190")
frame_3.grid(row=2, column=2, padx=300, pady=200)

CTkLabel(master=frame_3, text="DETAILS REQUIRED", font=("TIMES NEW ROMAN", 20), justify="left").pack(expand=True, pady=(30, 15))
river_entry = CTkEntry(master=frame_3, placeholder_text="Enter the river Name", width=400)
river_entry.pack(expand=True, pady=15, padx=20)
river_entry.insert(0, 'rivername')
river_entry.bind('<FocusIn>', river_enter)

# Create a frame to hold pH and Date entry fields in a single row
frame_ph_date = CTkFrame(master=frame_3)
frame_ph_date.pack(expand=True, fill="both", pady=(10, 15))

ph_label = CTkLabel(master=frame_ph_date, text="pH:")
ph_label.pack(side="left", padx=(0, 10))
ph_entry = CTkEntry(master=frame_ph_date)
ph_entry.pack(side="left")

date_label = CTkLabel(master=frame_ph_date, text="Date (YYYY-MM-DD):")
date_label.pack(side="left", padx=(20, 10))
date_entry = CTkEntry(master=frame_ph_date)
date_entry.pack(side="left")

# Create a frame to hold Temperature, Turbidity, and Conductivity entry fields in a single row
frame_sensor_data = CTkFrame(master=frame_3)
frame_sensor_data.pack(expand=True, fill="both", pady=(10, 15))

temp_label = CTkLabel(master=frame_sensor_data, text="Temperature:")
temp_label.pack(side="left", padx=(0, 10))
temp_entry = CTkEntry(master=frame_sensor_data)
temp_entry.pack(side="left")

turbidity_label = CTkLabel(master=frame_sensor_data, text="Turbidity:")
turbidity_label.pack(side="left", padx=(20, 10))
turbidity_entry = CTkEntry(master=frame_sensor_data)
turbidity_entry.pack(side="left")

conductivity_label = CTkLabel(master=frame_sensor_data, text="Conductivity:")
conductivity_label.pack(side="left", padx=(20, 10))
conductivity_entry = CTkEntry(master=frame_sensor_data)
conductivity_entry.pack(side="left")


CTkButton(master=frame_3, text="SAVE", command=connect_database).pack(expand=True, fill="both", pady=(30, 15), padx=30)



frame_1 = CTkScrollableFrame(master=loggedroot, fg_color="grey")
frame_1.grid(row=0, column=0, rowspan=10, sticky="nsew", padx=0, pady=0)



CTkLabel(master=frame_1, text="HOME", font=("TIMES NEW ROMAN", 20), justify="left").pack(expand=True, pady=(30, 15))
CTkButton(master=frame_1, text="About Us").pack(expand=True, fill="both", pady=(30, 15), padx=30)


# Create "Graph" button to plot graph
CTkButton(master=frame_1, text="Graph", command=plot_graph).pack(expand=True, fill="both", pady=(30, 20), padx=30)

# Create "Prediction" button to execute prediction code
CTkButton(master=frame_1, text="Prediction", command=perform_prediction).pack(expand=True, fill="both", pady=(30, 20), padx=30)

#push button
CTkButton(master=frame_1, text="Push", command=push_data).pack(expand=True, fill="both", pady=(30, 20), padx=30)


loggedroot.mainloop()




"""from tkinter import *
from customtkinter import *
from tkinter import PhotoImage
from tkinter import messagebox
import pymysql
from datetime import datetime
import matplotlib.pyplot as plt
import subprocess


#push button function

def push_data():
    try:
        
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="K24#2001@jqir#",
            database="userdata"
        )
        
        cursor = conn.cursor()

        # Fetch all rows from riverdata table
        cursor.execute("SELECT * FROM riverdata")
        rows = cursor.fetchall()

        # Insert fetched rows into oldriverdata table
        if rows:
            cursor.executemany("INSERT INTO oldriverdata VALUES (%s, %s, %s)", rows)
            conn.commit()
            print("Data pushed successfully")
        else:
            print("No data found to push")

    except pymysql.Error as error:
        print("Error:", error)

    finally:
        if conn:
            cursor.close()
            conn.close()


def perform_prediction():
    try:
        # Call the prediction script using subprocess
        subprocess.run(["python", "mainprediction.py"])
    except Exception as e:
        messagebox.showerror('Error', f'Prediction Error: {e}')

# Function to connect to the database, create tables, and insert sensor data


def connect_database():
    river_name = river_entry.get()
    if river_name == '':
        messagebox.showerror('Error', 'All fields are required')
        return

    try:
        con = pymysql.connect(host='localhost', user='root', password='K24#2001@jqir#', database='userdata')
        mycursor = con.cursor()
    except pymysql.Error as e:
        messagebox.showerror('Error', f'Database Connectivity Issue: {e}')
        return

    try:
        # Create table if not exists
        query = "CREATE TABLE IF NOT EXISTS riverdata ( id INT AUTO_INCREMENT PRIMARY KEY, river VARCHAR(50),date DATE,ph FLOAT, temp FLOAT, turbidity FLOAT,conductivity FLOAT)"
        mycursor.execute(query)

        # Fetch sensor data (replace with actual sensor readings)
        ph = 9
        date_str = "2024-03-24"
        temp = 27.2
        turbidity = 97
        conductivity = 457

        # Convert date string to date object
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

        # Insert data into the table
        insert_query = "INSERT INTO riverdata (river, date, ph, temp, turbidity, conductivity) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (river_name, date_obj, ph, temp, turbidity, conductivity)
        mycursor.execute(insert_query, data)
        con.commit()

        messagebox.showinfo('Success', 'Data inserted successfully.')

    except pymysql.Error as e:
        messagebox.showerror('Error', f'Database Error: {e}')

    finally:
        # Close the database connection
        if con:
            con.close()

# Function to plot the graph
def plot_graph():
    # Fetch data from both tables
    river_name = river_entry.get()

    try:
        # Connect to the database
        con = pymysql.connect(host='localhost', user='root', password='K24#2001@jqir#', database='userdata')
        cursor = con.cursor()

        # Fetch data from riverdata table
        query_riverdata = "SELECT date, ph FROM riverdata WHERE river = %s"
        cursor.execute(query_riverdata, (river_name,))
        result_riverdata = cursor.fetchall()

        # Fetch data from oldriverdata table
        query_oldriverdata = "SELECT date, ph FROM oldriverdata WHERE river = %s"
        cursor.execute(query_oldriverdata, (river_name,))
        result_oldriverdata = cursor.fetchall()

        # Combine results from both tables
        combined_results = result_riverdata + result_oldriverdata

        if combined_results:
            # Extract year and pH values from the combined results
            years = [data[0].year for data in combined_results]
            ph_values = [data[1] for data in combined_results]

            # Plot the graph
            plt.plot(years, ph_values, marker='o', linestyle='-')
            plt.xlabel('Year')
            plt.ylabel('pH')
            plt.title(f'Combined pH Variation Over Years for River {river_name}')
            plt.grid(True)
            plt.show()
        else:
            messagebox.showinfo('Info', 'No data found for the selected river.')

    except pymysql.Error as e:
        messagebox.showerror('Error', f'Database Error: {e}')

    finally:
        # Close the database connection
        if con:
            con.close()



def river_enter(event):
    if river_entry.get() == 'rivername':
        river_entry.delete(0, END)

loggedroot = CTk()
loggedroot.geometry("1280x725")
loggedroot.resizable(0, 0)
loggedroot.title('Logged Page')

# Load the background image
background_image =PhotoImage(file="bg123.png")
background_label = CTkLabel(master=loggedroot, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

heading1 = Label(loggedroot, text='HYDROSENTRY', font=('TIMES NEW ROMAN', 30, 'bold'), bg='#606190', fg='WHITE')
heading1.place(x=730, y=100)

frame_3 = CTkFrame(master=loggedroot, fg_color="#606190")
frame_3.grid(row=2, column=2, padx=300, pady=200)

CTkLabel(master=frame_3, text="DETAILS REQUIRED", font=("TIMES NEW ROMAN", 20), justify="left").pack(expand=True, pady=(30, 15))
river_entry = CTkEntry(master=frame_3, placeholder_text="Enter the river Name", width=400)
river_entry.pack(expand=True, pady=15, padx=20)
river_entry.insert(0, 'rivername')
river_entry.bind('<FocusIn>', river_enter)

CTkButton(master=frame_3, text="SAVE", command=connect_database).pack(expand=True, fill="both", pady=(30, 15), padx=30)



frame_1 = CTkScrollableFrame(master=loggedroot, fg_color="grey")
frame_1.grid(row=0, column=0, rowspan=10, sticky="nsew", padx=0, pady=0)



CTkLabel(master=frame_1, text="HOME", font=("TIMES NEW ROMAN", 20), justify="left").pack(expand=True, pady=(30, 15))
CTkButton(master=frame_1, text="About Us").pack(expand=True, fill="both", pady=(30, 15), padx=30)



#fetch button
CTkButton(master=frame_1, text="Fetch", command=fetch_data).pack(expand=True, fill="both", pady=(30, 20), padx=30)



# Create "Graph" button to plot graph
CTkButton(master=frame_1, text="Graph", command=plot_graph).pack(expand=True, fill="both", pady=(30, 20), padx=30)

# Create "Prediction" button to execute prediction code
CTkButton(master=frame_1, text="Prediction", command=perform_prediction).pack(expand=True, fill="both", pady=(30, 20), padx=30)

#push button
CTkButton(master=frame_1, text="Push", command=push_data).pack(expand=True, fill="both", pady=(30, 20), padx=30)


loggedroot.mainloop()"""
