import psycopg2


connection = psycopg2.connect(
    host="mydb-instance-1.c9s8f3j7z5y8.us-west-2.rds.amazonaws.com",  
    user="sdeabhi",  
    password="J8k2k8#bP9q9z$5h",  
    dbname="prod",  
    port="5432"
)

cursor = connection.cursor()

cursor.execute("SELECT * FROM your_table;")

result = cursor.fetchall()
print(result)

cursor.close()
connection.close()