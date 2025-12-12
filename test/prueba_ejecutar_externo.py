#!/usr/bin/env python3
"""
Script de prueba simple para ejecutar_externo
Probado en Rocky Linux 10
"""
from shell import ejecutar_externo

print("PRUEBA RÁPIDA ejecutar_externo")
print("=" * 40)

# Prueba 1: Comando que existe
print("\n1. Probando 'echo':")
ejecutar_externo("echo", ["¡Funciona!", "Perfecto"])

# Prueba 2: Comando con argumentos
print("\n2. Probando 'cat' con argumentos:")
ejecutar_externo("cat", ["prueba_ejecutar_externo.py"])

# Prueba 3: Comando que NO existe
print("\n3. Probando comando inexistente:")
ejecutar_externo("comando_falso_123", [])

