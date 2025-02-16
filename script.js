// Array para armazenar o histórico do chat em memória
let chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];

// Função para renderizar o histórico no HTML
function renderChatHistory() {
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML = ''; // Limpa o chat antes de renderizar o histórico

    chatHistory.forEach(function(message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');

        // Verifica o remetente e adiciona a classe correta
        if (message.sender === 'user') {
            messageElement.classList.add('user');
        } else {
            messageElement.classList.add('ai'); // Certifique-se de que essa classe existe no CSS
        }

        // Cabeçalho de data/hora
        const timestamp = new Date(message.timestamp);
        const header = document.createElement('small');
        header.textContent = formatDateTime(timestamp);
        header.style.display = 'block';
        header.style.marginBottom = '5px';
        header.style.color = '#666';

        messageElement.appendChild(header);
        messageElement.appendChild(document.createTextNode(message.content));
        chatBox.appendChild(messageElement);
    });

    chatBox.scrollTop = chatBox.scrollHeight; // Faz o scroll para o final
}


// Chama a função para renderizar o histórico quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    renderChatHistory();
});

document.getElementById('send-btn').addEventListener('click', function() {
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim() !== "") {
        navigator.clipboard.writeText(userInput).then(function() {
            const chatBox = document.getElementById('chat-box');
            const userMessage = document.createElement('div');
            userMessage.classList.add('message', 'user');
            
            // Cabeçalho de data/hora
            const timestamp = new Date();
            const header = document.createElement('small');
            header.textContent = formatDateTime(timestamp);
            header.style.display = 'block';
            header.style.marginBottom = '5px';
            header.style.color = '#666';

            userMessage.appendChild(header);
            userMessage.appendChild(document.createTextNode(userInput));
            chatBox.appendChild(userMessage);

            // Armazena em memória (MANTIDO O QUE JÁ FUNCIONAVA)
            chatHistory.push({
                sender: 'user',
                content: userInput,
                timestamp: timestamp.toISOString() // Formato ISO para facilitar envio POST
            });

            // Armazena no localStorage
            localStorage.setItem('chatHistory', JSON.stringify(chatHistory));

            document.getElementById('user-input').value = '';
            chatBox.scrollTop = chatBox.scrollHeight;
        }).catch(function(error) {
            console.error('Erro ao copiar texto: ', error);
        });
    }
});

document.getElementById('receive-btn').addEventListener('click', function() {
    navigator.clipboard.readText().then(function(text) {
        if (text.trim() !== "") {
            const chatBox = document.getElementById('chat-box');
            const aiMessage = document.createElement('div');
            aiMessage.classList.add('message', 'ai');
            
            // Cabeçalho de data/hora
            const timestamp = new Date();
            const header = document.createElement('small');
            header.textContent = formatDateTime(timestamp);
            header.style.display = 'block';
            header.style.marginBottom = '5px';
            header.style.color = '#666';

            aiMessage.appendChild(header);
            aiMessage.appendChild(document.createTextNode(text));
            chatBox.appendChild(aiMessage);

            // Armazena em memória (MANTIDO O QUE JÁ FUNCIONAVA)
            chatHistory.push({
                sender: 'ai',  
                content: text,
                timestamp: timestamp.toISOString()
            });

            // Armazena no localStorage
            localStorage.setItem('chatHistory', JSON.stringify(chatHistory));

            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }).catch(function(error) {
        console.error('Erro ao colar texto: ', error);
    });
});

// Função de formatação de data (PERMANECEU IGUAL)
function formatDateTime(date) {
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');

    return `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`;
}

// Função para enviar ao pressionar 'Enter'
document.getElementById('user-input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Impede a quebra de linha no campo de texto
        document.getElementById('send-btn').click(); // Aciona o botão de envio
    }
});

// Lógica para o botão "Novo Chat"
document.getElementById('new-chat-btn').addEventListener('click', function() {
    // Limpa o histórico na memória
    chatHistory = [];
    // Limpa o histórico no localStorage
    localStorage.removeItem('chatHistory');
    // Limpa o conteúdo do chat na interface
    document.getElementById('chat-box').innerHTML = '';
    // Limpa o campo de entrada de texto
    document.getElementById('user-input').value = '';
});

// Adicione este código ao final do script.js
document.getElementById('post-btn').addEventListener('click', function() {
    if (chatHistory.length === 0) {
        alert('Nenhuma mensagem no chat para enviar!');
        return;
    }

    console.log('Dados a serem enviados:', chatHistory); // <--- LOG DOS DADOS

    fetch('https://jsonplaceholder.typicode.com/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(chatHistory)
    })
    .then(response => {
        console.log('Status da resposta:', response.status); // <--- LOG DO STATUS
        return response.json();
    })
    .then(data => {
        console.log('Resposta da API:', data); // <--- LOG DA RESPOSTA
        alert('Chat enviado! Confira o console para detalhes.');
    })
    .catch(error => {
        console.error('Erro completo:', error); // <--- LOG DE ERRO
    });
});
