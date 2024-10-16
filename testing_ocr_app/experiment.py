import sqlite3

## connect to sqllite
connection=sqlite3.connect("cheques_psudo.db")

##create a cursor object to insert record,create table
cursor=connection.cursor()

## create the table
table_info="""
CREATE TABLE TRANSACTIONS (
    BANK_NAME VARCHAR(30) NOT NULL,
    AMOUNT DECIMAL(10, 2) DEFAULT 0.0,
    ACCOUNT_NUMBER INT,
    DATE DATE NOT NULL
)
"""

cursor.execute(table_info)

# Insert records into the TRANSACTION table
cursor.execute('''INSERT INTO TRANSACTIONS VALUES('Sampath Bank', 2500.50, 123456789, '2024-10-15')''')
cursor.execute('''INSERT INTO TRANSACTIONS VALUES('Bank of Ceylon', 125.75, 987654321, '2024-10-14')''')
cursor.execute('''INSERT INTO TRANSACTIONS VALUES('Peoples Bank', 800.00, 112233445, '2024-10-13')''')
cursor.execute('''INSERT INTO TRANSACTIONS VALUES('HSBC', 1500.25, 998877665, '2024-10-12')''')
cursor.execute('''INSERT INTO TRANSACTIONS VALUES('NSB', 300.00, 554433221, '2024-10-11')''')

## Display all the records
print("The inserted records are")
data=cursor.execute('''Select * from TRANSACTIONS''')
for row in data:
    print(row)

## Commit your changes in the database
connection.commit()
connection.close()
