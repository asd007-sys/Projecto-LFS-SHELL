import os
import sys

"""

    Función built-in mdkir
               
         - Crea directorio con nombre ingresado
         - Maneja errores, directorio existentes o falta de privilegio
         
         
"""



def mkdir(args):

    if not args: #Si no se ingreso un argumento para el nombre del directorio
        print( "Falta ingresar el nombre del directorio a crear")
        return #Volver al shell

    directorio = args[0] #Nombre del directorio a crear

    try:
        os.mkdir(directorio)   #Crear el directorio con el nombre pasado por argumento
        print(f"Directorio creado: {directorio}")
    except FileExistsError:  #Error de que ya existe el directorio
        print( f"ERROR, Directorio ya existe: {directorio}, ingresar un nombre no existente")
    except PermissionError: #Error de que no tiene los privilegios para crearlo
        print( "ERROR, Permiso denegado, no tiene suficientes privilegios")


"""
               
    Función built-in rm
               
         - Borra archivo
         - Obliga al usuario a confirmar la eliminacion del archivo
         - Manejo de errores
               
"""


def rm(args):
    if not args:  # El primer argumento es la direccion del archivo a borrar,si no existe, avisar al usuario
        print("Le falto ingresar la ruta absoluta o relativa del archivo a borrar ")
        return #Retorna al shell

    archivo = args[0]  # Obtener la direccion y nombre del archivo a borrar

    if os.path.isdir(archivo): #Verificar antes de confirmar si es un directorio, y avisar al usuario que solo puede borrar archivos
        print("El comando solo soporta eliminar archivos, por favor solo ingresar archivos")
        return

    # Prompt de confirmacion a borrar el archivo
    confirmacion = input(f" ¿Esta seguro que desea borrar '{archivo}'? [s/n]: ").lower().strip()

    if confirmacion != 's':  # Si el usuario confirma que quiere borar el archivo
        print(" Operacion cancelada por el usuario.")
        return  # Retornar al shell, evitar continuar con la eliminacio
    try:
        os.unlink(archivo)  # Llamada al sistema para borar el archivo
        print(f"Archivo eliminado: {archivo}")

    except FileNotFoundError:  # Archivo no existe
        print(f"El Archivo ingresado no existe: {archivo}")
    except PermissionError:  # El usuario no tiene los privilegios necesario para borrar
        print("Usted carece de privilegios para borrar el archivo")



"""
   Función built-in cp

        - Copia archivos
        - Precisa de exactamente dos argumentos, el primero a copiar, el segundo donde crear el archivo copiado
        - Permite uso de direcciones relativas
        - Bloque de 1 Megabyte , permite copiar archivos grandes


"""


def cp(args):
    if (len(args) != 2):  # Si la cantidad de argumentos recibidos es diferente a 2, se abandona la funcion
        print(
            "Esta funcion precisa de dos argumentos,primero: la ruta del archivo a copiar, segundo: la ruta del archivo a ser creado")
        return  # Abandonamos
    else:

        origen = os.path.abspath(args[0])  # Argumento recibido como direccion y nombre del archivo a copiar
        destino = os.path.abspath(args[1])  # Argumento recibido como direccion y nombre del archivo creado

        try:

            with open(origen, "rb") as a_origen:  # Abrir en lectura, para copiar archivo
                with open(destino, "wb") as a_destino:  # Abrir en modo escritura, para el archivo

                    Bloque_grande = 1000000  # Tamaño asignado del bloque a leer y escribir

                    while True:  # Loop de i/o

                        datos = a_origen.read(Bloque_grande)  # Leer un bloque del archivo en origen

                        if not datos:  # Si llegamos al fin del archivo origen, datos va a estar vacio,condicion de salida
                            break  # Escapamos del bucle

                        a_destino.write(datos)  # Se escribe al archivo destino el bloque leido

            print(f"Copia exitosa de '{origen}' a '{destino}'")

        except FileNotFoundError:  # Si no se encuentra el archivo a copiar
            print(f"Error: El archivo de origen '{origen}' no fue encontrado.")
        except PermissionError:  # Si no se puede acceder  por falta de privilegio el archivo a copiar
            print(f"Error: No tiene los privilegios suficientes para copiar en {destino}' ")
        except OSError as e:  # Error generico
            print(f"Ocurrió un error durante la copia: {e}")


"""

     Función built-in cd

        - Cambia de directorio al ingresar en el shell: cd Directorio-a-cambiar
        - Al ingresar solo el comando cd, se permanece en el directorio actual y se le avisa al usuario.
        - Informa al usuario si el directorio al que quiere cambiar, no existe o esta vacio.
        - Permite usos de rutas relativas

"""


def cd(args):
    if args:  # Si la lista no esta vacia
        nuevo_dir = (args[0])  # El directorio ingresado por el usuario por argumento
    else:  # Si la lista esta vacia
        print(f"Usted reside en el directorio {os.getcwd()}")
        nuevo_dir = "."  # La variable es asignada el directorio actual.

    try:
        os.chdir(nuevo_dir)  # Cambiar de directorio a la que se paso como argumento
        print(f"EXITO Cambio a {os.getcwd()}")  # Imprimir exito para debug
    except FileNotFoundError:  # Atrapar error si no encuentra o existe el directorio
        print(f"ERROR Directorio no encontrado: {nuevo_dir}")
    except OSError as e:  # Error generico
        print(f"Ocurrió un error durante la copia: {e}")


"""

    Función built-in ls

    - Muestra los archivos y directorios y los discierne
    - Permite mostrar los archivos en el directorio actual o en el directorio recibido por argumento.
    - Informa al usuario si el directorio no existe o si esta vacio

"""


