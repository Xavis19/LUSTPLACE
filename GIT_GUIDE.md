# 🔥 MarketPlace LUST - Guía de Git

## 📋 **Comandos para Subir a GitHub**

### **1. Inicializar Repositorio**
```bash
git init
git branch -M main
```

### **2. Agregar Archivos**
```bash
git add .
git commit -m "🎉 Initial commit: MarketPlace LUST v1.0"
```

### **3. Conectar con GitHub**
```bash
# Reemplaza TU_USUARIO con tu usuario de GitHub
git remote add origin https://github.com/TU_USUARIO/MarketPlace-LUST.git
```

### **4. Subir al Repositorio**
```bash
git push -u origin main
```

## 🔄 **Comandos Frecuentes**

### **Actualizar Cambios**
```bash
git add .
git commit -m "✨ Descripción del cambio"
git push
```

### **Ver Estado**
```bash
git status
git log --oneline
```

### **Crear Nueva Rama**
```bash
git checkout -b feature/nueva-funcionalidad
git push -u origin feature/nueva-funcionalidad
```

## 📝 **Convención de Commits**

- `🎉` `:tada:` - Commit inicial
- `✨` `:sparkles:` - Nueva funcionalidad
- `🐛` `:bug:` - Corrección de bug
- `📝` `:memo:` - Documentación
- `🎨` `:art:` - Mejoras de UI/UX
- `🔧` `:wrench:` - Configuración
- `🚀` `:rocket:` - Performance
- `🔒` `:lock:` - Seguridad
- `📦` `:package:` - Dependencias

## 🏷️ **Crear Release**

```bash
git tag -a v1.0.0 -m "🏷️ Release v1.0.0: MarketPlace LUST"
git push origin v1.0.0
```