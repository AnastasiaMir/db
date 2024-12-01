import psycopg2


conn = psycopg2.connect(dbname='school', user='postgres', password='1234', host='localhost', port=5433)


sql = "SELECT * FROM teachers;"
cursor = conn.cursor()
# Указатель на набор данных в памяти СУБД
cursor.execute(sql)
for row in cursor:
    print(row)
cursor.close()

conn.commit()
conn.close()