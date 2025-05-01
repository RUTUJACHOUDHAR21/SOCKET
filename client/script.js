const chat = document.getElementById('chat');
const messageInput = document.getElementById('message');

// Connect to your deployed server
const socket = new WebSocket('wss://socket-gjfh.onrender.com');

socket.addEventListener('open', () => {
  appendMessage('✅ Connected to the server');
});

socket.addEventListener('message', (event) => {
  appendMessage(`📩 ${event.data}`);
});

function sendMessage() {
  const message = messageInput.value;
  if (message) {
    socket.send(message);
    appendMessage(`🧑 You: ${message}`);
    messageInput.value = '';
  }
}

function appendMessage(message) {
  const messageElement = document.createElement('div');
  messageElement.textContent = message;
  chat.appendChild(messageElement);
  chat.scrollTop = chat.scrollHeight;
}
