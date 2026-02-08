import os
import sys
from datetime import datetime

"""
    SISTEMA DE LOGGER

    - Registra acciones en /var/log/shell/shell.log
    - Registra errores en /var/log/shell/sistema_error.log
    - Incluye timestamp, usuario, comando, resultado y mensaje

"""

"""
   Crea el directorio de logs si es que no existe.
   Si no tiene permisos, trata de crear en el directorio actual.
"""

Logger_Direccion = "/var/log/shell/"  # Direccion de los archivos de logger
Logger_Acciones = os.path.join(Logger_Direccion, "shell.log")  # ruta completa del archivo de logger para acciones
Logger_Errores = os.path.join(Logger_Direccion, "sistema_error.log")  # ruta completa del rchivo de logger para errores


def iniciar_logs():
    global Logger_Direccion, Logger_Acciones, Logger_Errores

    try:

        if not os.path.exists("/var"):  # Si no existe el diretorio /var, seria peculiar en linux,pero para prevenir problemas
            os.mkdir("/var") # Se crea el directorio /var

        if not os.path.exists("/var/log"):  # Si no existe el diretorio /var/log, crearlo
            os.mkdir("/var/log") # Se crea el directorio /var/log

        if not os.path.exists(Logger_Direccion):  # Si no existe el diretorio final, crearlo
            os.mkdir(Logger_Direccion) # Se crea el directorio /var/log/shell

        with open(Logger_Acciones, "a") as f:  # Verificar tener permiso suficiente para poder escribir
            pass    #Si se tiene suficientes permisos , seguir

    except PermissionError:  # Si el usuario no tiene los privilegios necesarios

        print("\nNo tiene privilegios para acceder a /var/log/shell \n")
        print("Los logs se guardaran en home/user/log/shell\n")

        Logger_Direccion = f"/home/{os.getenv('USER')}/log/shell"  # Direccion nueva del directorio de los logs
        Logger_Acciones = os.path.join(Logger_Direccion, "shell.log")  # Direccion del archivo logger de acciones
        Logger_Errores = os.path.join(Logger_Direccion, "sistema_error.log")  # Direccion del archivo logger de errores

        if not os.path.exists(f"/home/{os.getenv('USER')}/log/"):  # Si el directorio log no existe en el home del usuario
            os.mkdir(f"/home/{os.getenv('USER')}/log/") # Crear directorio

        if not os.path.exists(Logger_Direccion):  # Si el directorio shell no existe en el directorio log previo
            os.mkdir(Logger_Direccion) # Crear directorio



def registrar_accion(comando, args, exito, mensaje):  # Recibe el comando y lo registra
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Crear timestamp con formato ano/mes/dia hora:minutos:segundos
        usuario = os.getenv("USER") or os.getenv("USERNAME") or "Estudiante"  # Nombre del usuario para registrar
        if exito:  # Si el comando a registrar funciono correctamente
            resultado = "EXITO"
        else:  # Si el resultado del comando es un error
            resultado = "FRACASO"

        formateado = f"[{timestamp}] {usuario} | {comando + (' ' + ' '.join(args) if args else '')} | {resultado}"  # Formateo de la linea a registrar, Timestamp , Nombre ususario , comando y argumentos, Exito o Fracaso
        # condicional, si args esta vacio es '',string vacio, si no ,entonces ' '.join(args) agrega los argumentos separado por espacio
        if mensaje:  # Si existe mensaje de error para agregar
            formateado += f" | {mensaje}"  # Se le concatena al final el mensaje
        formateado += "\n"  # Siempre la variable formateado termina con caracter de nueva linea

        with open(Logger_Acciones, "a") as f:  # Abrir el archivo de logs de acciones como append, agregar al final
            f.write(formateado)  # Escribir la formateado en log
    except Exception as e:
        # Si falla el log, no interrumpir el shell
        pass


