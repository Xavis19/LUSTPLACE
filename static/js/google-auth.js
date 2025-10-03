/**
 * Google OAuth Integration for LUSTPLACE
 * Handles Google Sign-In for both login and registration
 */

class GoogleAuth {
    constructor() {
        // Client ID de Google (debes configurar tu propio Client ID)
        this.clientId = '758944758855-0ej7l6t3rijbefthjdp2e75bmdvup6hr.apps.googleusercontent.com';
        this.isInitialized = false;
        this.init();
    }

    async init() {
        try {
            console.log('🔄 Initializing Google Auth...');
            
            // Cargar la biblioteca de Google
            await this.loadGoogleScript();
            
            // Inicializar Google Sign-In
            google.accounts.id.initialize({
                client_id: this.clientId,
                callback: this.handleCredentialResponse.bind(this),
                auto_select: false,
                cancel_on_tap_outside: true
            });
            
            this.isInitialized = true;
            console.log('✅ Google Auth initialized successfully');
            
            // Renderizar botones existentes después de un pequeño delay
            setTimeout(() => {
                this.renderButtons();
            }, 100);
            
        } catch (error) {
            console.error('❌ Error initializing Google Auth:', error);
            this.showFallbackButtons();
        }
    }

    loadGoogleScript() {
        return new Promise((resolve, reject) => {
            if (window.google && window.google.accounts) {
                resolve();
                return;
            }

            const script = document.createElement('script');
            script.src = 'https://accounts.google.com/gsi/client';
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }

    async handleCredentialResponse(response) {
        try {
            // Mostrar indicador de carga
            this.showLoading();
            
            // Enviar credencial al servidor
            const result = await fetch('/auth/google-auth/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({
                    credential: response.credential
                })
            });

            const data = await result.json();
            
            if (data.success) {
                // Éxito - crear efectos visuales
                this.showSuccess(data.message);
                
                // Redirigir después de un breve delay
                setTimeout(() => {
                    window.location.href = '/productos/';
                }, 1500);
                
            } else {
                this.showError(data.error || 'Error en la autenticación');
            }
            
        } catch (error) {
            console.error('Error en autenticación Google:', error);
            this.showError('Error de conexión. Intenta nuevamente.');
        } finally {
            this.hideLoading();
        }
    }

    renderButtons() {
        // Buscar contenedores de botones de Google
        const containers = document.querySelectorAll('.google-signin-container');
        
        containers.forEach(container => {
            if (!this.initialized) return;
            
            // Limpiar contenido previo
            container.innerHTML = '';
            
            // Renderizar botón de Google
            google.accounts.id.renderButton(container, {
                theme: 'filled_black',
                size: 'large',
                text: 'signin_with',
                shape: 'rectangular',
                logo_alignment: 'left',
                width: '100%'
            });
        });

        // Renderizar botones personalizados
        this.setupCustomButtons();
    }

    setupCustomButtons() {
        const customButtons = document.querySelectorAll('.google-signin-custom');
        
        customButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                this.signIn();
            });
        });
    }

    signIn() {
        if (!this.initialized) {
            this.showError('Google OAuth no está inicializado');
            return;
        }

        google.accounts.id.prompt((notification) => {
            if (notification.isNotDisplayed() || notification.isSkippedMoment()) {
                // Fallback - usar popup
                this.signInWithPopup();
            }
        });
    }

    signInWithPopup() {
        // Implementación de popup como fallback
        const popup = window.open(
            `https://accounts.google.com/oauth/authorize?client_id=${this.clientId}&redirect_uri=${encodeURIComponent(window.location.origin + '/auth/google-callback/')}&response_type=code&scope=openid email profile`,
            'google-signin',
            'width=500,height=600,scrollbars=yes,resizable=yes'
        );

        const checkClosed = setInterval(() => {
            if (popup.closed) {
                clearInterval(checkClosed);
                // Recargar la página para verificar el estado de autenticación
                window.location.reload();
            }
        }, 1000);
    }

    // Funciones de UI
    showLoading() {
        const overlay = document.createElement('div');
        overlay.id = 'google-auth-overlay';
        overlay.className = 'fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center';
        overlay.innerHTML = `
            <div class="bg-dark-card rounded-2xl p-8 flex flex-col items-center space-y-4 animate-fadeInUp">
                <div class="w-16 h-16 border-4 border-orange-400 border-t-transparent rounded-full animate-spin"></div>
                <p class="text-white font-medium">Iniciando sesión con Google...</p>
                <div class="flex items-center space-x-2 text-gray-400 text-sm">
                    <i class="fab fa-google text-blue-400"></i>
                    <span>Procesando credenciales</span>
                </div>
            </div>
        `;
        document.body.appendChild(overlay);
    }

    hideLoading() {
        const overlay = document.getElementById('google-auth-overlay');
        if (overlay) {
            overlay.remove();
        }
    }

    showSuccess(message) {
        this.showNotification(message, 'success');
    }

    showError(message) {
        this.showNotification(message, 'error');
    }

    showNotification(message, type = 'info') {
        const colors = {
            success: 'bg-green-500',
            error: 'bg-red-500',
            info: 'bg-blue-500'
        };

        const icons = {
            success: 'fas fa-check-circle',
            error: 'fas fa-times-circle',
            info: 'fas fa-info-circle'
        };

        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 ${colors[type]} text-white px-6 py-4 rounded-lg shadow-lg z-50 flex items-center space-x-3 transform translate-x-full transition-transform duration-300`;
        notification.innerHTML = `
            <i class="${icons[type]}"></i>
            <span>${message}</span>
        `;

        document.body.appendChild(notification);

        // Animar entrada
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);

        // Remover después de 4 segundos
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => notification.remove(), 300);
        }, 4000);
    }

    getCSRFToken() {
        const token = document.querySelector('[name=csrfmiddlewaretoken]');
        if (token) return token.value;

        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') return value;
        }
        return '';
    }
}

    showFallbackButtons() {
        // Mostrar botones de fallback si Google no está disponible
        const containers = document.querySelectorAll('.google-signin-container, .google-signin-custom');
        
        containers.forEach(container => {
            container.innerHTML = `
                <button class="btn w-full bg-white text-gray-700 border border-gray-300 hover:bg-gray-50 flex items-center justify-center gap-3 py-3 rounded-xl transition-all duration-300 opacity-50 cursor-not-allowed" 
                        disabled>
                    <svg class="w-5 h-5" viewBox="0 0 24 24">
                        <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                        <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                        <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                        <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                    </svg>
                    <span>Google no disponible</span>
                </button>
            `;
        });
    }
}

// Inicializar Google Auth cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    window.googleAuth = new GoogleAuth();
});

// También inicializar si el script se carga después del DOM
if (document.readyState !== 'loading') {
    window.googleAuth = new GoogleAuth();
}

// Función global para botones personalizados
window.signInWithGoogle = function() {
    if (window.googleAuth) {
        window.googleAuth.signIn();
    } else {
        console.error('Google Auth no está inicializado');
    }
};
