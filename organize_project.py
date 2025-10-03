#!/usr/bin/env python3
"""
Script de organización y limpieza del proyecto LUSTPLACE
Elimina archivos obsoletos y reorganiza la estructura.
"""

import os
import shutil
import sys

def delete_file_or_folder(path):
    """Elimina archivo o carpeta si existe."""
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
            print(f"✅ Eliminada carpeta: {path}")
        else:
            os.remove(path)
            print(f"✅ Eliminado archivo: {path}")
    else:
        print(f"⚠️ No existe: {path}")

def organize_project():
    """Organiza y limpia el proyecto."""
    
    print("🧹 Iniciando limpieza y organización del proyecto LUSTPLACE...")
    
    # Archivos de documentación temporal/obsoletos
    files_to_remove = [
        "CSS_CHANGES_SUMMARY.md",
        "ERROR_FIX_NAMESPACE.md", 
        "MIGRATION_SUMMARY.md",
        "PERFIL_USUARIO_README.md",
        "UI_UX_IMPROVEMENTS_SUMMARY.md",
        "cleanup_project.py",  # Script anterior
        "migrate_to_postgres.py",
        "data_backup.json"
    ]
    
    # Apps que no se usan más
    unused_apps = [
        "login",  # Funcionalidad movida a authentication
        "VirtualR"  # No se usa
    ]
    
    # Templates obsoletos
    unused_templates = [
        "templates/base_modern.html",  # Solo usamos base_hentai_modern.html
        "templates/productos/lista_modern.html",
        "templates/productos/categoria_productos.html",
        # Mantener templates/Login/ por ahora hasta confirmar migración completa
    ]
    
    print("\n📁 Eliminando archivos obsoletos...")
    for file in files_to_remove:
        delete_file_or_folder(file)
    
    print("\n📦 Eliminando apps no utilizadas...")
    for app in unused_apps:
        delete_file_or_folder(app)
    
    print("\n🎨 Eliminando templates obsoletos...")
    for template in unused_templates:
        delete_file_or_folder(template)
    
    # Crear carpeta de documentación organizada
    if not os.path.exists("docs"):
        os.makedirs("docs")
        print("✅ Creada carpeta docs/")
    
    print("\n📚 Organizando documentación...")
    
    # Mover archivos importantes a docs/
    if os.path.exists("docs/project_structure.md"):
        print("📄 project_structure.md ya existe en docs/")
    
    print("\n🎉 ¡Limpieza completada!")
    print("\n📋 Estructura resultante:")
    print("""
    LUSTPLACE/
    ├── authentication/          # 👤 Sistema de usuarios y autenticación
    ├── Carrito/                # 🛒 Carrito de compras
    ├── payments/               # 💳 Procesamiento de pagos
    ├── productos/              # 📦 Gestión de productos y categorías
    ├── marketplace_lust/       # ⚙️ Configuración principal Django
    ├── templates/              # 🎨 Plantillas HTML
    ├── static/                 # 📁 Archivos estáticos (CSS, JS, img)
    ├── media/                  # 📸 Archivos subidos por usuarios
    ├── docs/                   # 📚 Documentación del proyecto
    └── requirements.txt        # 📋 Dependencias Python
    """)

if __name__ == "__main__":
    # Cambiar al directorio del proyecto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Confirmar antes de proceder
    print("⚠️ Este script eliminará archivos obsoletos del proyecto.")
    response = input("¿Continuar? (s/N): ").strip().lower()
    
    if response in ['s', 'si', 'yes', 'y']:
        organize_project()
    else:
        print("❌ Operación cancelada.")