def mostrar_logs(tipo):
    try:
        if tipo == "acciones":
            archivo = Logger_Acciones  # Si el usuario ingresa ver logs,tipo = acciones
            nombre = "ACCIONES"
        else:
            archivo = Logger_Errores  # Si ingresa ver_erroes, tipo=errores
            nombre = "ERRORES"

        if not os.path.exists(archivo):  # Verificar si el archivo esta vacio
            print(f"No hay log de {nombre.lower()} todavia")
            return  # Se retorna al menu principal

        with open(archivo, "r") as f:  # Se abre el archivo en modo lectura
            lineas = f.readlines()  # Se guarda todo el archivo en un array, cada elemento es una linea

        print(f"\n=== LOG DE {nombre} ({len(lineas)} entradas) ===\n")

        for linea in lineas[-30:]:  # Mostrar ultimas 30 líneas,para no tener demasiadas lineas
            print(linea.strip())

        print(f"\nArchivo completo: {archivo}")
    except Exception as e:  # En caso de error
        print(f"ERROR al leer logs: {e}")


def registrar_error(comando, args, tipo_error, mensaje_error):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Crear timestamp con formato ano/mes/dia hora:minutos:segundos
        usuario = os.getenv("USER") or os.getenv("USERNAME") or "Estudiante"  # Nombre del usuario para registrar

        formateado = f"[{timestamp}] {usuario} | {comando + (' ' + ' '.join(args) if args else '')} | {tipo_error} | {mensaje_error}\n"  # Formateo de linea a ingresar en Logger_Errores

        with open(Logger_Errores, "a") as f:  # Abrir el archivo para agregar al final del archivo la linea
            f.write(formateado)
    except Exception as e:  # Si falla el log, no interrumpir el shell
        pass


def help(args):
    if not args:
        print("-------------------------------------------------------")
        print("Ingrese help seguido por algunos de los comandos built-in siguentes para averiguar cada uso:")
        print(" - cd,ls,cp,rm,mkdir,cat,pwd,echo,exit,tutorial")
        print("\nEjecución Externa:")
        print(
            " - Cualquier otro comando (como date, nano o top) se ejecuta usando fork/exec.")
        print("-------------------------------------------------------")
        return
    else:
        if args[0] == "cd":
            print(" - cd <ruta>: Cambia el directorio de trabajo.  Ej: cd / \n")
            return
        if args[0] == "ls":
            print(" - ls <ruta>: Lista el contenido de un directorio.  Ej: ls (directorio actual), ls /usr \n")
            return
        if args[0] == "cp":
            print(" - cp <origen> <destino>: Copia archivos byte a byte. Ej cp hola.txt holita.txt (En mismo directorio), cp /usr/hola.txt /home/asd/holita.txt (en directorios diferentes) \n")
            return
        if args[0] == "rm":
            print(" - rm <archivo>: Elimina un archivo. Ej: rm archivo, rm /home/asd/holita.txt \n")
            return
        if args[0] == "mkdir":
            print(" - mkdir <dir>: Crea un directorio. Ej:mkdir asd (crear directorio en directorio actual), mkdir /home/asd/nuevo (crear directorio en ruta ingresada) \n")
            return
        if args[0] == "cat":
            print(" - cat <archivo>: Muestra el contenido del archivo. Ej: cat hola.txt, cat /home/asd/hola.txt \n")
            return
        if args[0] == "pwd":
            print(" - pwd: Muestra la ruta actual. \n")
            return
        if args[0] == "echo":
            print(" - echo <texto>: Imprime texto en consola. Ej: echo (imprime solo una nueva linea), echo asdfg, echo \"imprimir con espacios\" \n")
            return
        if args[0] == "exit":
            print(" - comando para salir del shell \n")
            return
        if args[0] == "tutorial":
            print(" - funcion de tutorial basico del shell \n funciona aunque el comando falle, logrando asi poder seguir el tutorial en caso de falta de privilegios o errores de directorios ya creados. \n")
            return
        else:
            print("El argumento ingresado no es un comando built-in")



