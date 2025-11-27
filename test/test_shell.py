import io 
import sys 
from shell import main 

def test_pwd_exit():

    # Simular entradas
    simulado = io.StringIO("pwd\nexit\n") 
    sys.stdin = simulado 

    # Capturar salidas
    salida = io.StringIO() 
    sys.stdout = salida 

    # Ejecutar shell
    main() 

    # Restaurar stdin/stdout
    sys.stdin = sys.__stdin__
    sys.stdout = sys.__stdout__

    # Mostrar salida capturada
    print("=== SALIDA CAPTURADA ===")
    print(salida.getvalue())

if __name__ == "__main__":
    test_pwd_exit()