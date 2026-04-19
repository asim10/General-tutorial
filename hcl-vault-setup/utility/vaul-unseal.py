import requests
import sqlite3

def get_vault_keys():
    conn = sqlite3.connect('./db_files/vault_key.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    QUERY = f"SELECT key from vaultkeys WHERE attribute like '%unseal%'"
    cursor.execute(QUERY)
    rows = cursor.fetchall()
    conn.close()

    # Convert to a list of strings
    unseal_keys = [row['key'] for row in rows]

    return unseal_keys



VAULT_ADDR = "https://127.0.0.1:8200"
CA_CERT = "/opt/homelab/ssl/ca.crt"  
UNSEAL_KEYS = get_vault_keys()

def check_status():
    url = f"{VAULT_ADDR}/v1/sys/health"
    try:
        r = requests.get(url, verify=CA_CERT)
        print(f"[INFO] Status Code: {r.status_code}")
    except requests.exceptions.SSLError as e:
        print(f"[ERROR] SSL Error: {e}")
    except Exception as e:
        print(f"[ERROR] Error: {e}")


def is_sealed():
    url = f"{VAULT_ADDR}/v1/sys/seal-status"
    r = requests.get(url, verify=CA_CERT)
    return r.json().get("sealed", True)


def unseal_vault():
    url = f"{VAULT_ADDR}/v1/sys/unseal"

    for key in UNSEAL_KEYS:
        r = requests.put(url, json={"key": key}, verify=CA_CERT)
        data = r.json()

        print(f"[INFO] Progress: {data.get('progress')}/{data.get('t')}")

        if not data.get("sealed"):
            print("[INFO] Vault successfully unsealed 🎉")
            return

    print("Vault is still sealed.")


if __name__ == "__main__":
    check_status()

    if is_sealed():
        print("[INFO] Attempting to unseal Vault...")
        unseal_vault()
    else:
        print("[INFO] Vault is already unsealed.")