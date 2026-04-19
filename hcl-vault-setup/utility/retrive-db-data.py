import sqlite3

conn = sqlite3.connect('./db_files/vault_key.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

QUERY = f"SELECT key from vaultkeys WHERE attribute like '%unseal%'"

cursor.execute(QUERY)
rows = cursor.fetchall()
conn.close()

# Convert to a list of strings
unseal_keys = [row['key'] for row in rows]

print(unseal_keys)
