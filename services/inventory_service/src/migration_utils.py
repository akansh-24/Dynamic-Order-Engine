# services/inventory_service/src/migration_utils.py
import psycopg2
import os

def run_flyway_migration():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL environment variable not set")

    conn = psycopg2.connect(db_url)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        id SERIAL PRIMARY KEY,
        product_name VARCHAR(255) NOT NULL UNIQUE,
        quantity INT NOT NULL,
        price NUMERIC(10,2) NOT NULL,
        updated_at TIMESTAMP DEFAULT NOW()
    );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("[ok] Migration applied successfully")

