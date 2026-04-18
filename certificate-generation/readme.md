# 🔐 Self-Signed Certificate Generation Guide

This guide walks you through creating your own Certificate Authority (CA), and issuing server and client certificates using `openssl`.

---

## 📌 Prerequisites

- OpenSSL installed (`openssl version` to verify)
- Basic terminal access (Linux/macOS/WSL)

---

## 🏗️ 1. Generate Certificate Authority (CA)

### 🔑 Generate CA Private Key
```bash
openssl genrsa -out ca.key 2048
````

### 📜 Create CA Certificate (Valid for 10 Years)

```bash
openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 -out ca.crt \
  -subj "/CN=My-Local-CA"
```

---

## 🖥️ 2. Configure Server Certificate

### ⚙️ Create Configuration File (`server.conf`)

```ini
[req]
distinguished_name = req_distinguished_name
x509_extentions = v3_req
prompt = no

[req_distinguished_name]
CN = homelab-server

[v3_req]
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
DNS.2 = homelab
IP.1 = 127.0.0.1
IP.2 = 192.168.1.77
IP.3 = 192.168.29.77
IP.4 = 192.168.1.37
IP.5 = 192.168.1.97
IP.6 = 192.168.1.87
IP.7 = 192.168.1.67
```

---

## 🔐 3. Generate Server Certificate

### 🔑 Generate Server Private Key

```bash
openssl genrsa -out server.key 2048
```

### 📄 Generate Certificate Signing Request (CSR)

```bash
openssl req -new -key server.key -out server.csr -config server.conf
```

### ✅ Sign Server Certificate with CA

```bash
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key \
  -CAcreateserial -out server.crt -days 365 -sha256 \
  -extfile server.conf -extensions v3_req
```

---

## 👤 4. Generate Client Certificate

### 🔑 Generate Client Private Key

```bash
openssl genrsa -out client.key 2048
```

### 📄 Generate Client CSR

```bash
openssl req -new -key client.key -out client.csr \
  -subj "/CN=homelab-client"
```

### ✅ Sign Client Certificate with CA

```bash
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key \
  -CAcreateserial -out client.crt -days 365 -sha256
```

---

## 📂 Output Files Summary

| File         | Description                |
| ------------ | -------------------------- |
| `ca.key`     | CA private key             |
| `ca.crt`     | CA root certificate        |
| `server.key` | Server private key         |
| `server.csr` | Server certificate request |
| `server.crt` | Signed server certificate  |
| `client.key` | Client private key         |
| `client.csr` | Client certificate request |
| `client.crt` | Signed client certificate  |

---

## ⚠️ Notes

* Keep all `.key` files secure and never share them.
* Add `ca.crt` to trusted root certificates on client systems.
* Update IPs and DNS entries in `server.conf` based on your environment.
* Certificates here are for development or internal use only.

---

## 🚀 You're Ready!

You now have a working self-signed CA and issued certificates for both server and client authentication.
