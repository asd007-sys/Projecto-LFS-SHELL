
import os
import sys

"""

    Función built-in ls

    - Muestra los archivos y directorios y los discierne
    - Permite mostrar los archivos en el directorio actual o en el directorio recibido por argumento.
    - Informa al usuario si el directorio no existe o si esta vacio
    
"""

def ls(args):
    ruta = "."
    if args:
        ruta = args[0] #Determina la ruta a listar. Si args tiene elementos (if args),elige el primer elemento (args[0]) como la ruta, osino , usa el directorio actual .  

    try:  #Para atrapar errores si los hay
        elementos = os.listdir(ruta) #Listar todos los archivos y directorios en la direccion ruta   
        if ruta == '.':
            print(f"Contenido de '{os.getcwd()}':")
        else:
            print(f"Contenido de '{ruta}':")
        if elementos: #Si elementos contiene al menos un archivo o directorio
            for elem in elementos: #Loop para determinar directorios  
                if os.path.isdir(os.path.join(ruta,elem)): #Se verifica si el archivo actual es o no un directorio , se arma la ruta(Direccion) + archivo, y checkea si es un directorio
                    print(f"  [Dir]  {elem}")
                else:   #Si no es un directorio el archivo actual
                    print(f"  [Arc] {elem}")
            return 
        else: #Si elemento esta vacio
            print("El directorio esta vacio!")
    except FileNotFoundError as e: #Si no existe o no se encuentra el archivo
        print(f" El directorio {ruta} no existe o no se puede acceder ")
    except OSError as e: #Si hay algun error,se ejecuta esto
        return "ERROR", str(e)
    




"""
    Parseador Basico:

    - Segmentar el input recibido en tokens,y retornalos todos separados en un array.
    - Manejo de comillas
    - Manejo del caracter de escape
  
"""


def parseador(linea_comando):


    tokens = [] # Array final del tokens parseados
    token_actual = "" # Acumilador del token de construcción
    entre_comillas = False # Estado dentro de comillas dobles, true adentro, false afuera
    proximo_escape = False # True: siguiente caracter literal, False: normal


    for caracter in linea_comando: # Leer caracter por caracter
        if proximo_escape:
            # Agregar literalmente independientemente del contexto
            token_actual += caracter # Se agrega el caracter a token_actual
            proximo_escape = False # Se resetea el flag
        elif caracter == '\\':
            proximo_escape = True # Se setea el flag
        elif caracter == '"':
            # Estado de comillas
            entre_comillas = not entre_comillas # Se le da el valor booleano opuesto del valor actual del flag
        elif caracter.isspace() and not entre_comillas:
            # Fin de token por espacio, solo si no estamos entre comillas
            if token_actual:
                tokens.append(token_actual) # Se terminó el token, se agrega al arrays de tokens
                token_actual = "" # Comenzamos un nuevo token
        else:
            # Caracter normal - agregar al token actual
            token_actual += caracter
    # Agregar el último token si queda alguno, por las dudas.
    if token_actual:
            tokens.append(token_actual)

    return tokens # Se retorna el array con los tokens

"""
    Ejecutador de programas externo:
    
    -Clona el shell,asigna pid correcto a cada instancia
    -La memoria donde esta el codigo es remplazado por el comando a ejectuar
    -El padre espera a que el hijo se termine de ejecutar, para evitar procesos zombie
    
"""



def ejecutar_externo(comando, argumentos):   #Permite al ejecutar programas externo,mediante clonacion y remplazo de codigo,datos en la memoria del proceso hijo
   
    try: 
        pid = os.fork()    # Clona el Shell , el hijo recibe 0 en pid(el clon), y el Padre un numero positivo(Pid del hijo)
    except OSError as e:
        print(f"Error al crear proceso (fork): {e}")  # Error al clonar
        return
    if pid == 0:   # Si se ejecuta actualmente el hijo
        try: 
            argv = [comando] + argumentos # Llenamos un array con el comando primero, seguido por los argumentos
            os.execvp(comando, argv) # Reemplazamos el codigo en el espacio de memoria del hijo, por el proceso externo que se quiere ejecutar 
        except FileNotFoundError:
            print(f"Error: El comando '{comando}' no fue encontrado en el sistema.")
            sys.exit(127) # Código estándar linux para "Command not found"
        except Exception as e:
            print(f"Error al ejecutar: {e}")
            sys.exit(1) # Salir con error genérico
    else: # Se ejecuta actualmente el proceso Padre
 
        try:
            _, status = os.waitpid(pid, 0) # El padre se bloquea , y espera a que el hijo termine de correr.  
        except KeyboardInterrupt:
            # Si el usuario hace Ctrl+C mientras corre el programa externo,
            # Se atrapa el error para que no se cierre el shell, solo deje de esperar.
            print("\nPrograma interrumpido.")


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

            #Parsear comando usando el parseador propio,recibimos el array
            partes = parseador(comando)

            if not partes:
                continue  # Ignorar si el parseador no devolvió tokens (ej: solo un '\' o espacios)


            comando_principal = partes[0] # El primer elemento del array es el comando principal
            argumentos = partes[1:] #Los siguientes se asumen como argumentos


            # Ejecutar comandos built-in
            if comando_principal == "exit":
                print("¡Hasta luego!")
                break
            elif comando_principal == "ls":
                ls(argumentos)
                

            elif comando_principal == "pwd":
                # Implementación manual del comando pwd
                print(os.getcwd())

            else:
                #Si no existe el commando
                ejecutar_externo(comando_principal, argumentos) #Funcion nueva

        except KeyboardInterrupt:
            # Manejo de Ctrl+C - Termina de forma alterna
            print("\n¡Hasta luego! (Terminado con Ctrl + C!)")
            break


if __name__ == "__main__":    # Si se abre el archivo, se corre main automaticamente, si se importa se puede usar parseador por si solo
    main()