document.addEventListener('DOMContentLoaded', function() {
    const chatbotButton = document.getElementById('chatbot-button');
    const chatbotWindow = document.getElementById('chatbot-window');
    const chatbotClose = document.getElementById('chatbot-close');
    const chatbotMessages = document.getElementById('chatbot-messages');
    const chatbotInput = document.getElementById('chatbot-input-field');
    const chatbotSend = document.getElementById('chatbot-send');

    // Mostrar/ocultar chatbot
    chatbotButton.addEventListener('click', function() {
        chatbotWindow.classList.toggle('chatbot-hidden');
        if (!chatbotWindow.classList.contains('chatbot-hidden')) {
            chatbotInput.focus();
        }
    });

    chatbotClose.addEventListener('click', function() {
        chatbotWindow.classList.add('chatbot-hidden');
    });

    // Función para agregar mensaje
    function addMessage(content, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.innerHTML = content.replace(/\n/g, '<br>');
        
        messageDiv.appendChild(contentDiv);
        chatbotMessages.appendChild(messageDiv);
        
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    // ✅ FUNCIÓN PRINCIPAL: Enviar mensaje a la IA
    function processUserMessage(message) {
        if (message.trim() === '') return;
        
        // Agregar mensaje del usuario
        addMessage(message, true);
        
        // Mostrar indicador de "escribiendo..."
        addMessage('🤖 Escribiendo...', false);
        
        // Enviar a la API de Python con IA
        fetch('/api/chatbot/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({'message': message})
        })
        .then(response => response.json())
        .then(data => {
            // Quitar indicador de "escribiendo..."
            chatbotMessages.removeChild(chatbotMessages.lastChild);
            
            if (data.success) {
                addMessage(data.response);
            } else {
                addMessage('❌ Error: ' + data.error);
            }
        })
        .catch(error => {
            chatbotMessages.removeChild(chatbotMessages.lastChild);
            addMessage('❌ Error de conexión. ¿Puedes intentar de nuevo?');
            console.error('Error:', error);
        });
        
        chatbotInput.value = '';
    }

    // Función para obtener CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Enviar mensaje con botón
    chatbotSend.addEventListener('click', function() {
        processUserMessage(chatbotInput.value);
    });

    // Enviar mensaje con Enter
    chatbotInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            processUserMessage(chatbotInput.value);
        }
    });

    // Botones rápidos
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('quick-btn')) {
            const message = e.target.getAttribute('data-message');
            processUserMessage(message);
        }
    });
});

function format_price(precio_usd, country='default') {
    // Formatear precio según país
    if (country === 'colombia') {
        const precio_cop = Math.floor(precio_usd * 4200);
        return `\$${precio_cop.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".")} COP`;
    } else {
        return `\$${precio_usd} USD`;
    }
}

// En tu chatbot:
const precio_formateado = format_price(producto.precio, 'colombia');