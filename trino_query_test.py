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
print("PostgreSQL Data (Customers):")
cursor.execute('SELECT * FROM postgresql.public.customers')
rows = cursor.fetchall()
for row in rows:
    print(row)

# Query from MongoDB
print("\nMongoDB Data (Users):")
cursor.execute('SELECT * FROM mongodb.testdb.users')
rows = cursor.fetchall()
for row in rows:
    print(row)

# Cross-database query
print("\nCross-Database Query (Product Reviews):")
# Joining PostgreSQL Products with MongoDB Reviews
cursor.execute('''
    SELECT p.name AS product_name, r.rating, r.review_text 
    FROM postgresql.public.products p
    JOIN mongodb.testdb.reviews r ON p.id = r.product_id
''')
rows = cursor.fetchall()
for row in rows:
    print(row)