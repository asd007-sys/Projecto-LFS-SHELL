import builtins #Importa el modulo que contiene todas las funciones built-in de Python

print("Pruebas de la funcion built-in cat")

comandos = ["cat texto_random.txt","exit"] #Commandos a ejecutar
comando_actual = 0 #Contadordel numero actual de comando a ser ejecutado,0 siendo el primer comando

def inpu_censiyo(entorno):  #Funcion principal de pruba, recibe la variable de entonrno
    global comando_actual  #Crear una variable global
    print(entorno, end='') #Imprimir el entonrno
    
    if comando_actual < len(comandos): #Verificar si quedan comandos a ejecutar, en esta prueba se ejecuta de 0 a 5
        cmd = comandos[comando_actual] #Obtenemos el comando a ejecutar
        print(cmd) #Lo imprimimos
        comando_actual += 1  #Se asigna el proximo comando para la proxima ronda
        return cmd #Se retorna el comando actual
    return "exit"
    
builtins.input = inpu_censiyo #Reemplaza la funcion built-in de Python por la que se creo (inpu_censiyo)


from shell import main #Importar el shell, despues de modificar la funcion built-in

main()