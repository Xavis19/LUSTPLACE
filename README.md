# 🔥 MarketPlace LUST

> **Marketplace Premium para Productos Adultos**  
> Una plataforma de e-commerce moderna y elegante con diseño dark theme y funcionalidades avanzadas.

---

## 📋 **Descripción**

MarketPlace LUST es una plataforma de comercio electrónico especializada en productos para adultos, construida con Django y diseñada con un enfoque en la **privacidad**, **discreción** y **experiencia de usuario premium**.

### ✨ **Características Principales**

- 🎨 **Diseño Moderno**: Dark theme con glass morphism y bordes ovalados
- 🛡️ **Sistema de Roles**: Diferenciación entre usuarios y administradores
- 🛒 **Carrito Inteligente**: Sistema de sesiones para gestión de compras
- ❤️ **Sistema de Favoritos**: Guardar productos preferidos
- 📱 **Responsive Design**: Optimizado para móviles y tablets
- 🔐 **Autenticación Completa**: Registro, login y logout
- ⚙️ **Panel de Admin Web**: Gestión de productos y usuarios desde la interfaz
- 📄 **Términos y Condiciones**: Sistema legal completo
- 💳 **Sistema de Pagos**: Integración preparada para múltiples métodos

---

## 🚀 **Tecnologías Utilizadas**

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Django** | 5.2.6+ | Framework web principal |
| **Python** | 3.9+ | Lenguaje de programación |
| **SQLite** | Incluido | Base de datos (desarrollo) |
| **Pillow** | 10.0.0+ | Procesamiento de imágenes |
| **HTML5/CSS3** | - | Frontend moderno |
| **JavaScript** | ES6+ | Interactividad |
| **FontAwesome** | 6.0+ | Iconografía |
| **Inter Font** | - | Tipografía moderna |

---

## 📦 **Instalación**

### **Prerrequisitos**
- Python 3.9 o superior
- pip (gestor de paquetes de Python)
- Git

### **1. Clonar el Repositorio**
```bash
git clone https://github.com/TU_USUARIO/MarketPlace-LUST.git
cd MarketPlace-LUST
```

### **2. Crear Entorno Virtual**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### **3. Instalar Dependencias**
```bash
# Solo las esenciales (recomendado para empezar)
pip install Django>=5.0,<6.0 Pillow>=10.0.0 python-decouple>=3.6 pytz>=2023.3

# O todas las dependencias
pip install -r requirements.txt
```

### **4. Configurar Base de Datos**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **5. Crear Superusuario**
```bash
python manage.py createsuperuser
```

### **6. Ejecutar Servidor**
```bash
python manage.py runserver
```

🎉 **¡Listo!** Visita http://127.0.0.1:8000

---

## 📁 **Estructura del Proyecto**

```
MarketPlace LUST/
├── 📁 authentication/          # Sistema de autenticación
├── 📁 Carrito/                # Gestión del carrito de compras
├── 📁 login/                  # Módulo de login
├── 📁 marketplace_lust/       # Configuración principal
├── 📁 payments/               # Sistema de pagos
├── 📁 productos/              # Gestión de productos
├── 📁 VirtualR/               # Funcionalidades adicionales
├── 📁 templates/              # Templates HTML
│   ├── 📁 Login/              # Templates de autenticación
│   ├── 📁 productos/          # Templates de productos
│   └── 📁 payments/           # Templates de pagos
├── 📁 static/                 # Archivos estáticos
│   ├── 📁 css/               # Estilos CSS
│   ├── 📁 js/                # JavaScript
│   └── 📁 img/               # Imágenes
├── 📁 media/                  # Archivos subidos por usuarios
├── 📄 requirements.txt        # Dependencias
├── 📄 manage.py              # Script de Django
└── 📄 db.sqlite3            # Base de datos (desarrollo)
```

---

## 🎯 **Funcionalidades**

### **👤 Para Usuarios**
- ✅ Registro y autenticación
- ✅ Navegación de productos con filtros
- ✅ Sistema de carrito de compras
- ✅ Gestión de favoritos
- ✅ Perfil personal con estadísticas
- ✅ Acceso a términos y condiciones

### **⚙️ Para Administradores**
- ✅ Panel de administración web moderno
- ✅ Gestión completa de productos (CRUD)
- ✅ Administración de usuarios y roles
- ✅ Estadísticas en tiempo real
- ✅ Acceso al Django Admin tradicional

### **🎨 Diseño y UX**
- ✅ Dark theme consistente
- ✅ Glass morphism effects
- ✅ Bordes ovalados en todos los componentes
- ✅ Animaciones suaves y transiciones
- ✅ Responsive design para todos los dispositivos
- ✅ Iconografía moderna con FontAwesome

---

## 🛠️ **Configuración Adicional**

### **Variables de Entorno**
Crea un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu-clave-secreta-super-segura
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### **Configuración de Producción**
Para despliegue en producción, descomenta en `requirements.txt`:
- `gunicorn` - Servidor WSGI
- `whitenoise` - Archivos estáticos
- `psycopg2-binary` - PostgreSQL

---

## 🤝 **Contribuir**

1. **Fork** el proyecto
2. Crea una **rama** para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add: Amazing Feature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. Abre un **Pull Request**

---

## 📞 **Contacto y Soporte**

- 📱 **WhatsApp**: +57 316 533 5942
- 📸 **Instagram**: [@ukx__19](https://instagram.com/ukx__19)
- 📧 **Email**: soporte@marketplacelust.com

---

## 📄 **Licencia**

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 🏆 **Agradecimientos**

- **Django Team** por el framework increíble
- **FontAwesome** por los iconos
- **Google Fonts** por la tipografía Inter
- **La comunidad de desarrolladores** por las mejores prácticas

---

<div align="center">

**🔥 MarketPlace LUST - E-commerce Premium**

*Construido con ❤️ y Django*

[![Django](https://img.shields.io/badge/Django-5.2+-green.svg)](https://djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>