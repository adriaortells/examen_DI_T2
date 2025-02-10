import sqlite3
import os


class Database:
    def __init__(self, db_name="products.db"):
        self.conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), db_name))
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price TEXT NOT NULL,  -- 🛑 Ha de ser REAL però està com a TEXT per obligar-los a millorar-ho
                category TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def add_product(self, name, price, category):
        self.cursor.execute("INSERT INTO products (name, price, category) VALUES (?, ?, ?)", (name, price, category))
        self.conn.commit()

    def update_product(self, product_id, name, price, category):
        self.cursor.execute("UPDATE products SET name=?, price=?, category=? WHERE id=?", (name, price, category, product_id))
        self.conn.commit()

    def delete_product(self, product_id):
        self.cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
        self.conn.commit()

    def get_products(self):
        self.cursor.execute("SELECT * FROM products")
        return self.cursor.fetchall()