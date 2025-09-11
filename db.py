
import pymysql

# Function to create tables in the database
def create_table():
    conn = pymysql.connect(host='localhost', user='root', password='K24#2001@jqir#', database='userdata')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS oldriverdata
                 (id INT AUTO_INCREMENT PRIMARY KEY, river VARCHAR(255), date DATE, ph VARCHAR(10), temp FLOAT, turbidity FLOAT, conductivity FLOAT, polluted INT)''')
    conn.commit()
    conn.close()

# Function to insert data into the oldriverdata table
def insert_data(river, ph, date, temp, turbidity, conductivity, polluted):
    conn = pymysql.connect(host='localhost', user='root', password='K24#2001@jqir#', database='userdata')
    c = conn.cursor()
    c.execute('''INSERT INTO oldriverdata (river, date, ph, temp, turbidity, conductivity, polluted)
                 VALUES (%s, %s, %s, %s, %s, %s, %s)''', (river, date, ph, temp, turbidity, conductivity, polluted))
    conn.commit()
    conn.close()

# Function to manually enter data for 20 rivers
def enter_river_data():
    print("Enter data for 20 rivers:")
    for i in range(20):
        river = input("River {}: ".format(i+1))
        date = input("Enter date for {} (YYYY-MM-DD format): ".format(river))
        ph = input("Enter pH (high/low) for {}: ".format(river))
        temp = float(input("Enter temperature for {} (in Celsius): ".format(river)))
        turbidity = float(input("Enter turbidity for {}: ".format(river)))
        conductivity = float(input("Enter conductivity for {}: ".format(river)))
        polluted = int(input("Is {} polluted: ".format(river)))
        insert_data(river, ph, date, temp, turbidity, conductivity, polluted)

# Main function to create tables, enter data, and display success message
def main():
    create_table()
    enter_river_data()
    print("Data entered successfully.")

if __name__ == "__main__":
    main()