PASOS_TUTORIAL = [
    # Lista de tuplas de cada paso del tutorial,valores por tupla: 1ero comando correcto, 2ndo argumentos correctos, 3ro Instruccion del paso, 4to mensaje al cumplir con el requisito
    ("pwd", [], "Escribe 'pwd'", "Perfecto."),
    ("ls", [], "Escribe 'ls'", "Perfecto."),
    ("mkdir", ["asd"], "Escribe 'mkdir asd'", "Has creado la carpeta asd."),
    ("cd", ["asd"], "Escribe 'cd asd' para entrar", "Ya estas dentro."),
    ("touch", ["addy"], "Escribe 'touch addy' para crear archivo nuevo", "Archivo addy creado"),
    ("cp", ["addy", "addyCopia"], "'cp addy addyCopia' para copiar el archivo addy", "Archivo addy copiado"),
    ("rm", ["addy"], "Escribe 'rm addy' para eliminar archivo addy", "Archivo addy eliminado."),
    ("echo", ["Termine el tutorial!"], "Escribe echo \"Termine el tutorial!\" ", "Ultimo paso logrado!.")

]

paso_actual = -1  # -1 signifca fuera del tutorial, diferente a -1 significa dentro del tutorial

"""

    Función tutorial

         - Tutorial de funciones
         - Utiliza lista de tuplas con 4 valores 


"""


def tutorial(comando, args):
    global paso_actual  # Utilizar la variable global

    if paso_actual == -1:  # Si el modo tutorial no esta activo, salir
        return True  # Para funcionamiento esperado de la shell, la llamada de esta funcion corre siempre, si es False o None, el shell no funciona como debe e ignora comandos.

    comando_esperado, argumentos, instruccion, info = PASOS_TUTORIAL[
        paso_actual]  # Asignar a cada varible correspondiente el valor del elemento actual de la tupla

    if comando == comando_esperado and args == argumentos:  # Si el usuario ingreso el comando y los argumentos esperados
        return True  # Permitir ejecucion del comando ingresado
        # La funcion imprimir_info_tutorial se encarga de los mensajes de exito
    else:  # Si el usuario ingreso el comando o  argumentos incorrectos
        if comando == comando_esperado:  # Si el comando ingresado por el usuario es correcto y el argumento  es incorrecto
            print(f" El comando es '{comando_esperado}', pero el argumento debe ser '{' '.join(argumentos)}'")
        else:  # Viceversa
            print(f"Error. Se esperaba '{comando_esperado} {' '.join(argumentos)}'.")
        return False  # Bloquear comando ingresado


"""

    Función ayudante del tutorial

         - Imprime correctamente las intrucciones del proximo paso
         - Encargado de finalizar tutorial


"""


def imprimir_info_tutorial():
    global paso_actual  # Utilizar la variable global
    if paso_actual == -1:  # Si el modo tutorial no esta activo, salir
        return True

    a, b, c, info = PASOS_TUTORIAL[
        paso_actual]  # Solo interesa avisar al usuario la informacion de exito del paso actual, las variables a,b,c no se utilizan
    print(f"\n {info}")  # Imprimir descripcion de exito del paso actual

    paso_actual += 1  # Cargar el indice del proximo paso

    if paso_actual >= len(PASOS_TUTORIAL):  # Si el anterior paso era el ultimo del tutorial, terminar el tutorial
        print("¡Fin del tutorial!\n")
        paso_actual = -1  # Resetar variable para salir del modo tutorial
    else:  # Existe un siguente paso, seguir con el tutorial
        print(f"SIGUIENTE: {PASOS_TUTORIAL[paso_actual][2]}")  # Imprime la instruccion del proximo paso a realizar


"""

    Función built-in echo

         - Imprime los argumentos recibidos separados por un espacio
         - Imprime linea vacia si no se ingresa argumentos, como lo hace echo normalmente
         - Atrapa errores


"""


def echo(args):
    if not args:
        print()  # Imprimir linea vacia si no hay argumentos
        registrar_accion("echo", args, True, "Se imprimio una linea vacia")  # Funcion para registrar accion exitosa
        return  # Volver a menu principal

    try:
        # Si args no esta vacio
        salida = " ".join(args)  # Agregar todos los argumentos separadados por espacio
        print(salida)  # imprimir el texto con los argumentos
        registrar_accion("echo", args, True,
                         "Se imprimio correctamente argumentos ingresado")  # Funcion para registrar accion exitosa
        return  # Volver a menu principal

    except OSError:  # Si salta algun error
        print("Ha ocurrido un error")
        registrar_accion("echo", args, False, "Ha ocurrido un error")  # Funcion para registrar accion fallida
        registrar_error("echo", args, "ErrorGenerico", "Ha ocurrido un error")  # Funcion para regisrar error


