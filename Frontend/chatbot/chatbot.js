document.addEventListener("DOMContentLoaded", function () {
  const chatMessages = document.getElementById("chatMessages");
  const userInput = document.getElementById("userInput");
  const sendBtn = document.getElementById("sendBtn");

  const API_URL = "http://127.0.0.1:5000/api/chat"; // Ensure correct API URL

  async function sendMessage() {
    const message = userInput.value.trim();
    if (message === "") return; // Prevent empty messages

    addMessage(message, true);
    userInput.value = ""; // Clear input after sending

    const typingDiv = document.createElement("div");
    typingDiv.className = "message ai-message typing";
    typingDiv.innerHTML = `<div class="message-avatar"><img src="../assets/person.png"></div>
                               <div class="message-content"><p>...</p></div>`;
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message }),
      });

      if (!response.ok) throw new Error("Server error");

      const data = await response.json();
      chatMessages.removeChild(typingDiv);
      addMessage(data.response);
    } catch (error) {
      chatMessages.removeChild(typingDiv);
      addMessage("❌ Error: Cannot connect to chatbot.");
      console.error("Error:", error);
    }
  }

  sendBtn.addEventListener("click", sendMessage);
  userInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") sendMessage(); // Fix enter key issue
  });

  function addMessage(content, isUser = false) {
    const messageDiv = document.createElement("div");
    messageDiv.className = isUser
      ? "message user-message"
      : "message ai-message";

    const avatarDiv = document.createElement("div");
    avatarDiv.className = "message-avatar";

    const avatarImg = document.createElement("img");
    avatarImg.src = isUser ? "/assets/person.png" : "/assets/logo.png";


    const contentDiv = document.createElement("div");
    contentDiv.className = "message-content";
    contentDiv.innerHTML = `<p>${content}</p>`;

    avatarDiv.appendChild(avatarImg);
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
});
