import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('student.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()


## create the table
table_info="""
create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),
SECTION VARCHAR(25),MARKS INT)
"""

# Execute the table creation command
cursor.execute(table_info)

# Commit the changes to the database
cursor.execute("insert into STUDENT values ('John', 'DATA SCIENCE', 'A', 85)")
cursor.execute("insert into STUDENT values ('Jane', 'DATA SCIENCE', 'B', 90)")
cursor.execute("insert into STUDENT values ('Doe', 'DATA SCIENCE', 'C', 95)")
cursor.execute("insert into STUDENT values ('Alice', 'DEVOPS', 'A', 80)")
cursor.execute("insert into STUDENT values ('Bob', 'DEVOPS', 'B', 88)")

#display all the records
print("All records in STUDENT table:")
data = cursor.execute("SELECT * FROM STUDENT")

for row in data:
    print(row)

# Commit the changes to the database
conn.commit()
conn.close()

