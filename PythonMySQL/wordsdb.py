#!/usr/bin/env python3
import mysql.connector
import re

#These are parameters for the database connection
conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'adminadmin',
    database = "vocab" # adds connection to the database via the cursor cursor = conn.cursor()
)
cursor = conn.cursor() #This is the cursor that will be used to execute queries
cursor.execute("SHOW DATABASES") #This will create a list of all the databases
found = False
for db in cursor: #This will loop through all the databases
    pattern = "[(,')]" #This is the pattern that will be used to find the database name
    db_string = re.sub(pattern, "", str(db)) #This will remove the parentheses and commas from the database name
    if (db_string == 'vocab'): #This will check if the database name is 'vocab'
        found = True
        print ("Database vocab exists")
if (not found): #This will check if the database name is 'vocab'
    cursor.excecute(" CREATE DATABASE vocab") #This will create the database 'vocab' but not list like "SHOW DATABASES"

sql = "DROP TABLE IF EXISTS vocab_table" #This will drop the table if it exists and the IF EXISTS command will prevent an sql error
cursor.execute(sql)

sql = "CREATE TABLE vocab_table (word VARCHAR(255), definition VARCHAR(255))"
cursor.execute(sql)
fh = open("Vocabulary_list.csv") #This will open the file that contains the vocabulary

wd_list = fh.readlines() #This will read the file and store it in a list

wd_list.pop(0) #This will remove the first element of the list, which is the header

vocab_list = [] #This will create an empty list to store the vocabulary

for rawstring in wd_list: #This will loop through the list
    word, definition = rawstring.split(",", 1) #This will split the string into two parts, the word and the definition
    definition = definition.strip() #This will remove the newline character from the definition
    vocab_list.append({word, definition}) #This will add the word and definition to the list
    sql = "INSERT INTO vocab_table (word, definition) VALUES (%s, %s)" # The %s allows the values to be applied separately from the sql string itself
    values = (word, definition) #This will create a tuple with the word and definition. The tuple will be used to replace the %s in the query
    cursor.execute(sql, values) #This will execute the query, this prevents SQL injection

    conn.commit() #This will commit the changes to the database
    #print("Inserted " + str(cursor.rowcount)+ " row into vocab_table")

sql = "SELECT * FROM vocab_table WHERE word = %s " #This will select all rows from the vocab_table where the word is equal to the word in the values tuple
value = ('boisterous',) #This will create a tuple with the word
cursor.execute(sql, value) #This will execute the query
result = cursor.fetchall() #This will store the result in a list titled result

for row in result:
    print(row)

sql = "UPDATE vocab_table SET definition = %s WHERE word = %s" #This will update the definition of the word 'boisterous' to "spirited; lively"
value  = ("spirited; lively", 'boisterous') #This will create a tuple with the new definition and the word
cursor.execute(sql, value)

conn.commit()
print("Modified row count: ", cursor.rowcount)
sql = "SELECT * FROM vocab_table WHERE word = %s" #This will select all rows from the vocab_table where the word is equal to the word in the values tuple
value = ('boisterous',) #This will create a tuple with the word
cursor.execute(sql, value) #This will execute the query
result = cursor.fetchall() #This will store the result in a list titled result after the query is executed




#print(vocab_list)