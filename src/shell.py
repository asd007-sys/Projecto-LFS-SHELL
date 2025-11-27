
import os





def main():
    """
    Función principal del REPL

    - Muestra el directorio actual
    - Manejo de señal ( Ctrl+C)
    - Ejecuta comandos built-in
    - Sistema de salida

    Comandos implementados hasta ahora:
    - pwd: Muestra el directorio de trabajo actual
    - exit: Termina el shell


    """
    print("Bienvenido a EduShell - Shell Educativo Universitario")
    print("Escribe 'exit' para salir\n")

    while True:
        try:

            # Leer comando del usuario mostrando la dirección actual en el prompt
            comando = input(f"EduShell [{os.getcwd()}] > ").strip()

            # Ignorar líneas vacías
            if not comando:
                continue


            # Ejecutar comandos built-in
            if comando == "exit":
                print("¡Hasta luego!")
                break

            elif comando == "pwd":
                # Implementación manual del comando pwd
                print(os.getcwd())

            else:
                #Si no existe el commando
                print(f"Comando no implementado: {comando}")

        except KeyboardInterrupt:
            # Manejo de Ctrl+C - Termina de forma alterna
            print("\n¡Hasta luego! (Terminado con Ctrl + C!)")
            break


if __name__ == "__main__":
    main()
