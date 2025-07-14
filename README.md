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

The issue might be due to how the tree structure is being rendered in your repository viewer (e.g., GitHub, GitLab). The horizontal layout in the image suggests that the markdown or tool you're using isn't interpreting the structure as a vertical tree. To ensure a vertical layout, you need to use proper markdown syntax for a directory tree. Here's how to fix it:

Update your `README.md` with the following precise markdown tree structure:

```
Project Structure
```
├── CHATBOT_UI/
│   ├── api/
│   │   ├── app.py
│   │   └── static/
│   │       ├── login.html
│   │       ├── chat.html
│   │       └── script.js
│   ├── chatbot/
│   │   ├── db.py
│   │   ├── llm.py
│   │   ├── session.py
│   │   └── ...
├── .env           # 🔐 MySQL credentials (NOT committed)
├── .gitignore
├── main.py        # CLI version (optional)
├── requirements.txt
└── README.md
```

### Steps to Apply:
1. Replace the existing content in `README.md` with the above code block.
2. Commit and push the changes:
   ```
   git add README.md
   git commit -m "Fix project structure to display vertically"
   git push
   ```

### Notes:
- The triple backticks (```) create a code block, which helps preserve the indentation and display the tree vertically.
- Ensure there are no extra spaces or tabs that might misalign the structure.
- Some Git hosting platforms (like GitHub) render markdown trees correctly if the indentation is consistent (using spaces, typically 2 or 4 per level).

If it still doesn't display vertically, it could be a rendering issue with your specific viewer. Let me know, and I can suggest alternative approaches!

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
