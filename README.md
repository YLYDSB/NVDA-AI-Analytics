# 📈 NVDA AI Market Analytics Platform

An application designed to track, persist, and analyze NVIDIA (NVDA) market data using local Large Language Models (LLMs).

---

## Highlights

- **Automated Data Pipeline**: Integrated with Alpha Vantage API to fetch real-time market quotes via a custom Python scheduler.
- **Relational Data Persistence**: Utilizes **SQLite** for structured storage of historical price data, enabling time-series analysis.
- **Microservices Architecture**: 
  - **FastAPI Backend**: A high-performance RESTful API with automated Swagger documentation.
  - **Streamlit Frontend**: An interactive dashboard for real-time visualization of price trends and volatility.
- **Privacy-First AI Insights**: Seamlessly integrated with **Ollama (Llama3)** to generate automated market summaries locally, ensuring data remains private and secure.
- **Production-Ready Deployment**: Fully containerized using **Docker** and **Docker Compose** for "one-click" environment setup.

---

## System Architecture

The project follows a modular architecture to ensure scalability and maintainability:

1. **Data Layer**: Managed via `database.py` (SQLite schema & CRUD operations).
2. **Ingestion Layer**: `ingest.py` (API logic) and `scheduler.py` (Automation).
3. **API Layer**: `main.py` (FastAPI endpoints for the frontend and external tools).
4. **Presentation Layer**: `dashboard.py` (Streamlit UI for data visualization).
5. **AI Logic**: Integrated local LLM inference via Ollama's REST API.

---

## Tech Stack

- **Language**: Python 3.11
- **Backend Framework**: FastAPI, Uvicorn
- **Frontend Framework**: Streamlit, Pandas
- **Database**: SQLite3
- **DevOps**: Docker, Docker Compose
- **AI Model**: Ollama (Llama3 / TinyLlama)

---


### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
- [Ollama](https://ollama.com/) installed (ensure `ollama pull llama3` has been executed).

