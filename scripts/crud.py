import sqlite3

conn = sqlite3.connect("../data/grocery.db")
cursor = conn.cursor()


def create_tables():
    cursor.execute('''
        CREATE TABLE IF NOT EXIST products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXIST prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            store TEXT,
            price REAL,
            date TEXT,
            FOREIGN KEY (product_id) REFERENCES product(id)  
        )
    ''')
    conn.commit()

def add_product(name):
    cursor.execute("INSERT INTO products (name) VALUES (?,?)", (name))
    conn.commit()
    
def add_price(product_id, store, price, date):
    cursor.execute("INSERT INTO prices (product_id, store, price, date) VALUES (?, ?, ?, ?)",
                   (product_id, store, price, date))
    conn.commit()
    
def get_all_products():
    cursor.execute("SELECT * FROM products")
    return cursor.fetchall()

def get_prices_for_product(product_name):
    cursor.execute('''
        SELECT products.name, prices.store, prices.price, prices.date
        FROM prices
        JOIN products ON prices.product_id = products.id
        WHERE products.name = ?
        ORDER BY prices.date
    ''', (product_name,))
    return cursor.fetchall()

def update_product_name(product_id, new_name):
    cursor.execute("UPDATE products SET name = ? WHERE id = ?", (new_name, product_id))
    conn.commit()

def delete_product(product_id):
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()

def delete_old_prices(before_date):
    cursor.execute("DELETE FROM prices WHERE date < ?", (before_date,))
    conn.commit()




