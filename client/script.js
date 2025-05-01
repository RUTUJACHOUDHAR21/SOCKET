// client/script.js
const chat = document.getElementById('chat');
const messageInput = document.getElementById('message');

// Replace 'localhost' with your server's URL when deploying
const socket = new WebSocket('ws://rutujachoudhar21.github.io/SOCKET/');

socket.addEventListener('open', () => {
  appendMessage('Connected to the server');
});

socket.addEventListener('message', (event) => {
  appendMessage(`Server: ${event.data}`);
});

function sendMessage() {
  const message = messageInput.value;
  if (message) {
    socket.send(message);
    appendMessage(`You: ${message}`);
    messageInput.value = '';
  }
}

function appendMessage(message) {
  const messageElement = document.createElement('div');
  messageElement.textContent = message;
  chat.appendChild(messageElement);
  chat.scrollTop = chat.scrollHeight;
}
