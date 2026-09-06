# Hashicorp Vault Transit Secrets Engine Cheat Sheet

This guide provides practical examples for interacting with the **HashiCorp Vault Transit Secrets Engine (Encryption-as-a-Service)**. It covers encryption, digital signatures, integrity verification, and cryptographic key management.

---

## 🛠️ Prerequisites

Before running these commands, ensure you are logged into your Vault container and the transit engine is enabled:

```bash
# Enter the container terminal
docker exec -it hashicorp_vault sh

# Enable the transit secrets engine
vault secrets enable transit
```

---

## 🔒 1. Data Encryption and Decryption

Vault handles cryptographic operations for applications without storing the actual data or exposing the encryption keys. Data payloads must be **base64 encoded**.

### Setup Key
```bash
vault write -f transit/keys/my-app-key
```

### Encrypt Data
1. Encode your text string to base64:
   ```bash
   echo -n "hello-homelab" | base64
   # Output: aGVsbG8taG9tZWxhYg==
   ```
2. Send to Vault to encrypt:
   ```bash
   vault write transit/encrypt/my-app-key plaintext=aGVsbG8taG9tZWxhYg==
   ```
   *Returns a ciphertext string starting with `vault:v1:...`.*

### Decrypt Data
Send the ciphertext back to Vault to retrieve the original base64 payload:
```bash
vault write transit/decrypt/my-app-key ciphertext="vault:v1:PASTE_CIPHERTEXT_HERE"
```

---

## ✍️ 2. Digital Signing and Verification

Used to verify authenticity. An asymmetric key pairs a private key (held securely inside Vault) with an exportable public key.

### Setup Asymmetric Key
```bash
vault write transit/keys/my-sign-key type=ed25519
```

### Sign Data
1. Encode payload to base64:
   ```bash
   echo -n "secure-config-data" | base64
   # Output: c2VjdXJlLWNvbmZpZy1kYXRh
   ```
2. Sign the data payload (Note: uses the `input` parameter):
   ```bash
   vault write transit/sign/my-sign-key input=c2VjdXJlLWNvbmZpZy1kYXRh
   ```
   *Returns a signature string starting with `vault:v1:...`.*

### Verify Signature
```bash
vault write transit/verify/my-sign-key \
  input=c2VjdXJlLWNvbmZpZy1kYXRh \
  signature="vault:v1:PASTE_SIGNATURE_HERE"
```
*Returns `valid true`. Modifying the input string returns `valid false`.*

---

## 🧮 3. Hashing and HMAC Generation

Used to verify data integrity. HMAC combines a cryptographic hash function with a secret key managed inside Vault to prevent unauthorized hash recalculations.

### Setup HMAC Key
```bash
vault write transit/keys/my-hmac-key type=hmac
```

### Generate HMAC
```bash
vault write transit/hmac/my-hmac-key input=Y29uZmlkZW50aWFsLXBheXJvbGwtZGF0YQ==
```
*Returns an HMAC signature starting with `vault:v1:...`.*

### Verify HMAC
```bash
vault write transit/verify/my-hmac-key \
  input=Y29uZmlkZW50aWFsLXBheXJvbGwtZGF0YQ== \
  hmac="vault:v1:PASTE_HMAC_HERE"
```

### Direct Hashing (Without a key)
To generate a generic SHA-256 fingerprint without a managed key:
```bash
vault write transit/hash input=Y29uZmlkZW50aWFsLXBheXJvbGwtZGF0YQ== format=hex algorithm=sha2-256
```

---

## 🔄 4. Key Generation and Rotation

Vault allows you to rotate underlying cryptographic key material seamlessly. Historical keys are preserved so old ciphertext remains readable.

### Setup Key & View Version
```bash
vault write -f transit/keys/my-rotating-key
vault read transit/keys/my-rotating-key
# Look for: latest_version 1
```

### Rotate Key
Force Vault to upgrade the key material version:
```bash
vault write -f transit/keys/my-rotating-key/rotate
vault read transit/keys/my-rotating-key
# Look for: latest_version 2
```

### Rewrap (Upgrade Old Ciphertext)
To upgrade old data encrypted with version 1 to the newly generated version 2 without exposing plaintext:
```bash
vault write transit/rewrap/my-rotating-key ciphertext="vault:v1:PASTE_OLD_V1_CIPHERTEXT"
```

---
