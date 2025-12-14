import os
import sys
from io import StringIO


from shell import ls,parseador


def pruebas_automaticas(comandos):
   
  
 
    print("PRUEBAS AUTOMÁTICAS DEL SHELL")

    # Loopear sobre cada comando en la lista de comandos
    for comando in comandos:
        
        print(f"EduShell [{os.getcwd()}] > {comando}")
        
        # Verificar si el comando esta vacio
        if not comando.strip():
            continue

        # Parsear el comando usando la funcion parseador del shell
        partes = parseador(comando)

        # Si esta vacio, volver al menu principal a esperar un comando
        if not partes:
            continue

        # Obtener el comando principal 
        comando_principal = partes[0]
        # Obtener los argumentos
        argumentos = partes[1:]
      
        if comando_principal == "exit":
            print("¡Hasta luego!")
            break

        elif comando_principal == "ls":
            ls(argumentos)

        elif comando_principal == "pwd":
            print(os.getcwd())
        # Si no es un comando built-in
        else:
            print("Es una prueba solo para ls")
        
        print()

    print("Pruebas completadas.")


if __name__ == "__main__":
    # Lista de comandos a ejecutar automáticamente
    comandos_a_ejecutar = [
        "ls", 
        "ls /",
        "ls /pokemon",
        "ls /vacio",
        "exit"
    ]
    
    pruebas_automaticas(comandos_a_ejecutar)