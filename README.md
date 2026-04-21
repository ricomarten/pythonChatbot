# 🤖 Local AI Chatbot Interface (Ollama-based)

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org)
[![Flask Framework](https://img.shields.io/badge/framework-Flask-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Ollama](https://img.shields.io/badge/AI_Engine-Ollama-orange.svg)](https://ollama.com/)

Aplikasi Chatbot AI berbasis web yang berjalan sepenuhnya secara **offline** di infrastruktur lokal. Dirancang untuk keamanan data tinggi, khususnya untuk kebutuhan audit IT dan SQA tanpa ketergantungan pada API pihak ketiga.

## ✨ Fitur Utama
- **Privasi Penuh:** Data tidak pernah keluar dari mesin lokal (Localhost).
- **Model Selector:** Berpindah antar model AI (DeepSeek, Llama, Mistral) secara real-time.
- **Streamlit-like UI:** Antarmuka bersih menggunakan Tailwind CSS.
- **Audit-Ready:** Log aktivitas tercatat di terminal untuk kebutuhan debugging/QA.

## 🏗️ Arsitektur Sistem
Aplikasi ini menghubungkan frontend Flask ke engine Ollama melalui API lokal.



## 🚀 Panduan Instalasi

1. Prasyarat
- Pastikan [Ollama](https://ollama.com/) sudah terinstal di macOS/Windows/Linux.
- Download model yang diinginkan melalui terminal:
  ```bash
  ollama pull deepseek-r1:7b
  ollama pull llama3.2

2. Instalasi Library
Bash
pip install flask ollama
3. Jalankan Aplikasi
Simpan kode Python di bawah sebagai app.py.

Jalankan: python app.py.

Akses di browser: http://127.0.0.1:5000.