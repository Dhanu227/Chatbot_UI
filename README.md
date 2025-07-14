# 🧠 AI Chat Assistant (FastAPI + LangChain + Ollama)

This is an AI-powered chatbot web app inspired by ChatGPT. It allows users to register, create sessions, and chat with an AI assistant powered by **LangChain + Ollama** using the **Mistral 7B** model — all running locally and open-source.

---

## 🚀 Features

- 🔐 User registration & login (bcrypt-secured)
- 💬 Multiple chat sessions per user 
- 🧠 AI responses using LangChain + Ollama (Mistral 7B or other models)
- 🗃️ Persistent history stored in MySQL
- 💻 Modern two-page UI (login & chat) with sidebar layout
- 🧩 Works 100% offline — no paid APIs

---

## 🏗️ Tech Stack

| Layer          | Technology             |
|----------------|-------------------------|
| Frontend       | HTML, CSS, JavaScript   |
| Backend        | FastAPI (Python)        |
| AI Model       | LangChain + Ollama      |
| Database       | MySQL + SQLAlchemy ORM  |
| Authentication | Bcrypt                  |
| Server         | Uvicorn (ASGI)          |

---

## 📁 Project Structure

CHATBOT_UI/
├── api/                    # FastAPI app + static frontend
│   ├── app.py
│   └── static/
│       ├── login.html
│       ├── chat.html
│       └── script.js
├── chatbot/                # Core logic: DB, LLM, sessions
│   ├── db.py
│   ├── llm.py
│   ├── session.py
│   └── ...
├── .env                    # 🔐 MySQL credentials (NOT committed)
├── .gitignore
├── main.py                 # CLI version (optional)
├── requirements.txt
└── README.md


## 🛠️ How to Run This Project Locally

1)To run this project locally, first clone the repository and move into the folder using:

```bash
git clone https://github.com/yourusername/chatbot-ui.git
cd chatbot-ui
Next, create a .env file in the root directory of your project and add your MySQL credentials:

2)env
MYSQL_USER=root
MYSQL_PASSWORD=yourpassword
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=your_database_name
Now create a Python virtual environment and activate it:

3)bash
python -m venv venv
venv\Scripts\activate     # Windows
# or
source venv/bin/activate  # macOS/Linux

3)Then install the dependencies:
bash
pip install -r requirements.txt

4)Make sure you have Ollama installed. You can download it from https://ollama.com. Once installed, start the Ollama server in a separate terminal:
bash
ollama serve

Then pull the model you'll be using (e.g., mistral):
bash
ollama pull mistral

5)Now you can start the FastAPI server:
bash
uvicorn api.app:app --reload --port 8080

Finally, open your browser and go to:
http://localhost:8080

6)From here, you can register a new user, log in, create or select sessions from the sidebar, and begin chatting with the AI.
