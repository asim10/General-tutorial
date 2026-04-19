# Hashi Vault setup documentation

This guide walks you through setting up your own hashi vault using `docker` with ssl enabled.

---

## 📌 Prerequisites
* Docker installed
* Python installed (libraries `requests` `sqlite3`)
* Basic terminal access (Linux/macOS/WSL)

---

## ⚙️ Setup the Vault Configuration

### Create the vault config
```hcl
# /opt/data/docker/hsvault/config/config.hcl
storage "file" {
  path = "/vault/file"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  
  # Enable TLS
  tls_disable = 0
  tls_cert_file = "/vault/config/vault.crt"
  tls_key_file  = "/vault/config/vault.key"
  
  # This allows Vault to request the client certificate for Auth
  tls_disable_client_certs = "false"
}

api_addr = "https://127.0.0.1:8200"
cluster_addr = "https://127.0.0.1:8201"
ui = true
```
### ⚠️ Notes
* Since your entrypoint looks for /vault/config/config.hcl, you need to create this file on your host machine at /opt/data/docker/hsvault/config/config.hcl.
* Important: You must also copy your vault.crt and vault.key into that same directory so Vault can access them.
---

## Setup the docker container

### Create docker-compose file
```yaml
# docker-compose.yaml
services:
  vault:
    container_name: hashicorp_vault
    image: hashicorp/vault:1.17
    ports:
      - "8200:8200"
      - "8201:8201"
    environment:
      # Change http to https
      VAULT_ADDR: "https://127.0.0.1:8200"
      # Point to the CA so the Vault CLI inside the container trusts itself
      VAULT_CACERT: "/vault/config/ca.crt"
    cap_add:
      - IPC_LOCK
    volumes:
      - /opt/data/docker/hsvault/data:/vault/data:rw
      - /opt/data/docker/hsvault/file:/vault/file:rw
      - /opt/data/docker/hsvault/config:/vault/config:rw
    entrypoint: vault server -config /vault/config/config.hcl
    restart: always
```
### Start the Container

```bash
docker compose up -d #RHEL
docker-compose up -d #Debian
```
---

## Configure Vault

### Download vault client in the host
```bash
curl -O https://releases.hashicorp.com/vault/1.20.0/vault_1.20.0_linux_amd64.zip
unzip vault_1.20.0_linux_amd64.zip
sudo mv vault /usr/local/bin/
# Run below command to validate vault
vault version
# Output should be like this - Vault v1.20.0 (6fdd6b59e97d97a9e19b0fb5304bf879c190295e), built 2025-06-23T10:21:30Z
```

### Setup vault profile
```bash
echo 'export VAULT_ADDR="https://localhost:8200"' >> ~/.bash_profile
echo 'export VAULT_CACERT="/opt/homelab/ssl/ca.crt"' >> ~/.bash_profile
source ~/.bash_profile
```

### Initialize the vault
```bash
vault operator init
# This command will provide the unseal keys and root token, keep it somewhere safe
```

### Unseal the Vault
---
#### Using unseal keys retried earlier
```bash
vault operator unseal <key_share>
# You must repeat this command until the Unseal Progress threshold (e.g., 3/5) is met.
vault status # To check the vault status
```
#### Using automated script
---
##### Create a sqlite db using python to store the keys
```python
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
```

##### Create a python script to unseal the vault
```python
# vault-unseal.py
import requests
import sqlite3
import time

def get_vault_keys():
    conn = sqlite3.connect('/opt/homelab/utilities/vault/utility/db_files/vault_key.db')
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

def check_status(attempt=1, max_attempts=5):
    url = f"{VAULT_ADDR}/v1/sys/health"
    try:
        r = requests.get(url, verify=CA_CERT)
        if r.status_code == 200:
            print("[INFO] Vault is initialized and unsealed ✅")
        elif r.status_code == 429:
            print("[INFO] Vault is unsealed but in standby mode ⚠️")
        elif r.status_code == 472:
            print("[INFO] Vault is sealed 🔒")
        elif r.status_code == 501:
            print("[WARN] Vault is not initialized ❌")
        elif r.status_code == 503:
            print("[WARN] Vault is sealed 🔒")
        else:
            print(f"[WARN] Unknown status: {r.status_code}")
    except requests.exceptions.ConnectionError as e:
        print(f"[ERROR] Attempt {attempt}: Connection refused ❌")

        if attempt >= max_attempts:
            print("Max attempts reached.")
            raise

        time.sleep(5)
        return check_status(attempt + 1, max_attempts)
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

        print(f"[INFO] Progress: {data.get('progress')}/{data.get('t')} ⌛")

        if not data.get("sealed"):
            print("[INFO] Vault successfully unsealed 🎉")
            return

    print("Vault is still sealed.")


if __name__ == "__main__":
    check_status()

    if is_sealed():
        print("[INFO] Attempting to unseal Vault... 🏃")
        unseal_vault()
    else:
        print("[INFO] Vault is already unsealed ✅")
        
```
##### Schedule the script in `crontab` to start at reboot of the host
```bash
crontab -e

# Vault unseal
@reboot python /opt/homelab/utilities/vault/utility/vault-unseal.py >> /opt/homelab/utilities/logs/vault-unseal.log
```
---

