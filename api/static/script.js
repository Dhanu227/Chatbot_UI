let userId = localStorage.getItem("user_id");
let sessionId = null;

if (!userId && window.location.pathname.includes("chat.html")) {
  window.location.href = "/static/login.html";
}

async function loadSessions() {
  const res = await fetch(`/sessions/${userId}`);
  const data = await res.json();
  const list = document.getElementById('session-list');
  list.innerHTML = "";

  data.forEach((s, index) => {
    const div = document.createElement('div');
    div.className = 'session-item' + (index === 0 ? ' active' : '');
    div.textContent = s.title;
    div.dataset.id = s.id;
    div.onclick = () => {
      sessionId = s.id;
      document.querySelectorAll(".session-item").forEach(e => e.classList.remove("active"));
      div.classList.add("active");
      document.getElementById("active-session-title").textContent = s.title;
      loadHistory();
    };
    list.appendChild(div);

    if (index === 0) {
      sessionId = s.id;
      document.getElementById("active-session-title").textContent = s.title;
      loadHistory();
    }
  });
}

async function createSession() {
  const res = await fetch('/new_session', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: userId })
  });

  const data = await res.json();
  if (res.ok) {
    sessionId = data.session_id;
    loadSessions();
  }
}

async function loadHistory() {
  const res = await fetch(`/session-messages/${userId}/${sessionId}`);
  const data = await res.json();
  const chatBox = document.getElementById('chat-box');
  chatBox.innerHTML = "";

  data.forEach(msg => appendMessage(msg.role, msg.content));
}

async function sendMessage() {
  const input = document.getElementById('user-input');
  const message = input.value.trim();
  if (!message || !sessionId || !userId) return;

  appendMessage("user", message);

  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: userId,
        session_id: parseInt(sessionId),
        message: message
      })
    });

    const data = await res.json();
    if (res.ok && data.reply !== undefined) {
      appendMessage("assistant", data.reply);
    } else {
      appendMessage("assistant", data.message || "Assistant error.");
    }
  } catch (err) {
    appendMessage("assistant", "Server error.");
  }

  input.value = "";
}

function appendMessage(role, content) {
  const chatBox = document.getElementById('chat-box');
  const p = document.createElement('p');
  p.className = role;
  p.textContent = content;
  chatBox.appendChild(p);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function logout() {
  localStorage.removeItem("user_id");
  window.location.href = "/static/login.html";
}

window.onload = () => {
  if (userId) loadSessions();
};
