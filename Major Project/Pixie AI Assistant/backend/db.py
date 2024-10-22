import csv
import sqlite3

connection = sqlite3.connect("pixie.db")
cursor = connection.cursor()

#query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key,name VARCHAR(100),path VARCHAR(1000))"
#cursor.execute(query)

#query = "INSERT INTO sys_command VALUES (null,'vs code','C:\\Users\\kumar\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe')"
#cursor.execute(query)
#connection.commit()

#create table for adding webapp path for commands
#query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key,name VARCHAR(100),url VARCHAR(1000))"
#cursor.execute(query)

#query = "INSERT INTO web_command VALUES(null,'canva','https://www.canva.com/')"
#cursor.execute(query)
#connection.commit()

#testing module
#app_name = "sticky notes"
#cursor.execute('SELECT path from sys_command WHERE name IN(?)',(app_name,))
#results = cursor.fetchall()
#print(results[0][0])

#create table for contacts
#cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key,name VARCHAR(150),contact_no VARCHAR(100),email VARCHAR(300) NULL)''')

# Specify the column indices you want to import (0-based index)
# Example: Importing the 1st and 31th columns
#desired_columns_indices = [0, 20]

# Read data from CSV and insert into SQLite table for the desired columns
#with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#    csvreader = csv.reader(csvfile)
#    for row in csvreader:
#        selected_data = [row[i] for i in desired_columns_indices]
#        cursor.execute(''' INSERT INTO contacts (id, 'name', 'contact_no') VALUES (null, ?, ?);''', tuple(selected_data))

# Commit changes and close connection
#connection.commit()
#connection.close()