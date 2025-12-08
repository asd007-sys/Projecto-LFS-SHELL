import sys
import os

# Añadir el directorio src al path para poder importar
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from shell import parseador

def test_parseador():
    entradas = [
        "pwd hola",
        'echo "hola mundo"',
        '\\\"hola\\\"',
        '"hola"',
        '\\',
    ]

    print("=== Pruebas del parseador ===")
    for e in entradas:
        resultado = parseador(e)
        print(f"'{e}' => {resultado}")
    print("=============================")

if __name__ == "__main__":
    test_parseador()