"""

    Función built-in cat

         - Abre archivo y lo imprime
         - Maneja archivos grandes eficientemente


"""


def cat(args):
    if not args:  # Si no hay argumento (archivo a leer) recibido en la funcion
        print(
            "Falta ingresar el archivo a leer!, ej: cat libro.txt , cat /home/user/librito.txt")  # Advertir al usuario
        registrar_accion("cat", args, False,
                         "Falta argumento para el nombre del archivo a leer")  # Funcion para registrar accion fallida
        registrar_error("cat", args, "FaltaNombreArchivoALeer",
                        "Falta argumento para el nombre del archivo a leer")  # Funcion para regisrar error
        return  # Volver a menu principal

    archivo = args[0]  # El primer argumento es el archivo
    try:
        with open(archivo, 'r') as zeta:  # Abrir el archivo a leer en modo lectura
            for linea in zeta: #Loopear sobre el archivo por linea
                print(linea.strip())
        print(f"Contenido de {archivo} mostrado")
        registrar_accion("cat", args, True, "Lectura de archivo exitosa")  # Funcion para registrar accion exitosa
        return
    except FileNotFoundError:  # Error de archivo no encontrado
        print(f"Archivo no existe: {archivo}. Puede utilizar el comando ls para verificar nombre o directorio correcto")
        registrar_accion("cat", args, False,
                         "El archivo a leer no existe o no fue encontrado")  # Funcion para registrar accion fallida
        registrar_error("cat", args, "NoSeEncontroArchivoALeer",
                        "El archivo a leer no existe o no fue encontrado")  # Funcion para regisrar error
        return
    except PermissionError:  # Permisos insuficientes
        print("Permiso denegado,no tiene los privilegios necesarios")
        registrar_accion("cat", args, False,
                         "No tiene los privilegios suficientes para leer archivo")  # Funcion para registrar accion fallida
        registrar_error("cat", args, "PermisoInsuficiente",
                        "No tiene los privilegios suficientes para leer archivo")  # Funcion para regisrar error
        return
    except IsADirectoryError: #Es un directorio
        print("Usted no puede leer un directorio")
        registrar_accion("cat", args, False, "No se puede leer un directorio")
        registrar_error("cat", args, "IsADirectoryError","No se puede leer un directorio")


"""

    Función built-in mdkir

         - Crea directorio con nombre ingresado
         - Maneja errores, directorio existentes o falta de privilegio


"""


def mkdir(args):
    if not args:  # Si no se ingreso un argumento para el nombre del directorio
        print("Falta ingresar el nombre del directorio a crear, ej: mkdir nombre123")
        registrar_accion("mkdir", args, False,
                         "Falta argumento para el nombre del directorio a crear")  # Funcion para registrar accion fallida
        registrar_error("mkdir", args, "FaltaNombre",
                        "Falta argumento para el nombre del directorio a crear")  # Funcion para regisrar error
        return  # Volver al shell

    directorio = args[0]  # Nombre del directorio a crear

    try:
        os.mkdir(directorio)  # Crear el directorio con el nombre pasado por argumento
        print(f"Directorio creado: {directorio}")
        registrar_accion("mkdir", args, True, "Creado")  # Funcion para registrar accion exitosa
    except FileExistsError:  # Error de que ya existe el directorio
        print(
            f"ERROR, Directorio ya existe: {directorio}, ingresar un nombre no existente,puede utilizar ls para verificar nombres existentes")
        registrar_accion("mkdir", args, False,
                         "El archivo no existe/no fue encontrado")  # Funcion para registrar accion fallida
        registrar_error("mkdir", args, "FileExistsError", f"Directorio ya existe")  # Funcion para regisrar error
    except PermissionError:  # Error de que no tiene los privilegios para crearlo
        print("ERROR, Permiso denegado, no tiene suficientes privilegios,intente crearlo en otro directorio por favor")
        registrar_accion("mkdir", args, False,
                         "No tiene los privilegios suficientes")  # Funcion para registrar accion fallida
        registrar_error("mkdir", args, "PermissionError",
                        "No tiene los privilegios suficientes")  # Funcion para regisrar error


