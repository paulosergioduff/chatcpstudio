# Chat CP Studio (Chat Copy and Paste Studio)

Chat CP Studio is a lightweight web application designed to facilitate manual interactions with LLMs (Large Language Models). Instead of relying on direct API integrations, this tool provides a structured way to copy and paste messages while keeping a persistent chat history.

## ✨ Features
- 📋 **Clipboard Integration** – Easily copy user inputs and paste AI responses.
- 💾 **Persistent Chat History** – Uses `localStorage` to maintain past conversations.
- 🎨 **Simple and Clean UI** – A minimalistic chat interface for easy message tracking.
- 🚀 **Send Conversations via POST** – Allows exporting chat history for further processing.

## 🛠️ How It Works
1. **Type your message** and click "Send". The text is copied to the clipboard.
2. **Paste AI responses** into the app using the "Receive" button.
3. **Review and manage** conversations with built-in history storage.
4. **Export** chat logs using the "Send Chat via POST" feature.

## 🏗️ Tech Stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Simple HTTP Server)
- **Storage**: Local Storage (browser-based)

## 🏃 Getting Started
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/yourusername/chat-cp-studio.git
cd chat-cp-studio
