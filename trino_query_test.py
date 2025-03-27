import trino

# Connect to Trino
connection = trino.dbapi.connect(
    host='localhost',
    port=8080,
    user='trino',
    catalog='postgresql',
    schema='public',
)

cursor = connection.cursor()

# Query from PostgreSQL
print("PostgreSQL Data:")
cursor.execute('SELECT * FROM postgresql.public.customers')
rows = cursor.fetchall()
for row in rows:
    print(row)

# Query from MongoDB
print("\nMongoDB Data:")
cursor.execute('SELECT * FROM mongodb.testdb.products')
rows = cursor.fetchall()
for row in rows:
    print(row)

# Cross-database query
print("\nCross-Database Query:")
cursor.execute('''
    SELECT c.name AS customer_name, p.name AS product_name, p.price 
    FROM postgresql.public.customers c, mongodb.testdb.products p
    WHERE c.id = 1
''')
rows = cursor.fetchall()
for row in rows:
    print(row)