### Login to Vault
```bash
vault login <your-root-token>
```

### Enable the certificate auth method
```bash
vault auth enable cert
```

### Create a Named Role with CA Cert registration.
```bash
# Any cert signed by this CA can now attempt login. This links your ca.crt to a specific policy. We will use the default policy for now, but in production, you’d create a specific one.
vault write auth/cert/certs/homelab-role \
    certificate=@/opt/homelab/ssl/ca.crt \
    display_name="homelab-client" \
    policies="default" \
    token_ttl=1h \
    token_max_ttl=4h
# tokens will have a validity of 1 hour/ 3600 seconds
```

### Generate the Runtime Token

```bash
# Using cUrl
curl --request POST \
    --cacert /opt/homelab/ssl/ca.crt \
    --cert /opt/homelab/ssl/client.crt \
    --key /opt/homelab/ssl/client.key \
    --data '{"name": "homelab-role"}' \
    https://127.0.0.1:8200/v1/auth/cert/login

# Using vault CLI
vault login -method=cert \
    -client-cert=certs/client.crt \
    -client-key=certs/client.key \
    name=homelab-role
```

### Create a new policy
```bash
cat <<EOF > homelab-policy.hcl
path "secret/*" {
  capabilities = ["read", "list"]
}

path "secret/policy/*" {
  capabilities = ["read", "list"]
}

path "secret/policy/homelab-internal/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}
EOF

# apply the policy
vault policy write homelab-policy homelab-policy.hcl
```

### Apply the policy to the previously created role
```bash
vault write auth/cert/certs/homelab-role \
    certificate=@/opt/homelab/ssl/ca.crt \
    display_name="homelab-client" \
    policies="default,homelab-policy" \
    token_ttl=1h \
    token_max_ttl=4h
```
---
## Create Utility

### Generate Vault token
```bash
# get-vault-token.sh 
#!/bin/bash

COMMON_SSL_DIR='/opt/homelab/ssl'
VAULT_URL="https://localhost:8200"

while [[ -z ${VAULT_TOKEN} ]] || [[ ${VAULT_TOKEN} == "null" ]]; do
  VAULT_TOKEN=$(curl -sk -X POST --cert ${COMMON_SSL_DIR}/vault_client.crt --key ${COMMON_SSL_DIR}/vault_client.key ${VAULT_URL}/v1/auth/cert/login | jq -r '.auth.client_token')
  if [[ -z ${VAULT_TOKEN} ]] || [[ ${VAULT_TOKEN} == "null" ]]; then sleep 2; fi
done

echo ${VAULT_TOKEN}
```

### Create secrets
```bash
# create-vault-secret.sh

#!/bin/bash

alias=$1
key=$2
value=$3
last_updated_time=$(date +%s%3N)

CA_CERT='/opt/homelab/ssl/ca.crt'
export VAULT_TOKEN=$(/opt/homelab/ansible_project/scripts/get-vault-token.sh)
export VAULT_URL="https://localhost:8200"

# Construct JSON payload safely
# Note: Using double quotes for the whole string so variables expand
PAYLOAD=$(cat <<EOF
{
  "alias": "$alias",
  "key": "$key",
  "value": "$value",
  "lastupdatedtime": "$last_updated_time"
}
EOF
)

# Create vault entry (Added /data/ to path for KV-V2)
curl --cacert "$CA_CERT" \
     --header "X-Vault-Token: $VAULT_TOKEN" \
     --request POST \
     --data "$PAYLOAD" \
     "${VAULT_URL}/v1/secret/policy/homelab-internal/${alias}"

# Revoke token
curl --cacert "${CA_CERT}" \
     -H "X-Vault-Token: $VAULT_TOKEN" \
     -X POST "${VAULT_URL}/v1/auth/token/revoke-self"

# Clear Vault token
export VAULT_TOKEN=""
```

### Retrive vault secret
```bash
# get-vault-secret.sh

#!/bin/bash

alias=$1

CA_CERT='/opt/homelab/ssl/ca.crt'
export VAULT_TOKEN=$(/opt/homelab/ansible_project/scripts/get-vault-token.sh)
export VAULT_URL="https://localhost:8200"

# Create vault entry (Added /data/ to path for KV-V2)
curl -s --cacert "$CA_CERT" \
     --header "X-Vault-Token: $VAULT_TOKEN" \
     --request GET \
     "${VAULT_URL}/v1/secret/policy/homelab-internal/${alias}" | jq

# Revoke token
curl --cacert "${CA_CERT}" \
     -H "X-Vault-Token: $VAULT_TOKEN" \
     -X POST "${VAULT_URL}/v1/auth/token/revoke-self"

# Clear Vault token
export VAULT_TOKEN=""
```