"""

    Función built-in rm

         - Borra archivo
         - Obliga al usuario a confirmar la eliminacion del archivo
         - Manejo de errores

"""


def rm(args):
    if not args:  # El primer argumento es la direccion del archivo a borrar,si no existe, avisar al usuario
        print(
            "Le falto ingresar la ruta absoluta o relativa del archivo a borrar (Ej: rm archivo_existente, rm /home/archivo_existente )")
        registrar_accion("rm", args, False,
                         "Falta argumento del nombre del archivo a borrar")  # Funcion para registrar accion fallida
        registrar_error("rm", args, "FaltaNombre",
                        "Falta argumento del nombre del archivo a borrar")  # Funcion para regisrar error
        return  # Retorna al shell

    archivo = args[0]  # Obtener la direccion y nombre del archivo a borrar

    if os.path.isdir(
            archivo):  # Verificar antes de confirmar si es un directorio, y avisar al usuario que solo puede borrar archivos
        print(
            "El comando solo soporta eliminar archivos, por favor solo ingresar archivos, puede utilizar ls para saber si es archivo o directorio")
        registrar_accion("rm", args, False,
                         "Prohibido borrar directorio, solo archivos")  # Funcion para registrar accion fallida
        registrar_error("rm", args, "EsDirectorio",
                        "Prohibido borrar directorio, solo archivos")  # Funcion para regisrar error
        return

    # Prompt de confirmacion a borrar el archivo
    confirmacion = input(f" ¿Esta seguro que desea borrar '{archivo}'? [s/n]: ").lower().strip()

    if confirmacion != 's':  # Si el usuario confirma que quiere borar el archivo
        print(" Operacion cancelada por el usuario.")
        return  # Retornar al shell, evitar continuar con la eliminacio
    try:
        os.unlink(archivo)  # Llamada al sistema para borar el archivo
        print(f"Archivo eliminado: {archivo}")
        registrar_accion("rm", args, True, "Archivo eliminado correctamente")  # Funcion para registrar accion exitosa

    except FileNotFoundError:  # Archivo no existe
        print(f"El Archivo ingresado no existe: {archivo},puede utilizar ls para buscar el nombre correcto")
        registrar_accion("rm", args, False, "No se encontro el archivo")  # Funcion para registrar accion fallida
        registrar_error("rm", args, "ArchivoNoEncontrado", "No se encontro el archivo")  # Funcion para regisrar error
    except PermissionError:  # El usuario no tiene los privilegios necesario para borrar
        print("Usted carece de privilegios para borrar el archivo")
        registrar_accion("rm", args, False,
                         "No tiene los privilegios suficientes")  # Funcion para registrar accion fallida
        registrar_error("rm", args, "FaltaPermiso",
                        "No tiene los privilegios suficientes")  # Funcion para regisrar error


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
            "Esta funcion precisa de dos argumentos,primero: la ruta del archivo a copiar, segundo: la ruta del archivo a ser creado, ej: cp asd.txt /home/user/asd.txt")
        registrar_accion("cp", args, False, "Numero de argumentos incorrecto")  # Funcion para registrar accion fallida
        registrar_error("cp", args, "NumArgsIncorrecto",
                        "Numero de argumentos incorrecto")  # Funcion para regisrar error
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
            registrar_accion("cp", args, True, "Archivo copiado correctamente")  # Funcion para registrar accion exitosa

        except FileNotFoundError:  # Si no se encuentra el archivo a copiar
            # Verificar cual de los dos no existe
            if not os.path.exists(origen):
                print(f"Error: El archivo de origen '{origen}' no fue encontrado, puede utilizar ls para informarse")
                registrar_accion("cp", args, False, "No se encontro el Archivo a copiar")  # Funcion para registrar accion fallida
                registrar_error("cp", args, "ArchivoNoEncontrado","No se encontro el Archivo a copiar")  # Funcion para regisrar error
            else:
                # Si el origen existe, entonces el problema es la carpeta destino
                destino_dir = os.path.dirname(destino)
                print(f"Error: La carpeta destino '{destino_dir}' no existe")
                registrar_accion("cp", args, False,"No se encontro el directorio destino a copiar")  # Funcion para registrar accion fallida
                registrar_error("cp", args, "DirectorioNoEncontrado","No se encontro el directorio destino a copiar")  # Funcion para regisrar error        
        

        except PermissionError:  # Si no se puede acceder  por falta de privilegio el archivo a copiar
            print(f"Error: No tiene los privilegios suficientes para copiar en {destino}' ")
            registrar_accion("cp", args, False,
                             "No tiene los privilegios suficientes para copiar")  # Funcion para registrar accion fallida
            registrar_error("cp", args, "FaltaPermiso",
                            "No tiene los privilegios suficientes para copiar")  # Funcion para regisrar error

        except OSError as e:  # Error generico
            print(f"Ocurrió un error durante la copia: {e}")
            registrar_accion("cp", args, False, "Ha ocurrido un error")  # Funcion para registrar accion fallida
            registrar_error("cp", args, "ErrorGenerico", "Ha ocurrido un error")  # Funcion para regisrar error


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
        registrar_accion("cd", args, True, "Permanecer en el mismo directorio")  # Funcion para registrar accion exitosa
        nuevo_dir = "."  # La variable es asignada el directorio actual.
        return  # Terminar y no seguir ejecutando el resto del codigo

    try:
        os.chdir(nuevo_dir)  # Cambiar de directorio a la que se paso como argumento
        print(f"EXITO Cambio a {os.getcwd()}")  # Imprimir exito para debug
        registrar_accion("cd", args, True,
                         "Cambiar de directorio exitosamente")  # Funcion para registrar accion exitosa
    except FileNotFoundError:  # Atrapar error si no encuentra o existe el directorio
        print(
            f"ERROR Directorio no encontrado: {nuevo_dir}. Utlize el comando ls para saber si es correcto el directorio ingresado ")
        registrar_accion("cd", args, False,
                         "No se pudo encontrar el directorio a ingresar")  # Funcion para registrar accion fallida
        registrar_error("cd", args, "DirNoEncontrado",
                        "No se pudo encontrar el directorio a ingresar")  # Funcion para regisrar error
    except PermissionError:
        print(" No tiene los privilegios suficientes ")
        registrar_accion("ls", args, False,"No tiene los privilegios suficientes")  # Funcion para registrar accion fallida
        registrar_error("ls", args, "PermissionError","No tiene los privilegios suficientes")  # Funcion para regisrar error
    except OSError as e:  # Error generico
        registrar_accion("cd", args, False, "Ha ocurrido un error")  # Funcion para registrar accion fallida
        registrar_error("cd", args, "ErrorGenerico", "Ha ocurrido un error")  # Funcion para regisrar error


