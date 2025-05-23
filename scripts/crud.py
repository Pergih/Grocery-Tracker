import sqlite3

conn = sqlite3.connect("data/grocery.db")
cursor = conn.cursor()


def create_tables():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS canonical_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS brands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scraped_name TEXT,
            brand_id INTEGER,
            canonical_id INTEGER,
            url TEXT,
            FOREIGN KEY (brand_id) REFERENCES brands(id),
            FOREIGN KEY (canonical_id) REFERENCES canonical_products(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            price REAL,
            unit TEXT,
            date TEXT,
            FOREIGN KEY (product_id) REFERENCES product(id)  
        )
    ''')
    conn.commit()

# === ADD and CREATE ===

def add_canonical_product(name):
    cursor.execute("INSERT OR IGNORE INTO canonical_products (name) VALUES (?)", (name,))
    conn.commit()
    
    cursor.execute("SELECT id FROM canonical_products WHERE name = ?", (name,))
    return cursor.fetchone()[0]
    
def add_brand(name):
    cursor.execute("INSERT OR IGNORE INTO brands (name) VALUES (?)", (name,))
    conn.commit()
    
    cursor.execute("SELECT id FROM brands WHERE name = ?", (name,))
    return cursor.fetchone()[0]
    
def add_product(scraped_name, brand_id, canonical_id, url):
    cursor.execute("INSERT OR IGNORE INTO products (scraped_name, brand_id, canonical_id, url) VALUES (?, ?, ?, ?)", 
                   (scraped_name, brand_id, canonical_id, url))
    conn.commit()
    
    cursor.execute('''
        SELECT id FROM products
        WHERE scraped_name = ? AND brand_id = ? AND canonical_id = ? AND url = ?
    ''', (scraped_name, brand_id, canonical_id, url))
    return cursor.fetchone()[0]
    
def add_price(product_id, price, unit, date):
    cursor.execute(
        "INSERT INTO prices (product_id, price, unit, date) VALUES (?, ?, ?, ?)",
        (product_id, price, unit, date)
    )
    conn.commit()

# === READS / GET ===
    
def get_all_brands():
    cursor.execute("SELECT * FROM brands")
    return cursor.fetchall()
    
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

# === UPDATE ===

def update_product_name(product_id, new_name):
    cursor.execute("UPDATE products SET name = ? WHERE id = ?", (new_name, product_id))
    conn.commit()

# === DELETE ===

def delete_product(product_id):
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()

def delete_old_prices(before_date):
    cursor.execute("DELETE FROM prices WHERE date < ?", (before_date,))
    conn.commit()

