Here is a targeted interview preparation guide designed for a **GCP DevOps / Cloud Automation Role** at TCS, focused on **Harness, Ansible, GCP, and Infrastructure as Code**.

TCS technical rounds for mid-to-senior levels typically balance **core tool knowledge**, **architectural design**, and **scenario-based troubleshooting**.

---

## 1. Harness CI/CD Platform Questions

Interviews focus heavily on pipeline design, secret management, delegate architecture, and automated rollout strategies.

### **Q1: How does the Harness Delegate architecture work, and how do you handle deployment in restricted or private GCP VPCs?**

* **Expected Answer:**
The Harness Delegate is a lightweight worker process running inside your target infrastructure (e.g., a Pod in GKE or an instance in GCP). It establishes an outbound connection to the Harness Manager (SaaS), pulling execution tasks and performing them locally within the environment. Because connection is strictly outbound (over HTTPS/WSS), there is no need to open inbound firewall ports into private VPCs.

### **Q2: How do Continuous Verification (CV) and auto-rollback work in Harness?**

* **Expected Answer:**
Harness uses machine learning to connect with monitoring and logging tools (e.g., Cloud Monitoring, Datadog, Prometheus) during deployments. It establishes a baseline from prior releases, monitors metrics/logs for anomalies during canary or blue-green rollouts, and triggers an automated rollback (via pre-configured failure strategies) if error rates or latency thresholds are breached.

### **Q3: Explain how you structure Harness Pipelines for multi-stage (Dev -> Staging -> Prod) promotion with governance.**

* **Expected Answer:**
* **Pipelines & Stages:** Define stages for Build, Integration Test, and Deployment using reusable Templates (Pipeline/Stage/Step scale).
* **Environment & Services:** Map deployment targets to specific GCP environments/clusters.
* **Governance & Approvals:** Enforce explicit manual approvals or Jira/ServiceNow integration triggers before Production stages.
* **RBAC & OPA:** Apply Policy-as-Code using Open Policy Agent (OPA) within Harness to block deployments if compliance rules (e.g., unapproved images, missing labels) are violated.



---

## 2. Ansible & Configuration Management Questions

TCS interviewers probe deeply into modular design, performance tuning, dynamic infrastructure inventorying, and state management.

### **Q1: How do you manage dynamic GCP inventories in Ansible, and how do you target specific instance groups?**

* **Expected Answer:**
Instead of static inventory files, use the official GCP inventory plugin (`google.cloud.gcp_compute`).
```yaml
plugin: google.cloud.gcp_compute
projects:
  - my-gcp-project-id
auth_kind: serviceaccount
service_account_file: /path/to/sa_key.json
keyed_groups:
  - key: labels.environment
    prefix: env
  - key: zone
    prefix: zone

```


This automatically groups target VMs dynamically based on GCP tags or labels (e.g., `env_prod`, `zone_us_central1_a`).

### **Q2: What is Idempotency in Ansible, and how do you write a playbook that maintains it when using command/shell modules?**

* **Expected Answer:**
* **Idempotency** means executing a playbook multiple times yields the exact same system state without unintended side effects.
* Native Ansible modules (e.g., `apt`, `copy`, `gcp_compute_instance`) are inherently idempotent.
* For raw `command` or `shell` tasks, idempotency is maintained using parameters like `creates` (skip task if file exists) or `when` checks:
```yaml
- name: Run script only if service is not installed
  ansible.builtin.shell: /tmp/install.sh
  args:
    creates: /usr/bin/installed_binary

```





### **Q3: Explain how you organize enterprise automation using Ansible Roles and Collections.**

* **Expected Answer:**
* **Roles:** Provide a standard directory structure (`tasks/`, `handlers/`, `vars/`, `defaults/`, `templates/`) to encapsulate specific behavior (e.g., hardening OS, installing Nginx).
* **Collections:** Packages that group roles, custom plugins, and modules (e.g., `google.cloud` collection) to distribute cross-team automation cleanly via Ansible Galaxy or Private Automation Hub.



---

## 3. GCP & Infrastructure as Code (IaC) Questions

Expect questions around GCP IAM, networking, container orchestrations, and integrating Terraform/Ansible/Harness together.

### **Q1: How do Terraform, Ansible, and Harness fit together in a complete end-to-end cloud pipeline?**

* **Expected Answer:**
1. **Provisioning (Terraform):** Triggered in CI/CD to spin up underlying GCP infrastructure (VPCs, GKE clusters, Cloud SQL, Compute instances).
2. **Configuration Management (Ansible):** Configures VM-level software, applies OS security patching, and manages internal system settings.
3. **Application Delivery (Harness):** Takes built application artifacts (Docker images, Helm charts), orchestrates canary/blue-green deployments onto GKE/VMs, and manages rollbacks.



### **Q2: How do you securely handle service account credentials and secrets across GCP, Ansible, and Harness?**

* **Expected Answer:**
* **GCP / GKE:** Use **Workload Identity** to map Kubernetes Service Accounts directly to GCP IAM roles, eliminating long-lived service account key files.
* **Harness:** Store sensitive tokens/keys in secret managers (e.g., GCP Secret Manager or Vault) and link them via Harness Secret Manager connectors.
* **Ansible:** Protect internal variables and playbook secrets using **Ansible Vault** (`ansible-vault encrypt`).



### **Q3: What strategy do you use for Blue/Green vs. Canary deployments on Google Kubernetes Engine (GKE)?**

