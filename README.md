# 🤖 Multi-Purpose Local AI Chatbot

A local AI chatbot built with **Shiny for Python**, **Chatlas**, and **Ollama**. The application provides a simple web interface for chatting with locally installed Large Language Models (LLMs) such as **Llama 3**, **Mistral**, and **Phi-3**.

## Features

* 🖥️ Local AI inference (no cloud API required)
* 🔍 Automatic detection of installed Ollama models
* 🤖 Multiple model selection
* ⚙️ Custom system prompt
* 🎨 Adjustable response creativity
* 💬 Streaming responses
* 🗑️ Clear conversation
* 📱 Responsive Shiny interface

---

## Tech Stack

* Python
* Shiny for Python
* Chatlas
* Ollama
* Open-source LLMs

---

## Prerequisites

Install:

* Python 3.9+
* Ollama

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Beena-Kurian/multi-purpose-local-ai-chatbot.git
cd multi-purpose-local-ai-chatbot
```

### 2. Create a virtual environment

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Python packages

```bash
pip install -r requirements.txt
```

---

## Install Ollama Models

Download one or more models:

```bash
ollama pull llama3
ollama pull mistral
ollama pull phi3
```

Verify installed models:

```bash
ollama list
```

---

## Run the Application

```bash
python -m shiny run --reload --launch-browser app.py
```

Open in browser:

```text
http://127.0.0.1:8000
```

---

## Using the Chatbot

* Select an AI model from the sidebar.
* Customize the system prompt
* Adjust response creativity.
* Start chatting.

---

## Resources

* **Shiny for Python:** https://shiny.posit.co/py/
* **Chatlas Documentation:** https://posit-dev.github.io/chatlas/
* **Ollama:** https://ollama.com/
* **Ollama API:** https://docs.ollama.com/api
* **Ollama Model Library:** https://ollama.com/library

---


## License

This project is released under the MIT License.
