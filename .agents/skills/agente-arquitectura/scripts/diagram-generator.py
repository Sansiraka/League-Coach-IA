#!/usr/bin/env python3
"""Generador de diagramas Mermaid a partir de estructura de código.

Este script analiza la estructura de directorios de un proyecto
y genera un diagrama Mermaid representando los componentes y sus relaciones.

Uso:
    python diagram-generator.py /ruta/al/proyecto
    python diagram-generator.py /ruta/al/proyecto --output diagrama.md
    python diagram-generator.py /ruta/al/proyecto --type sequence
"""

import os
import sys
import argparse
from pathlib import Path


def analizar_estructura(ruta: str, max_profundidad: int = 3) -> dict:
    """Analiza la estructura de directorios de un proyecto.
    
    Args:
        ruta: Ruta al directorio raíz del proyecto.
        max_profundidad: Profundidad máxima de análisis.
        
    Returns:
        Diccionario con la estructura del proyecto.
    """
    estructura = {
        "nombre": os.path.basename(ruta),
        "tipo": "directorio",
        "hijos": [],
    }
    
    # Directorios a ignorar
    ignorar = {
        "node_modules", ".git", "__pycache__", ".venv", "venv",
        "dist", "build", ".next", "coverage", ".pytest_cache",
    }
    
    if max_profundidad <= 0:
        return estructura
    
    try:
        for item in sorted(os.listdir(ruta)):
            if item.startswith(".") and item not in {".env.example"}:
                continue
            if item in ignorar:
                continue
                
            ruta_completa = os.path.join(ruta, item)
            
            if os.path.isdir(ruta_completa):
                hijo = analizar_estructura(ruta_completa, max_profundidad - 1)
                estructura["hijos"].append(hijo)
            else:
                estructura["hijos"].append({
                    "nombre": item,
                    "tipo": "archivo",
                    "extension": Path(item).suffix,
                })
    except PermissionError:
        pass
    
    return estructura


def generar_mermaid_componentes(estructura: dict) -> str:
    """Genera un diagrama de componentes Mermaid.
    
    Args:
        estructura: Diccionario con la estructura del proyecto.
        
    Returns:
        String con el diagrama Mermaid.
    """
    lineas = ["graph TB"]
    contador = [0]
    
    def _procesar(nodo, padre_id=None):
        nodo_id = f"n{contador[0]}"
        contador[0] += 1
        
        if nodo["tipo"] == "directorio":
            nombre = nodo["nombre"]
            num_archivos = len([h for h in nodo.get("hijos", []) if h["tipo"] == "archivo"])
            num_dirs = len([h for h in nodo.get("hijos", []) if h["tipo"] == "directorio"])
            
            etiqueta = f"{nombre}"
            if num_archivos > 0:
                etiqueta += f"\\n({num_archivos} archivos)"
            
            lineas.append(f'    {nodo_id}["{etiqueta}"]')
            
            if padre_id:
                lineas.append(f"    {padre_id} --> {nodo_id}")
            
            for hijo in nodo.get("hijos", []):
                if hijo["tipo"] == "directorio":
                    _procesar(hijo, nodo_id)
    
    _procesar(estructura)
    return "\n".join(lineas)


def generar_mermaid_tree(estructura: dict) -> str:
    """Genera un diagrama tipo árbol con Mermaid.
    
    Args:
        estructura: Diccionario con la estructura del proyecto.
        
    Returns:
        String con el diagrama Mermaid.
    """
    lineas = ["graph LR"]
    contador = [0]
    
    def _procesar(nodo, padre_id=None):
        nodo_id = f"n{contador[0]}"
        contador[0] += 1
        
        nombre = nodo["nombre"]
        
        if nodo["tipo"] == "directorio":
            lineas.append(f'    {nodo_id}["📁 {nombre}"]')
        else:
            ext = nodo.get("extension", "")
            icono = {
                ".py": "🐍", ".js": "📜", ".ts": "📘",
                ".html": "🌐", ".css": "🎨", ".json": "📋",
                ".md": "📝", ".yml": "⚙️", ".yaml": "⚙️",
            }.get(ext, "📄")
            lineas.append(f'    {nodo_id}["{icono} {nombre}"]')
        
        if padre_id:
            lineas.append(f"    {padre_id} --> {nodo_id}")
        
        for hijo in nodo.get("hijos", []):
            _procesar(hijo, nodo_id)
    
    _procesar(estructura)
    return "\n".join(lineas)


def main():
    parser = argparse.ArgumentParser(
        description="Genera diagramas Mermaid a partir de la estructura del proyecto."
    )
    parser.add_argument("ruta", help="Ruta al directorio del proyecto")
    parser.add_argument(
        "--output", "-o",
        help="Archivo de salida (default: stdout)",
        default=None,
    )
    parser.add_argument(
        "--type", "-t",
        choices=["components", "tree"],
        default="components",
        help="Tipo de diagrama a generar",
    )
    parser.add_argument(
        "--depth", "-d",
        type=int,
        default=3,
        help="Profundidad máxima de análisis (default: 3)",
    )
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.ruta):
        print(f"Error: '{args.ruta}' no es un directorio válido.", file=sys.stderr)
        sys.exit(1)
    
    estructura = analizar_estructura(args.ruta, args.depth)
    
    if args.type == "components":
        diagrama = generar_mermaid_componentes(estructura)
    else:
        diagrama = generar_mermaid_tree(estructura)
    
    resultado = f"```mermaid\n{diagrama}\n```"
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(resultado)
        print(f"Diagrama guardado en: {args.output}")
    else:
        print(resultado)


if __name__ == "__main__":
    main()
