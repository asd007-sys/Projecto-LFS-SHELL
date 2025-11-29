# Bitácora del Proyecto LFS

## Integrantes: Marcelo Avalos 
## Fecha de inicio: 27 de Noviembre Sesión 1: Instalación Rocky Linux 10 Host


### Objetivo: Instalar Rocky Linux 10 como host para LFS

## Tareas Realizadas 
 #### Instalación inicial (18:01 - 18:32)
 - Crear VM (4 CPU, 11.5GB RAM, 60GB disco)
 - Configurar esquema de particiones personalizado
 - Completar instalación básica   



## Comandos ejecutados después de la instalación:

 lsblk 

 free -h


## Resultados:

Particiones: / (20G), /home (5G), swap (12G), libre (22G)

RAM: 11.5GB confirmada

Versión: Rocky Linux 10.0

## Problemas Encontrados

Problema: Tamaño de /home posiblemente muy pequeño

Solución: Como la mayoría de LFS se construye en la partición dedicada, el host no precisa de un /home grande

## Aprendizaje: 
El espacio crítico está en la partición LFS, no en /home del host

## Resultados Obtenidos

Rocky Linux 10 instalado y funcionando 22GB espacio libre reservado para LFS Sistema listo para configuración LFS

## Reflexión Técnica

Los 22GB libres deberían ser suficientes el LFS segun el manual.El swap de 12GB deberia ayudar en compilaciones grandes.La partición /home de 5GB es suficiente para documentación y configuraciones del proyecto

## Evidencias

![Particion del build system](../imagenes/LFS/sesion1/Build-sysytem.png)
*Figura 1: Particion del build system*

![Instalacion completa](../imagenes/LFS/sesion1/instalado.png)
*Figura 2:  Instalacion completa*

![Commando lsblk y free -h](../imagenes/LFS/sesion1/lsblk-free-h.png)
*Figura 3:  Commando lsblk y free -h*



# Sesión 2: 28 de Noviembre, 18:02 a 20:22 - Preparación Completa del Entorno LFS

## Duración: 2:30 horas aprox. 
## Participantes: Marcelo Avalos 

### Objetivo: Verificar requisitos del host, crear partición LFS y preparar para comenzar LFS

## Tareas Realizadas




(18:02 - 18:29)
 - Correr version-check.sh del manual LFS 
 - Identificar paquetes faltantes en el sistema host 

 (18:29 - 19:51)
 - Instalar paquetes o herramientas faltantes 
 - Configurar enlace simbólico yacc -> bison 

(19:51- 20:22)

 - Crear partición LFS en espacio libre de ~ 23GB 
 - Formatear partición LFS como ext4


## Comandos Ejecutados

#### Updatear el sistema

dnf  check-update

dnf upgrade

#### Verificación de los requisitos necesarios

bash version-check.sh

#### Instalación de paquetes faltantes

dnf install bison m4 patch perl

 dnf install gcc gcc-c++ make

#### Configuración de yacc, link simbolico

ln -sv /usr/bin/bison /usr/bin/yacc

#### Creación de partición LFS con parted

parted /dev/sda

print free # Ver espacio libre

parted /dev/sda mkpart primary ext4 40.8GB 63.8GB 

quit

#### Formatear partición

mkfs -t ext4 /dev/sda6

## Problemas Encontrados

Problema 1: Comandos gcc, g++ y make faltantes

Causa: No viene con Rocky Linux, ni con el check-update , upgrade. 

Solución: dnf install gcc gcc-c++ make

Problema 2: yacc no encontrado y bison tampoco

Causa: Instalar bison y hacer el link simbólico entre bison y yacc 

Solución: dnf install bison m4 patch perl ln -sv /usr/bin/bison /usr/bin/yacc

Problema 3: texinfo paquete faltante

Causa: Repositorio CRB deshabilitado por predeterminado, se habilita mediante comandos. 

Solución: se habilita mediante comandos:

dnf config-manager --set-enabled crb 

dnf install texinfo

Problema 4: Faltaban los paquetes perl, m4 y patch

Causa: De nuevo no está incluido en Rocky Linux, ni se descarga con el update. 

Solución: dnf install m4 patch perl

Problema 5: Error de symlink - creé /usr/bin/yac por error

Causa: Mal tipeado el comando 

Solución: rm -v /usr/bin/yac

Problema 6: Se intentó formatear con fdisk pero este lanzó una advertencia de que el disco está actualmente en uso.

Causa fdisk recomienda que reparticionar es una mala idea actualmente, porque el disco está en uso y se puede perder datos.

Solución: Usar parted para hacer la partición en el disco, se resolvió sin problemas


## Resultados Obtenidos

Todas las herramientas necesarias instaladas 

GCC confirmado 

Partición LFS creada (/dev/sda6 de ~21GB) 

Partición formateada como ext4 Host completamente preparado para LFS



## Reflexión Técnica

La preparación del Host y de sus requisitos necesarios demostró que es importante chequear siempre si falta un paquete, porque podría ocasionar grandes problemas más adelante. Ignore la sección en un previo intento y sufrí las consecuencias.Habilitar el repositorio crb fue necesario para instalar texinfo,me tomó bastante tiempo encontrar la resolución. Poder usar parted en un disco en uso para crear una particion en la memoria libre es algo muy util y conveniente.

## Evidencias
![requisitos-faltantes](../imagenes/LFS/sesion2/requisitos-faltantes.png)
*Figura 1:  Requisitos que faltan en el build system(Rocky Linux)*

![requisitos-cumplido](../imagenes/LFS/sesion2/requisitos-cumplido.png)
*Figura 2:  Requisitos necesarios cumplidos*

![fdisk-advertensia](../imagenes/LFS/sesion2/fdisk-advertensia.png)
*Figura 3:  Advertensia del fdisk *

![Partición LFS creada](../imagenes/LFS/sesion2/parted.png)
*Figura 4:  Creación de la particion con parted*

![Partición LFS creada](../imagenes/LFS/sesion2/lsblk.png)
*Figura 5:  Output del comando lsblk para ver partition nueva para lfs*