def ls(args):
    ruta = "."
    if args:
        ruta = args[
            0]  # Determina la ruta a listar. Si args tiene elementos (if args),elige el primer elemento (args[0]) como la ruta, osino , usa el directorio actual .

    try:  # Para atrapar errores si los hay
        elementos = os.listdir(ruta)  # Listar todos los archivos y directorios en la direccion ruta
        if ruta == '.':
            print(f"Contenido de '{os.getcwd()}':")
        else:
            print(f"Contenido de '{ruta}':")
        if elementos:  # Si elementos contiene al menos un archivo o directorio
            for elem in elementos:  # Loop para determinar directorios
                if os.path.isdir(os.path.join(ruta,
                                              elem)):  # Se verifica si el archivo actual es o no un directorio , se arma la ruta(Direccion) + archivo, y checkea si es un directorio
                    print(f"  [Dir]  {elem}")
                else:  # Si no es un directorio el archivo actual
                    print(f"  [Arc] {elem}")
            return
        else:  # Si elemento esta vacio
            print("El directorio esta vacio!")
    except FileNotFoundError as e:  # Si no existe o no se encuentra el archivo
        print(f" El directorio {ruta} no existe o no se puede acceder ")
    except OSError as e:  # Error generico
        print(f"Ocurrió un error durante la copia: {e}")


"""
    Parseador Basico:

    - Segmentar el input recibido en tokens,y retornalos todos separados en un array.
    - Manejo de comillas
    - Manejo del caracter de escape

"""


def parseador(linea_comando):
    tokens = []  # Array final del tokens parseados
    token_actual = ""  # Acumilador del token de construcción
    entre_comillas = False  # Estado dentro de comillas dobles, true adentro, false afuera
    proximo_escape = False  # True: siguiente caracter literal, False: normal

    for caracter in linea_comando:  # Leer caracter por caracter
        if proximo_escape:
            # Agregar literalmente independientemente del contexto
            token_actual += caracter  # Se agrega el caracter a token_actual
            proximo_escape = False  # Se resetea el flag
        elif caracter == '\\':
            proximo_escape = True  # Se setea el flag
        elif caracter == '"':
            # Estado de comillas
            entre_comillas = not entre_comillas  # Se le da el valor booleano opuesto del valor actual del flag
        elif caracter.isspace() and not entre_comillas:
            # Fin de token por espacio, solo si no estamos entre comillas
            if token_actual:
                tokens.append(token_actual)  # Se terminó el token, se agrega al arrays de tokens
                token_actual = ""  # Comenzamos un nuevo token
        else:
            # Caracter normal - agregar al token actual
            token_actual += caracter
    # Agregar el último token si queda alguno, por las dudas.
    if token_actual:
        tokens.append(token_actual)

    return tokens  # Se retorna el array con los tokens


"""
    Ejecutador de programas externo:

    -Clona el shell,asigna pid correcto a cada instancia
    -La memoria donde esta el codigo es remplazado por el comando a ejectuar
    -El padre espera a que el hijo se termine de ejecutar, para evitar procesos zombie

"""


def ejecutar_externo(comando,
                     argumentos):  # Permite al ejecutar programas externo,mediante clonacion y remplazo de codigo,datos en la memoria del proceso hijo

    try:
        pid = os.fork()  # Clona el Shell , el hijo recibe 0 en pid(el clon), y el Padre un numero positivo(Pid del hijo)
    except OSError as e:
        print(f"Error al crear proceso (fork): {e}")  # Error al clonar
        return
    if pid == 0:  # Si se ejecuta actualmente el hijo
        try:
            argv = [comando] + argumentos  # Llenamos un array con el comando primero, seguido por los argumentos
            os.execvp(comando,
                      argv)  # Reemplazamos el codigo en el espacio de memoria del hijo, por el proceso externo que se quiere ejecutar
        except FileNotFoundError:
            print(f"Error: El comando '{comando}' no fue encontrado en el sistema.")
            sys.exit(127)  # Código estándar linux para "Command not found"
        except Exception as e:
            print(f"Error al ejecutar: {e}")
            sys.exit(1)  # Salir con error genérico
    else:  # Se ejecuta actualmente el proceso Padre

        try:
            _, status = os.waitpid(pid, 0)  # El padre se bloquea , y espera a que el hijo termine de correr.
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

            # Parsear comando usando el parseador propio,recibimos el array
            partes = parseador(comando)

            if not partes:
                continue  # Ignorar si el parseador no devolvió tokens (ej: solo un '\' o espacios)

            comando_principal = partes[0]  # El primer elemento del array es el comando principal
            argumentos = partes[1:]  # Los siguientes se asumen como argumentos

            # Ejecutar comandos built-in
            if comando_principal == "exit":
                print("¡Hasta luego!")
                break
            elif comando_principal == "mkdir":
                mkdir(argumentos)

            elif comando_principal == "ls":
                ls(argumentos)

            elif comando_principal == "cd":
                cd(argumentos)

            elif comando_principal == "cp":
                cp(argumentos)

            elif comando_principal == "rm":
                rm(argumentos)

            elif comando_principal == "pwd":
                # Implementación manual del comando pwd
                print(os.getcwd())

            else:
                # Si no existe el commando
                ejecutar_externo(comando_principal, argumentos)  # Funcion nueva

        except KeyboardInterrupt:
            # Manejo de Ctrl+C - Termina de forma alterna
            print("\n¡Hasta luego! (Terminado con Ctrl + C!)")
            break


if __name__ == "__main__":  # Si se abre el archivo, se corre main automaticamente, si se importa se puede usar parseador por si solo
    main()