const chatContainer = document.getElementById("chatContainer");
const openChat = document.getElementById("openChat");
const closeChat = document.getElementById("closeChat");
const sendBtn = document.getElementById("sendBtn");
const userInput = document.getElementById("userInput");
const chatMessages = document.getElementById("chatMessages");

// Toggle Chat Window
openChat.addEventListener("click", () => {
    chatContainer.style.display = "flex";
    openChat.style.display = "none";
});

closeChat.addEventListener("click", () => {
    chatContainer.style.display = "none";
    openChat.style.display = "block";
});

// Create Message Bubble
function createMessage(text, sender) {
    const div = document.createElement("div");
    div.classList.add("message", sender);
    
    // Support basic markdown-like line breaks for cleaner bot responses
    div.innerHTML = text.replace(/\n/g, '<br>');
    
    chatMessages.appendChild(div);
    
    // Smooth scroll to bottom
    chatMessages.scrollTo({
        top: chatMessages.scrollHeight,
        behavior: 'smooth'
    });
}

// Send Message Logic
async function sendMessage() {
    const msg = userInput.value.trim();
    if (!msg) return;

    // Show User Message
    createMessage(msg, "user");
    userInput.value = "";

    // Add typing indicator placeholder (optional)
    const typingDiv = document.createElement("div");
    typingDiv.classList.add("message", "bot");
    typingDiv.textContent = "...";
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
        const response = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: msg })
        });
        
        const data = await response.json();
        
        // Remove typing indicator and show bot reply
        chatMessages.removeChild(typingDiv);
        createMessage(data.reply, "bot");
    } catch (error) {
        chatMessages.removeChild(typingDiv);
        createMessage("I'm sorry, I'm having trouble connecting to the university server. Please ensure the backend is running!", "bot");
    }
}

sendBtn.addEventListener("click", sendMessage);

userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
});