* **Expected Answer:**
* **Blue/Green:** Run two identical production environments side-by-side. Cut traffic over at the Load Balancer / Ingress level once health checks pass.
* **Canary:** Deploy a new version alongside the current one, shifting a small fraction (e.g., 10%) of traffic using Istio/ASM or Ingress controllers, progressively increasing traffic while Harness tracks continuous metrics.



---

## 4. Real-World Scenario & Troubleshooting Questions

### **Scenario A: An Ansible playbook run through a Harness Pipeline fails on 2 out of 20 GCP VM targets mid-execution. How do you handle this safely?**

* **Key Points to Cover:**
* Mention using `max_fail_percentage` or `serial` keywords in Ansible to halt execution before failing the entire fleet.
* Use Ansible `block`, `rescue`, and `always` blocks to catch errors, send alerts, or run cleanup tasks gracefully.
* Explain how Harness handles stage failure strategies (e.g., notify operator, automatically rollback changed states, or run a dedicated failure pipeline).



### **Scenario B: A deployment pipeline succeeds in Harness, but application pods in GKE enter a `CrashLoopBackOff` state. How do you troubleshoot?**

* **Key Points to Cover:**
* Use `kubectl describe pod <pod_name>` to inspect events (Liveness/Readiness probe failures, OOMKilled, volume mount issues).
* Check container logs with `kubectl logs <pod_name> --previous` to analyze application-level stack traces.
* Check GCP Cloud Logging / Cloud Monitoring to verify environment variables, secret mounts, or database connectivity.



---

## Technical Concept Cheat-Sheet

| Tool | Focus Areas to Mention in TCS Interview |
| --- | --- |
| **Harness** | Delegates, Pipeline-as-Code, Continuous Verification, OPA Policies, Secret Manager Integration |
| **Ansible** | Dynamic Inventories (`gcp_compute`), Roles/Collections, Idempotency, Ansible Vault, Handlers |
| **GCP** | GKE, IAM & Workload Identity, Secret Manager, VPCs & Private Google Access, Cloud Monitoring |
| **IaC / K8s** | Terraform State Management, Helm, Istio / Ingress Traffic Splitting |

You hit the core principles right on target for the parts you answered. Let’s break down your responses, validate what you got right, and fill in the missing pieces for a complete interview-grade answer.

---

### Feedback on Scenario 1: Harness Delegate Outage

* **Your Answer:** Add multiple delegates with the same tag and use the tag in place of a specific delegate ID.
* **Evaluation & Gaps:**
* **Spot on for High Availability!** Assigning a shared selector tag (e.g., `gke-prod-delegate`) to a pool of multiple delegate pods ensures that if one pod goes down or restarts, Harness automatically routes tasks to another available delegate in the pool.
* **Missing Triage Steps:** To answer the *troubleshooting* half of the question in an interview, you should mention:
1. **Check Pod Status & Logs:** Run `kubectl describe pod <delegate-pod>` to check for OOMKilled events or CPU/Memory throttling, and `kubectl logs <delegate-pod>` to inspect connection errors with the Harness Manager.
2. **Network/Proxy Outbound Check:** Verify that outbound HTTPS/WSS (port 443) to the Harness Manager or external relays hasn't been blocked by a recent GCP firewall update or VPC Service Controls change.
3. **Delegate Token Expiry:** Check if the account credentials/tokens used by the delegate have expired or been rotated.





---

### Feedback on Scenario 2: Ansible Idempotency & Secrets

* **Your Answer:**
1. Using parameters like `creates` and `when`.
2. Using `no_log: true`.


* **Evaluation & Gaps:**
* **Spot on!**
* For non-idempotent custom tasks (like running shell scripts), using arguments like `creates` or `removes`, or writing custom `when` conditional checks, is the standard way to enforce idempotency. (Ideally, shifting away from raw `command`/`shell` modules to native declarative modules like `template` or `copy` makes idempotency automatic).
* `no_log: true` is the exact Ansible parameter required to mask sensitive strings (like database passwords or API keys) from printing in standard output or CI/CD logs.


* **Tying in GCP Secret Manager:** To make the secret management piece complete, mention using Ansible's built-in GCP lookup plugins or modules (e.g., `google.cloud.gcp_secret_manager_secret` or lookup plugins like `lookup('google.cloud.gcp_secret_manager', 'my-secret', project=...)`) to fetch the password dynamically at runtime rather than hardcoding it in repository variables.



---

### Review of Scenario 3: Zero-Downtime Migration (Terraform, Ansible, and Harness)

Since you skipped this one, here is how a senior engineer maps out this architecture in an interview:

1. **Phase 1: Infrastructure Provisioning (Terraform)**
* Terraform provisions the foundational layer on GCP: VPC subnets, Cloud SQL databases, and the target Google Kubernetes Engine (GKE) clusters, along with IAM roles and Workload Identity bindings.


2. **Phase 2: Configuration & Base Setup (Ansible)**
* Ansible configures any remaining VM-level dependencies (if legacy VMs still exist during transition), sets up cluster-level admission controllers, or provisions shared cluster tools (monitoring agents, ingress controllers) if not handled via Terraform Helm providers.


3. **Phase 3: Application Delivery & Cutover (Harness)**
* Harness manages the application layer. It takes containerized microservices, deploys them to the new GKE cluster, and coordinates traffic shifting (using Canary or Blue/Green strategies) alongside continuous verification (monitoring error rates via Cloud Monitoring) to ensure zero downtime during the cutover from legacy MIGs to GKE.
