#!/usr/bin/env python3
"""
Data initialization script for Trino demo with MongoDB and PostgreSQL
"""
import pymongo
import psycopg2
from datetime import datetime
import random

def init_postgres():
    """Initialize PostgreSQL with sample data"""
    print("Initializing PostgreSQL...")
    
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="testdb",
        user="user",
        password="password"
    )
    
    # Create a cursor
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
        DROP TABLE IF EXISTS order_items;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS customers;
        
        CREATE TABLE customers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            country VARCHAR(50),
            signup_date DATE NOT NULL
        );
        
        CREATE TABLE products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            category VARCHAR(50) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            in_stock BOOLEAN DEFAULT TRUE
        );
        
        CREATE TABLE orders (
            id SERIAL PRIMARY KEY,
            customer_id INTEGER REFERENCES customers(id),
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(20) NOT NULL
        );
        
        CREATE TABLE order_items (
            id SERIAL PRIMARY KEY,
            order_id INTEGER REFERENCES orders(id),
            product_id INTEGER REFERENCES products(id),
            quantity INTEGER NOT NULL,
            price DECIMAL(10, 2) NOT NULL
        );
    """)
    
    # Insert customer data
    customer_data = [
        ('John Doe', 'john@example.com', 'USA', '2024-01-15'),
        ('Jane Smith', 'jane@example.com', 'Canada', '2024-02-20'),
        ('Bob Johnson', 'bob@example.com', 'UK', '2024-03-05'),
        ('Maria Garcia', 'maria@example.com', 'Spain', '2024-01-28'),
        ('Ahmed Hassan', 'ahmed@example.com', 'Egypt', '2024-02-14'),
        ('Li Wei', 'li@example.com', 'China', '2024-03-10'),
        ('Anna Kowalski', 'anna@example.com', 'Poland', '2024-01-05')
    ]
    
    cursor.executemany(
        "INSERT INTO customers (name, email, country, signup_date) VALUES (%s, %s, %s, %s)",
        customer_data
    )
    
    # Insert product data
    product_data = [
        ('Laptop Pro', 'Electronics', 1299.99, True),
        ('Wireless Headphones', 'Electronics', 149.99, True),
        ('Coffee Maker', 'Kitchen', 79.99, True),
        ('Smart Watch', 'Electronics', 249.99, True),
        ('Blender', 'Kitchen', 59.99, False),
        ('Smartphone X', 'Electronics', 899.99, True),
        ('Desk Lamp', 'Home Goods', 35.99, True),
        ('Yoga Mat', 'Fitness', 29.99, True),
        ('Water Bottle', 'Fitness', 19.99, True),
        ('Bluetooth Speaker', 'Electronics', 89.99, False)
    ]
    
    cursor.executemany(
        "INSERT INTO products (name, category, price, in_stock) VALUES (%s, %s, %s, %s)",
        product_data
    )
    
    # Insert order data
    cursor.execute("SELECT id FROM customers")
    customer_ids = [row[0] for row in cursor.fetchall()]
    
    order_statuses = ['Completed', 'Processing', 'Shipped', 'Cancelled']
    
    order_data = []
    for _ in range(15):
        customer_id = random.choice(customer_ids)
        status = random.choice(order_statuses)
        days_ago = random.randint(1, 60)
        order_date = datetime.now().replace(
            hour=random.randint(9, 17),
            minute=random.randint(0, 59),
            second=random.randint(0, 59)
        ).strftime('%Y-%m-%d %H:%M:%S')
        
        order_data.append((customer_id, order_date, status))
    
    cursor.executemany(
        "INSERT INTO orders (customer_id, order_date, status) VALUES (%s, %s, %s)",
        order_data
    )
    
    # Insert order items
    cursor.execute("SELECT id FROM products")
    product_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT id FROM orders")
    order_ids = [row[0] for row in cursor.fetchall()]
    
    order_items_data = []
    for order_id in order_ids:
        # Each order has 1-4 items
        for _ in range(random.randint(1, 4)):
            product_id = random.choice(product_ids)
            quantity = random.randint(1, 3)
            
            # Get product price
            cursor.execute("SELECT price FROM products WHERE id = %s", (product_id,))
            price = cursor.fetchone()[0]
            
            order_items_data.append((order_id, product_id, quantity, price))
    
    cursor.executemany(
        "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
        order_items_data
    )
    
    # Commit and close
    conn.commit()
    cursor.close()
    conn.close()
    
    print("PostgreSQL initialization complete!")

def init_mongodb():
    """Initialize MongoDB with sample data"""
    print("Initializing MongoDB...")
    
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://root:password@localhost:27017/")
    db = client["testdb"]
    
    # Clear existing collections
    db.users.drop()
    db.reviews.drop()
    db.inventory.drop()
    
    # Create users collection
    users = [
        {
            "user_id": 1,
            "username": "tech_guru",
            "name": "Alex Chen",
            "email": "alex@example.com",
            "age": 28,
            "interests": ["programming", "machine learning", "hiking"],
            "address": {
                "street": "123 Tech Lane",
                "city": "San Francisco",
                "state": "CA",
                "zip": "94105"
            },
            "premium_member": True,
            "joined_date": datetime(2022, 3, 15)
        },
        {
            "user_id": 2,
            "username": "design_star",
            "name": "Sofia Rodriguez",
            "email": "sofia@example.com",
            "age": 34,
            "interests": ["design", "photography", "travel"],
            "address": {
                "street": "456 Creative Ave",
                "city": "New York",
                "state": "NY",
                "zip": "10001"
            },
            "premium_member": True,
            "joined_date": datetime(2021, 7, 22)
        },
        {
            "user_id": 3,
            "username": "music_lover",
            "name": "James Wilson",
            "email": "james@example.com",
            "age": 25,
            "interests": ["music", "concerts", "guitars"],
            "address": {
                "street": "789 Melody Road",
                "city": "Nashville",
                "state": "TN",
                "zip": "37203"
            },
            "premium_member": False,
            "joined_date": datetime(2023, 1, 10)
        },
        {
            "user_id": 4,
            "username": "food_explorer",
            "name": "Aisha Johnson",
            "email": "aisha@example.com",
            "age": 31,
            "interests": ["cooking", "food", "travel", "blogging"],
            "address": {
                "street": "101 Flavor Street",
                "city": "Chicago",
                "state": "IL",
                "zip": "60607"
            },
            "premium_member": True,
            "joined_date": datetime(2022, 11, 5)
        },
        {
            "user_id": 5,
            "username": "fitness_coach",
            "name": "Marcus Brown",
            "email": "marcus@example.com",
            "age": 29,
            "interests": ["fitness", "nutrition", "running"],
            "address": {
                "street": "202 Wellness Way",
                "city": "Los Angeles",
                "state": "CA",
                "zip": "90001"
            },
            "premium_member": False,
            "joined_date": datetime(2023, 4, 18)
        }
    ]
    
    db.users.insert_many(users)
    
    # Create reviews collection
    reviews = [
        {
            "review_id": 1,
            "product_id": 1,  # Laptop Pro
            "user_id": 1,
            "rating": 4.5,
            "review_text": "Great laptop overall. Fast performance and good battery life.",
            "verified_purchase": True,
            "review_date": datetime(2024, 2, 15)
        },
        {
            "review_id": 2,
            "product_id": 2,  # Wireless Headphones
            "user_id": 3,
            "rating": 5.0,
            "review_text": "Excellent sound quality and very comfortable for long periods.",
            "verified_purchase": True,
            "review_date": datetime(2024, 1, 20)
        },
        {
            "review_id": 3,
            "product_id": 3,  # Coffee Maker
            "user_id": 4,
            "rating": 3.5,
            "review_text": "Makes good coffee but a bit loud in operation.",
            "verified_purchase": True,
            "review_date": datetime(2024, 3, 5)
        },
        {
            "review_id": 4,
            "product_id": 6,  # Smartphone X
            "user_id": 2,
            "rating": 4.0,
            "review_text": "Great camera and screen. Battery could be better.",
            "verified_purchase": False,
            "review_date": datetime(2024, 2, 28)
        },
        {
            "review_id": 5,
            "product_id": 8,  # Yoga Mat
            "user_id": 5,
            "rating": 4.8,
            "review_text": "Perfect thickness and very durable. Highly recommend!",
            "verified_purchase": True,
            "review_date": datetime(2024, 1, 10)
        },
        {
            "review_id": 6,
            "product_id": 1,  # Laptop Pro
            "user_id": 2,
            "rating": 4.0,
            "review_text": "Good performance but runs a bit hot under load.",
            "verified_purchase": True,
            "review_date": datetime(2024, 3, 10)
        },
        {
            "review_id": 7,
            "product_id": 5,  # Blender
            "user_id": 4,
            "rating": 2.5,
            "review_text": "Not very powerful and struggles with harder ingredients.",
            "verified_purchase": True,
            "review_date": datetime(2024, 2, 5)
        }
    ]
    
    db.reviews.insert_many(reviews)
    
    # Create inventory collection
    inventory = [
        {
            "warehouse_id": "W001",
            "location": "San Francisco",
            "items": [
                {"product_id": 1, "quantity": 15, "last_updated": datetime(2024, 3, 1)},
                {"product_id": 2, "quantity": 28, "last_updated": datetime(2024, 3, 5)},
                {"product_id": 6, "quantity": 12, "last_updated": datetime(2024, 3, 10)}
            ]
        },
        {
            "warehouse_id": "W002",
            "location": "Chicago",
            "items": [
                {"product_id": 3, "quantity": 8, "last_updated": datetime(2024, 2, 28)},
                {"product_id": 4, "quantity": 20, "last_updated": datetime(2024, 3, 8)},
                {"product_id": 7, "quantity": 35, "last_updated": datetime(2024, 3, 12)}
            ]
        },
        {
            "warehouse_id": "W003",
            "location": "Atlanta",
            "items": [
                {"product_id": 5, "quantity": 0, "last_updated": datetime(2024, 3, 2)},
                {"product_id": 8, "quantity": 42, "last_updated": datetime(2024, 3, 15)},
                {"product_id": 9, "quantity": 56, "last_updated": datetime(2024, 3, 10)}
            ]
        },
        {
            "warehouse_id": "W004",
            "location": "Los Angeles",
            "items": [
                {"product_id": 10, "quantity": 0, "last_updated": datetime(2024, 2, 25)},
                {"product_id": 1, "quantity": 10, "last_updated": datetime(2024, 3, 14)},
                {"product_id": 4, "quantity": 15, "last_updated": datetime(2024, 3, 7)}
            ]
        }
    ]
    
    db.inventory.insert_many(inventory)
    
    client.close()
    print("MongoDB initialization complete!")

if __name__ == "__main__":
    print("Starting data initialization...")
    init_postgres()
    init_mongodb()
    print("Data initialization complete!")
