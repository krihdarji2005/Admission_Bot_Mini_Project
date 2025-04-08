document.addEventListener("DOMContentLoaded", function () {
  // DOM Elements
  const chatMessages = document.getElementById("chatMessages");
  const userInput = document.getElementById("userInput");
  const sendBtn = document.getElementById("sendBtn");
  const clearChatBtn = document.querySelector(".clear-chat-btn");
  const settingsBtn = document.querySelector(".settings-btn");
  const sidebarToggle = document.getElementById("sidebarToggle");
  const sidebar = document.getElementById("sidebar");
  const suggestionBtns = document.querySelectorAll(".suggestion-btn");
  const newChatBtn = document.querySelector(".new-chat-btn");
  const historyList = document.querySelector(".history-list");

  // API URL for the Flask backend
  const API_URL = "http://127.0.0.1:5000/api/chat";

  // State variables
  let currentChatId = 1;
  let isTyping = false;
  let recentChats = [];
  let userSettings = {
    darkMode: false,
    fontSize: "medium",
    notifications: true
  };

  // Initialize the application
  initializeApp();

  // Initialize the application
  function initializeApp() {
    // Load settings from localStorage
    loadSettings();
    
    // Load recent chats from localStorage
    loadRecentChats();
    
    // If no chats exist, create a default one
    if (recentChats.length === 0) {
      createNewChat("Admission Query", true);
    }
    
    // Render the recent chats in the sidebar
    renderRecentChats();
    
    // Apply saved settings
    applySettings();
    
    // Set up event listeners
    setupEventListeners();
  }

  // Set up event listeners
  function setupEventListeners() {
    // Send message when send button is clicked
    sendBtn.addEventListener("click", sendMessage);
    
    // Send message when Enter key is pressed in input field
    userInput.addEventListener("keypress", function(e) {
      if (e.key === "Enter") {
        sendMessage();
      }
    });
    
    // Clear chat when clear button is clicked
    clearChatBtn.addEventListener("click", function() {
      // Show confirmation dialog
      if (confirm("Are you sure you want to clear the current chat?")) {
        clearChat();
      }
    });
    
    // Toggle settings panel when settings button is clicked
    settingsBtn.addEventListener("click", toggleSettings);
    
    // Toggle sidebar when sidebar toggle button is clicked
    sidebarToggle.addEventListener("click", function() {
      sidebar.classList.toggle("active");
      
      // Update toggle button icon
      const icon = sidebarToggle.querySelector("i");
      if (icon) {
        icon.className = sidebar.classList.contains("active") 
          ? "fas fa-chevron-left" 
          : "fas fa-chevron-right";
      }
    });
    
    // Create new chat when new chat button is clicked
    newChatBtn.addEventListener("click", function() {
      createNewChat("New Chat", true);
    });
    
    // Add click event to suggestion buttons
    suggestionBtns.forEach(btn => {
      btn.addEventListener("click", function() {
        const suggestion = this.textContent;
        userInput.value = suggestion;
        sendMessage();
      });
    });
  }

  // Load settings from localStorage
  function loadSettings() {
    const savedSettings = localStorage.getItem("chatbot_settings");
    if (savedSettings) {
      userSettings = JSON.parse(savedSettings);
    }
  }

  // Save settings to localStorage
  function saveSettings() {
    localStorage.setItem("chatbot_settings", JSON.stringify(userSettings));
  }

  // Apply settings to the UI
  function applySettings() {
    // Apply dark mode
    if (userSettings.darkMode) {
      document.body.classList.add("dark");
    } else {
      document.body.classList.remove("dark");
    }
    
    // Apply font size
    document.documentElement.style.setProperty(
      "--font-size-base", 
      userSettings.fontSize === "small" ? "0.875rem" : 
      userSettings.fontSize === "large" ? "1.125rem" : "1rem"
    );
  }

  // Load recent chats from localStorage
  function loadRecentChats() {
    const savedChats = localStorage.getItem("chatbot_recent_chats");
    if (savedChats) {
      recentChats = JSON.parse(savedChats);
      
      // Get the highest chat ID to ensure new chats have unique IDs
      if (recentChats.length > 0) {
        const maxId = Math.max(...recentChats.map(chat => chat.id));
        currentChatId = maxId + 1;
      }
      
      // Find the active chat
      const activeChat = recentChats.find(chat => chat.active);
      if (activeChat) {
        // Load messages for the active chat
        loadChatMessages(activeChat.id);
      }
    }
  }

  // Save recent chats to localStorage
  function saveRecentChats() {
    localStorage.setItem("chatbot_recent_chats", JSON.stringify(recentChats));
  }

  // Render recent chats in the sidebar
  function renderRecentChats() {
    // Clear the history list
    historyList.innerHTML = "";
    
    // Add each chat to the history list
    recentChats.forEach(chat => {
      const li = document.createElement("li");
      li.className = `history-item ${chat.active ? "active" : ""}`;
      li.dataset.id = chat.id;
      
      // Get the appropriate icon based on chat type
      let iconHtml;
      switch (chat.icon) {
        case "chat":
          iconHtml = '<span class="material-icons-outlined">chat</span>';
          break;
        case "description":
          iconHtml = '<span class="material-icons-outlined">description</span>';
          break;
        case "menu_book":
          iconHtml = '<span class="material-icons-outlined">menu_book</span>';
          break;
        case "event":
          iconHtml = '<span class="material-icons-outlined">event</span>';
          break;
        case "home_work":
          iconHtml = '<span class="material-icons-outlined">home_work</span>';
          break;
        default:
          iconHtml = '<span class="material-icons-outlined">chat</span>';
      }
      
      // Create the chat item HTML
      li.innerHTML = `
        <span class="history-icon">${iconHtml}</span>
        <span class="history-text">${chat.title}</span>
        <button class="delete-chat-btn" title="Delete chat">
          <i class="fas fa-trash"></i>
        </button>
      `;
      
      // Add click event to select this chat
      li.addEventListener("click", function() {
        selectChat(chat.id);
      });
      
      // Add click event to delete button
      const deleteBtn = li.querySelector(".delete-chat-btn");
      deleteBtn.addEventListener("click", function(e) {
        e.stopPropagation(); // Prevent triggering the chat selection
        deleteChat(chat.id);
      });
      
      // Add the chat item to the history list
      historyList.appendChild(li);
    });
  }

  // Create a new chat
  function createNewChat(title, setActive = false) {
    // Create a new chat object
    const newChat = {
      id: currentChatId++,
      title: title,
      icon: "chat",
      active: setActive,
      messages: [{
        content: "👋 Hi there! I'm your KJSIT Admission Assistant. How can I help you with your admission queries today?",
        isUser: false
      }]
    };
    
    // If setting this chat as active, deactivate all other chats
    if (setActive) {
      recentChats.forEach(chat => {
        chat.active = false;
      });
    }
    
    // Add the new chat to the recent chats
    recentChats.unshift(newChat);
    
    // Save the updated recent chats
    saveRecentChats();
    
    // Render the updated recent chats
    renderRecentChats();
    
    // If setting this chat as active, load its messages
    if (setActive) {
      loadChatMessages(newChat.id);
    }
    
    return newChat;
  }

  // Select a chat
  function selectChat(chatId) {
    // Find the chat with the given ID
    const chat = recentChats.find(c => c.id === chatId);
    if (!chat) return;
    
    // Deactivate all chats
    recentChats.forEach(c => {
      c.active = false;
    });
    
    // Activate the selected chat
    chat.active = true;
    
    // Save the updated recent chats
    saveRecentChats();
    
    // Render the updated recent chats
    renderRecentChats();
    
    // Load the messages for the selected chat
    loadChatMessages(chatId);
    
    // Close sidebar on mobile after selection
    if (window.innerWidth < 768) {
      sidebar.classList.remove("active");
      
      // Update toggle button icon
      const icon = sidebarToggle.querySelector("i");
      if (icon) {
        icon.className = "fas fa-chevron-right";
      }
    }
  }

  // Delete a chat
  function deleteChat(chatId) {
    // Show confirmation dialog
    if (!confirm("Are you sure you want to delete this chat?")) {
      return;
    }
    
    // Check if the chat to delete is active
    const chatToDelete = recentChats.find(c => c.id === chatId);
    const isActive = chatToDelete && chatToDelete.active;
    
    // Remove the chat from recent chats
    recentChats = recentChats.filter(c => c.id !== chatId);
    
    // If there are no chats left, create a new one
    if (recentChats.length === 0) {
      createNewChat("New Chat", true);
    } 
    // If the deleted chat was active, activate the first chat
    else if (isActive) {
      recentChats[0].active = true;
      loadChatMessages(recentChats[0].id);
    }
    
    // Save the updated recent chats
    saveRecentChats();
    
    // Render the updated recent chats
    renderRecentChats();
  }

  // Load messages for a chat
  function loadChatMessages(chatId) {
    // Find the chat with the given ID
    const chat = recentChats.find(c => c.id === chatId);
    if (!chat) return;
    
    // Clear the chat messages container
    chatMessages.innerHTML = "";
    
    // Add each message to the chat messages container
    chat.messages.forEach(message => {
      addMessageToUI(message.content, message.isUser);
    });
    
    // Scroll to the bottom of the chat
    scrollToBottom();
  }

  // Save messages for the active chat
  function saveActiveChatMessages() {
    // Find the active chat
    const activeChat = recentChats.find(c => c.active);
    if (!activeChat) return;
    
    // Get all messages from the UI
    const messages = [];
    const messageElements = chatMessages.querySelectorAll(".message");
    
    messageElements.forEach(element => {
      const isUser = element.classList.contains("user-message");
      const content = element.querySelector(".message-content p").innerHTML;
      messages.push({ content, isUser });
    });
    
    // Update the active chat's messages
    activeChat.messages = messages;
    
    // Save the updated recent chats
    saveRecentChats();
  }

  // Send a message
  async function sendMessage() {
    const message = userInput.value.trim();
    if (message === "") return;
    
    // Add the user message to the UI
    addMessageToUI(message, true);
    
    // Clear the input field
    userInput.value = "";
    
    // Save the updated messages
    saveActiveChatMessages();
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
      // Send the message to the backend
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ message })
      });
      
      if (!response.ok) {
        throw new Error("Failed to get response from server");
      }
      
      const data = await response.json();
      
      // Hide typing indicator
      hideTypingIndicator();
      
      // Add the bot response to the UI
      addMessageToUI(data.response, false);
      
      // Save the updated messages
      saveActiveChatMessages();
      
      // Show notification if enabled
      if (userSettings.notifications && document.hidden) {
        showNotification("New Message", "You have a new message from KJSIT Bot");
      }
    } catch (error) {
      console.error("Error:", error);
      
      // Hide typing indicator
      hideTypingIndicator();
      
      // Add error message to the UI
      addMessageToUI("Sorry, I couldn't process your request. Please try again later.", false);
      
      // Save the updated messages
      saveActiveChatMessages();
    }
  }

  // Add a message to the UI
  function addMessageToUI(content, isUser) {
    const messageDiv = document.createElement("div");
    messageDiv.className = isUser ? "message user-message" : "message ai-message";
    
    const avatarDiv = document.createElement("div");
    avatarDiv.className = "message-avatar";
    
    const avatarImg = document.createElement("img");
    avatarImg.src = isUser ? "/assets/person.png" : "/assets/logo.png";
    avatarDiv.appendChild(avatarImg);
    
    const contentDiv = document.createElement("div");
    contentDiv.className = "message-content";
    contentDiv.innerHTML = `<p>${content}</p>`;
    
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    
    chatMessages.appendChild(messageDiv);
    
    // Scroll to the bottom of the chat
    scrollToBottom();
  }

  // Show typing indicator
  function showTypingIndicator() {
    // Check if typing indicator already exists
    if (document.getElementById("typing-indicator")) return;
    
    const typingDiv = document.createElement("div");
    typingDiv.className = "message ai-message typing";
    typingDiv.id = "typing-indicator";
    
    typingDiv.innerHTML = `
      <div class="message-avatar">
        <img src="/assets/logo.png" alt="Bot Avatar">
      </div>
      <div class="message-content">
        <div class="typing-indicator">
          <span class="dot dot-1"></span>
          <span class="dot dot-2"></span>
          <span class="dot dot-3"></span>
        </div>
      </div>
    `;
    
    chatMessages.appendChild(typingDiv);
    
    // Scroll to the bottom of the chat
    scrollToBottom();
  }

  // Hide typing indicator
  function hideTypingIndicator() {
    const typingIndicator = document.getElementById("typing-indicator");
    if (typingIndicator) {
      typingIndicator.remove();
    }
  }

  // Clear the current chat
  function clearChat() {
    // Find the active chat
    const activeChat = recentChats.find(c => c.active);
    if (!activeChat) return;
    
    // Reset the chat to only have the welcome message
    activeChat.messages = [{
      content: "👋 Hi there! I'm your KJSIT Admission Assistant. How can I help you with your admission queries today?",
      isUser: false
    }];
    
    // Save the updated recent chats
    saveRecentChats();
    
    // Load the messages for the active chat
    loadChatMessages(activeChat.id);
  }

  // Toggle settings panel
  function toggleSettings() {
    // Check if settings panel already exists
    const existingPanel = document.getElementById("settings-panel");
    if (existingPanel) {
      existingPanel.remove();
      return;
    }
    
    // Create settings panel
    const settingsPanel = document.createElement("div");
    settingsPanel.id = "settings-panel";
    settingsPanel.className = "settings-panel";
    
    // Add settings content
    settingsPanel.innerHTML = `
      <h3>Settings</h3>
      <div class="settings-option">
        <label for="darkMode">Dark Mode</label>
        <input type="checkbox" id="darkMode" ${userSettings.darkMode ? "checked" : ""}>
      </div>
      <div class="settings-option">
        <label for="fontSize">Font Size</label>
        <select id="fontSize">
          <option value="small" ${userSettings.fontSize === "small" ? "selected" : ""}>Small</option>
          <option value="medium" ${userSettings.fontSize === "medium" ? "selected" : ""}>Medium</option>
          <option value="large" ${userSettings.fontSize === "large" ? "selected" : ""}>Large</option>
        </select>
      </div>
      <div class="settings-option">
        <label for="notifications">Notifications</label>
        <input type="checkbox" id="notifications" ${userSettings.notifications ? "checked" : ""}>
      </div>
      <button id="save-settings" class="settings-save-btn">Save Settings</button>
    `;
    
    // Add the settings panel to the DOM
    document.querySelector(".chat-header").insertAdjacentElement("afterend", settingsPanel);
    
    // Add event listener to save button
    document.getElementById("save-settings").addEventListener("click", function() {
      // Update settings from form values
      userSettings.darkMode = document.getElementById("darkMode").checked;
      userSettings.fontSize = document.getElementById("fontSize").value;
      userSettings.notifications = document.getElementById("notifications").checked;
      
      // Save the updated settings
      saveSettings();
      
      // Apply the updated settings
      applySettings();
      
      // Close the settings panel
      settingsPanel.remove();
      
      // Show confirmation message
      showToast("Settings saved successfully!");
    });
  }

  // Show a toast notification
  function showToast(message) {
    // Check if toast container exists
    let toastContainer = document.getElementById("toast-container");
    if (!toastContainer) {
      // Create toast container
      toastContainer = document.createElement("div");
      toastContainer.id = "toast-container";
      document.body.appendChild(toastContainer);
      
      // Add styles for toast container
      toastContainer.style.position = "fixed";
      toastContainer.style.bottom = "20px";
      toastContainer.style.right = "20px";
      toastContainer.style.zIndex = "9999";
    }
    
    // Create toast
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.textContent = message;
    
    // Add styles for toast
    toast.style.backgroundColor = "var(--primary-color)";
    toast.style.color = "white";
    toast.style.padding = "10px 20px";
    toast.style.borderRadius = "4px";
    toast.style.marginTop = "10px";
    toast.style.boxShadow = "0 2px 5px rgba(0, 0, 0, 0.2)";
    toast.style.animation = "fadeIn 0.3s, fadeOut 0.3s 2.7s";
    
    // Add toast to container
    toastContainer.appendChild(toast);
    
    // Remove toast after 3 seconds
    setTimeout(() => {
      toast.remove();
      
      // Remove container if empty
      if (toastContainer.children.length === 0) {
        toastContainer.remove();
      }
    }, 3000);
  }

  // Show browser notification
  function showNotification(title, message) {
    // Check if browser supports notifications
    if (!("Notification" in window)) {
      console.log("This browser does not support desktop notification");
      return;
    }
    
    // Check if permission is granted
    if (Notification.permission === "granted") {
      // Create notification
      const notification = new Notification(title, {
        body: message,
        icon: "/assets/logo.png"
      });
      
      // Close notification after 5 seconds
      setTimeout(() => {
        notification.close();
      }, 5000);
    }
    // Request permission if not granted
    else if (Notification.permission !== "denied") {
      Notification.requestPermission().then(permission => {
        if (permission === "granted") {
          showNotification(title, message);
        }
      });
    }
  }

  // Scroll to the bottom of the chat
  function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  // Add keyframe animations for toast
  const style = document.createElement("style");
  style.textContent = `
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeOut {
      from { opacity: 1; transform: translateY(0); }
      to { opacity: 0; transform: translateY(-20px); }
    }
    
    /* Settings Panel */
    .settings-panel {
      position: absolute;
      top: 70px;
      right: 20px;
      background-color: var(--background-color);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 1.25rem;
      box-shadow: var(--shadow-md);
      z-index: 100;
      width: 250px;
    }
    
    .settings-panel h3 {
      margin-top: 0;
      margin-bottom: 1rem;
      font-size: 1rem;
      color: var(--text-color);
    }
    
    .settings-option {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;
    }
    
    .settings-option label {
      font-size: 0.9375rem;
      color: var(--text-secondary);
    }
    
    .settings-save-btn {
      width: 100%;
      padding: 0.625rem;
      background-color: var(--primary-color);
      color: white;
      border: none;
      border-radius: var(--radius-sm);
      cursor: pointer;
      font-weight: 500;
      margin-top: 1rem;
      transition: all var(--transition-fast);
    }
    
    .settings-save-btn:hover {
      background-color: var(--accent-color);
    }
    
    /* Delete Chat Button */
    .delete-chat-btn {
      opacity: 0;
      background: none;
      border: none;
      color: var(--text-light);
      cursor: pointer;
      transition: all var(--transition-fast);
      padding: 4px;
      border-radius: 50%;
    }
    
    .history-item:hover .delete-chat-btn {
      opacity: 1;
    }
    
    .delete-chat-btn:hover {
      color: var(--accent-color);
      background-color: var(--primary-light);
    }
    
    /* Typing Indicator */
    .typing-indicator {
      display: flex;
      align-items: center;
      gap: 4px;
    }
    
    .typing-indicator .dot {
      width: 8px;
      height: 8px;
      background-color: var(--primary-color);
      border-radius: 50%;
      animation: blink 1.4s infinite;
      animation-fill-mode: both;
    }
    
    .typing-indicator .dot:nth-child(2) {
      animation-delay: 0.2s;
    }
    
    .typing-indicator .dot:nth-child(3) {
      animation-delay: 0.4s;
    }
    
    @keyframes blink {
      0% { opacity: 0.2; transform: scale(0.8); }
      20% { opacity: 1; transform: scale(1); }
      100% { opacity: 0.2; transform: scale(0.8); }
    }
    
    /* Dark Mode */
    .dark {
      --primary-color: hsl(0, 79%, 50%);
      --primary-light: hsla(0, 79%, 30%, 0.3);
      --primary-dark: hsl(0, 79%, 60%);
      --accent-color: #ff4040;
      --text-color: #f0f0f0;
      --text-secondary: #d0d0d0;
      --text-light: #a0a0a0;
      --link-color: #ff5555;
      --background-color: #1a1a1a;
      --background-light: #252525;
      --light-gray: #333333;
      --gray: #666666;
      --dark-gray: #999999;
      --border-color: #444444;
    }
  `;
  document.head.appendChild(style);
});
