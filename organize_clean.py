#!/usr/bin/env python3
"""
🧹 Script de Organización y Limpieza LUSTPLACE
Elimina archivos obsoletos y reorganiza la estructura del proyecto
Fecha: 3 de octubre de 2025
"""
import os
import shutil
import sys

def log_action(message, color="white"):
    """Log con colores"""
    colors = {
        "green": "\033[92m✅",
        "red": "\033[91m❌", 
        "yellow": "\033[93m⚠️",
        "blue": "\033[94mℹ️",
        "white": "\033[0m📋"
    }
    print(f"{colors[color]} {message}\033[0m")

def safe_remove(path):
    """Elimina archivos/directorios de forma segura"""
    try:
        if os.path.isfile(path):
            os.remove(path)
            log_action(f"Archivo eliminado: {path}", "green")
        elif os.path.isdir(path):
            shutil.rmtree(path)
            log_action(f"Directorio eliminado: {path}", "green")
        return True
    except Exception as e:
        log_action(f"Error eliminando {path}: {e}", "red")
        return False

def main():
    """Función principal de limpieza"""
    print("🚀 Iniciando organización del proyecto LUSTPLACE...\n")
    
    # Detener servidor si está corriendo
    log_action("Deteniendo servidores Django...", "blue")
    os.system("pkill -f 'manage.py runserver'")
    
    # Archivos de documentación obsoletos a eliminar
    docs_to_remove = [
        "CSS_CHANGES_SUMMARY.md",
        "ERROR_FIX_NAMESPACE.md", 
        "MIGRATION_SUMMARY.md",
        "PERFIL_USUARIO_README.md",
        "UI_UX_IMPROVEMENTS_SUMMARY.md",
        "data_backup.json",
        "cleanup_project.py",
        "migrate_to_postgres.py"
    ]
    
    # Templates obsoletos (usamos base_hentai_modern.html como principal)
    templates_to_remove = [
        "templates/base_modern.html",
        "templates/productos/lista_modern.html",
        "templates/productos/categoria_productos.html"  # usa base_modern
    ]
    
    # Archivos Python de configuración temporal
    python_files_to_remove = [
        "crear_categorias.py"
    ]
    
    log_action("🗑️  Eliminando archivos de documentación obsoletos...", "yellow")
    for doc in docs_to_remove:
        if os.path.exists(doc):
            safe_remove(doc)
    
    log_action("🗑️  Eliminando templates obsoletos...", "yellow") 
    for template in templates_to_remove:
        if os.path.exists(template):
            safe_remove(template)
    
    log_action("🗑️  Eliminando archivos Python temporales...", "yellow")
    for py_file in python_files_to_remove:
        if os.path.exists(py_file):
            safe_remove(py_file)
    
    # Crear estructura organizada
    log_action("📁 Creando estructura organizada...", "blue")
    
    # Crear directorio docs organizado
    docs_dir = "docs"
    os.makedirs(docs_dir, exist_ok=True)
    
    # Limpiar archivos __pycache__ y .pyc
    log_action("🧹 Limpiando archivos cache de Python...", "yellow")
    for root, dirs, files in os.walk("."):
        for dir_name in dirs[:]:  # Copiar la lista para modificarla
            if dir_name == "__pycache__":
                cache_path = os.path.join(root, dir_name)
                safe_remove(cache_path)
                dirs.remove(dir_name)  # No seguir explorando este directorio
    
    print("\n" + "="*50)
    log_action("✨ Limpieza completada exitosamente", "green")
    log_action("📝 Ahora se creará el README actualizado", "blue")
    print("="*50)

if __name__ == "__main__":
    main()