"""

    Función built-in ls

    - Muestra los archivos y directorios y los discierne
    - Permite mostrar los archivos en el directorio actual o en el directorio recibido por argumento.
    - Informa al usuario si el directorio no existe o si esta vacio

"""


def ls(args):
    ruta = "."
    if args:
        ruta = args[0]  # Determina la ruta a listar. Si args tiene elementos (if args),elige el primer elemento (args[0]) como la ruta, osino , usa el directorio actual .

    try:  # Para atrapar errores si los hay
        elementos = os.listdir(ruta)  # Listar todos los archivos y directorios en la direccion ruta
        if ruta == '.':
            print(f"Contenido de '{os.getcwd()}':")
            registrar_accion("ls", args, True,"Listar archivos y directorios del directorio actual correctamente")  # Funcion para registrar accion exitosa
        else:
            print(f"Contenido de '{ruta}':")
            registrar_accion("ls", args, True,"Listar archivos y directorios del directorio ingresado correctamente")  # Funcion para registrar accion exitosa
        if elementos:  # Si elementos contiene al menos un archivo o directorio
            for elem in elementos:  # Loop para determinar directorios
                if os.path.isdir(os.path.join(ruta,elem)):  # Se verifica si el archivo actual es o no un directorio , se arma la ruta(Direccion) + archivo, y checkea si es un directorio
                    print(f"  [Dir]  {elem}")
                else:  # Si no es un directorio el archivo actual
                    print(f"  [Arc] {elem}")
            return
        else:  # Si elemento esta vacio
            print("El directorio esta vacio!")
            registrar_accion("ls", args, True,"Tratar de listar un directorio vacio")  # Funcion para registrar accion exitosa
    except FileNotFoundError as e:  # Si no existe o no se encuentra el archivo
        print(f" El directorio {ruta} no existe o no se puede acceder ")
        registrar_accion("ls", args, False,"No se pudo encontrar el directorio a listar")  # Funcion para registrar accion fallida
        registrar_error("ls", args, "DirNoEncontrado","No se pudo encontrar el directorio a listar")  # Funcion para regisrar error
    except PermissionError:
        print(" No tiene los privilegios suficientes ")
        registrar_accion("ls", args, False,"No tiene los privilegios suficientes")  # Funcion para registrar accion fallida
        registrar_error("ls", args, "PermissionError","No tiene los privilegios suficientes")  # Funcion para regisrar error
    except OSError as e:  # Error generico
        registrar_accion("ls", args, False, "Ha ocurrido un error")  # Funcion para registrar accion fallida
        registrar_error("ls", args, "ErrorGenerico", "Ha ocurrido un error")  # Funcion para regisrar error


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
    global paso_actual  # Utilizar variable global
    iniciar_logs()  # Iniciar sistema de logging, ayuda a designar directorio correcto y verificar privilegios tambien.

    print("Bienvenido a EduShell - Shell Educativo Universitario")
    print("Escribe 'exit' para salir")
    print("Escribe 'help' para obetener ayuda basica\nEscribe 'tutorial' para un tutorial basico \n")
    
    while True:
        try:

            # Leer comando del usuario mostrando el modo actual: shell normal o tutorial

            if paso_actual != -1:  # Si se ingreso al modo tutorial
                comando = input(f"TUTORIAL - Paso {paso_actual + 1}  > ").strip()
            else:
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

            if comando_principal == "tutorial":
                paso_actual = 0  # Se cambia el valor al primer paso
                print(f"Inicio: {PASOS_TUTORIAL[0][2]}")
                continue

            permitido = tutorial(comando_principal,
                                 argumentos)  # Se guarda el retorno de la funcion dependiendo si se ingreso el comando correcto (True) o incorrecto (False)

            if not permitido:  # Si se ingreso el comando incorrecto, no se ejecuta el comando en el shell, permite al usuario no destruir o modificar algo sin intencion.
                continue

            if comando_principal == "help":
                help(argumentos)
                continue

            if comando_principal == "ver_logs":
                mostrar_logs("acciones")  # Acceder a la funcion con tipo=acciones para ver los logs
                continue

            if comando_principal == "ver_errores":
                mostrar_logs("errores")  # Acceder a la funcion con argumento tipo=errores para ver los errores
                continue

            # Ejecutar comandos built-in
            if comando_principal == "exit":
                print("¡Hasta luego!")
                registrar_accion("exit", argumentos, True, "Salir del shell")
                break

            elif comando_principal == "echo":
                echo(argumentos)

            elif comando_principal == "cat":
                cat(argumentos)

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
                registrar_accion("pwd", argumentos, True,"Imprimir directorio actual")  # Funcion para registrar accion exitosa

            else:
                # Si no existe el commando
                ejecutar_externo(comando_principal, argumentos)  # Funcion nueva

            if paso_actual != -1:  # Si esta activo el modo tutorial
                imprimir_info_tutorial()  # Imprimir mensaje de exito. Tambien siguiente instrucciones o de finalizacion del tutorial

        except KeyboardInterrupt:
            # Manejo de Ctrl+C - Termina de forma alterna
            print("\n¡Hasta luego! (Terminado con Ctrl + C!)")
            break


if __name__ == "__main__":  # Si se abre el archivo, se corre main automaticamente, si se importa se puede usar parseador por si solo
    main()