# 🚀 Speckitplus Hackathon II - Phase 5: Cloud Native Production

![Status](https://img.shields.io/badge/Status-Completed-success)
![Phase](https://img.shields.io/badge/Phase-5_Cloud_Deployment-blue)
![Stack](https://img.shields.io/badge/Next.js-FastAPI-Docker-green)

## 📌 Overview
**Phase 5** marks the transition from a local development environment to a **Live Production Architecture**.

In this final phase, the **Todo App** evolved from a local Kubernetes cluster (Minikube) to a globally distributed, serverless cloud application. The focus was on **Production Readiness**, **Security Hardening**, and **Performance Optimization**.

---

## 🌐 Live Deployments
| Service | Provider | Status | URL |
| :--- | :--- | :--- | :--- |
| **Frontend** | **Vercel** (Edge Network) | 🟢 Live | [Click Here](https://speckitplus-hackathon-2.vercel.app/) |
| **Backend** | **Hugging Face Spaces** (Docker) | 🟢 Live | [Click Here](https://huzaifa48-hackathon-2-todo-app.hf.space/docs) |
| **Database** | **Neon** (Serverless Postgres) | 🟢 Live | *Private Connection* |

---

## ⚡ Phase 5: Key Achievements

### 1. Cloud-Native Deployment
* **Frontend on Vercel:** Deployed the Next.js 16 application to Vercel's Global Edge Network for sub-100ms latency worldwide.
* **Backend on Hugging Face:** Containerized the FastAPI backend using **Docker** and deployed it to Hugging Face Spaces as a permanent cloud microservice.
* **Zero-Config Scaling:** Both services are configured to scale automatically based on traffic demand (Serverless).

### 2. Advanced Performance Optimization
* **Docker Multi-Stage Builds:** Refactored the `Dockerfile` to use multi-stage builds.
    * *Result:* Reduced Backend image size by **60%**, ensuring faster cold starts and lower bandwidth usage.
* **Asynchronous Concurrency:** Fully refactored all Database and AI API calls to use Python's `async/await`.
    * *Result:* The server can handle **100+ concurrent requests** without blocking, critical for AI-heavy workloads.
* **Database Connection Pooling:** Implemented **SQLAlchemy Connection Pooling** with Neon DB to efficiently manage connections in a serverless environment.

### 3. Security Hardening
* **Strict CORS Policy:** configured Cross-Origin Resource Sharing to allow requests *only* from the production Vercel frontend, preventing unauthorized API access.
* **Environment Secret Management:** Migrated all sensitive keys (Gemini API, DB URL, Secret Keys) from local `.env` files to encrypted **Cloud Environment Variables**.

---

## 🛠 Tech Stack

### **Frontend (Client)**
* **Framework:** Next.js 16 (App Router)
* **Language:** TypeScript
* **Styling:** Tailwind CSS + Shadcn UI
* **State Management:** React Query (TanStack)

### **Backend (Server)**
* **Framework:** FastAPI (Python 3.12)
* **Database ORM:** SQLModel (SQLAlchemy + Pydantic)
* **AI Engine:** Google Gemini 2.5 Flash via OpenAI Agents SDK
* **Authentication:** Better-Auth + JWT

### **DevOps & Infrastructure**
* **Containerization:** Docker
* **Orchestration:** Kubernetes (Minikube for Dev)
* **Cloud Hosting:** Vercel & Hugging Face Spaces
* **Database:** Neon Tech (Serverless PostgreSQL)

---

## 🏃‍♂️ How to Run Locally (Dev Mode)

If you want to run the production code on your local machine:

### 1. Clone the Repository
```bash
git clone [https://github.com/Huzaifa206/Speckitplus-Hackathon-2.git](https://github.com/Huzaifa206/Speckitplus-Hackathon-2.git)
cd Speckitplus-Hackathon-2