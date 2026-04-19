### Create a sample db file
import sqlite3

def create_sample_db():
    conn = sqlite3.connect('./db_files/vault_key.db')
    cursor = conn.cursor()

    # Create a sample table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vaultkeys (
            id INTEGER PRIMARY KEY,
            attribute TEXT NOT NULL,
            key TEXT NOT NULL
        )
    ''')

    # Insert sample data
    keys = [
        (1, 'unseal_Key_1', '********************************************'),
        (2, 'unseal_Key_2', '********************************************'),
        (3, 'unseal_Key_3', '********************************************'),
        (4, 'unseal_Key_4', '********************************************'),
        (5, 'unseal_Key_5', '********************************************'),
        (6, 'root_token', 'hvs.*****************************'),
    ]
    
    cursor.executemany('INSERT INTO vaultkeys VALUES (?,?,?)', keys)
    conn.commit()
    conn.close()
    print("✅ vault_key.db created!")

create_sample_db()