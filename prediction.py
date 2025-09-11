
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pymysql
import matplotlib.pyplot as plt
import seaborn as sns

# Function to insert predicted pH into the database
def insert_predicted_ph(river_name, predicted_ph):
    try:
        # Establish connection to the database
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='K24#2001@jqir#',
                                     database='userdata')
        cursor = connection.cursor()

        # Insert predicted pH along with river name into the 'predictedph' table
        insert_query = "INSERT INTO predictedph (river, predictedph) VALUES (%s, %s)"
        data = (river_name, predicted_ph)
        cursor.execute(insert_query, data)

        # Commit changes and close connection
        connection.commit()
        connection.close()

        print("Predicted pH value inserted into the database successfully.")

    except pymysql.Error as e:
        print("Error inserting predicted pH into the database:", e)

# Connect to the database
connection_old = pymysql.connect(host='localhost',
                                 user='root',
                                 password='K24#2001@jqir#',
                                 database='userdata')

connection_new = pymysql.connect(host='localhost',
                                 user='root',
                                 password='K24#2001@jqir#',
                                 database='userdata')

# Read data from the database
oldriverdata = pd.read_sql('SELECT * FROM oldriverdata', connection_old)
riverdata = pd.read_sql('SELECT * FROM riverdata', connection_new)

# Concatenate the dataframes
combined_data = pd.concat([oldriverdata, riverdata])

# Perform data preprocessing if needed
# For simplicity, let's assume there are no missing values and all columns are numeric.

# Split the data into features (X) and target (y)
X = combined_data[['temp', 'turbidity', 'conductivity']]  # Features: temperature, turbidity, conductivity
y = combined_data['ph']  # Target: pH level

# Train the model
model = LinearRegression()
model.fit(X, y)

# Make predictions on new data if needed
# For example, you can predict the pH level for a new set of features
new_data = pd.DataFrame({'temp': [25.0], 'turbidity': [105], 'conductivity': [495]})
predicted_ph = model.predict(new_data)[0]

# Define a threshold value
# Define the range-based threshold
lower_threshold = 6.5
upper_threshold = 7.5

# Classify the predicted pH value
predicted_label = 'Safe' if lower_threshold <= predicted_ph <= upper_threshold else 'Polluted'

# Print the predicted label
print("Predicted pH label for new data:", predicted_label)

# Get the river name from the riverdata table
river_name_query = "SELECT river FROM riverdata"
cursor = connection_new.cursor()
cursor.execute(river_name_query)
river_name = cursor.fetchone()[0]

# Insert the predicted pH along with the river name into the database
insert_predicted_ph(river_name, predicted_ph)
