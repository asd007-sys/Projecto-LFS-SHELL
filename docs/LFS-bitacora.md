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



# Sesión 3: 29 de Noviembre - 09:47 a  11:21 - Configuración del Entorno LFS y Descarga de Paquetes


## Participantes: Marcelo Avalos 
## Objetivo: Configurar entorno LFS, crear estructura de directorios y descargar todos los paquetes.

## Tareas Realizadas
(09:47 - 10:03 )

Configurar variable de entorno LFS

Tener umask correcto para permisos seguros

Montar partición de LFS en el punto de montaje

Asignar permisos de ownership y acceso

Crear directorio sources con permisos correctos

(10:03 - 10:37)

Descargar paquetes fuente usando wget-list-systemd

(10:37 - 11:07)

Completar descargas faltantes desde el mirror 

(11:07 - 11:21)

Verificar que todos los archivos están correctamente descargados con md5sums

Asignar root como dueño de los paquetes descargados


## Comandos Ejecutados

#### Configurar variables de entorno 

export LFS=/mnt/lfs

umask 022

#### Montar partición LFS

mkdir -pv $LFS

mount -v -t ext4 /dev/sda6 $LFS

#### Asignar permisos de ownership y acceso

chown root:root $LFS

chmod 755 $LFS

#### Crear directorio sources y configurar permisos

mkdir -v $LFS/sources

chmod -v a+wt $LFS/sources

#### Descargar paquetes usando el wget-list-systemd del manual

cd $LFS/sources

wget https://www.linuxfromscratch.org/lfs/view/stable-systemd/wget-list-systemd

wget --input-file=wget-list-systemd --continue --directory-prefix=$LFS/sources

#### Descargar paquetes faltantes usando uno de los mirrors disponibles

wget --input-file=wget-list-systemd-mirror --continue --directory-prefix=$LFS/sources

#### Verificar integridad de los paquetes

pushd $LFS/sources

  md5sum -c md5sums

popd

#### Ver si hay alguna linea que no termina en OK

md5sum -c md5sums | grep -v “OK”

#### Asignar root como dueño de paquetes descargado

chown root:root $LFS/sources/*


## Problemas Encontrados

Problema 1: Algunos paquetes fallaron en la descarga con la lista oficial

Causa: Problemas de conectividad con los servidores oficiales

Solución: Usar mirror alternativo https://lfs.gnlug.org/pub/lfs/lfs-packages/12.4/ para completar las descargas. Se uso una inteligencia artificial para que copie la direccion url de cada paquete + el nombre de cada paquete, ej : https://lfs.gnlug.org/pub/lfs/lfs-packages/12.4/acl-2.3.2.tar.xz . Se hizo esto para cada paquete y se creó un archivo wget-list-systemd-mirror y se uso este mismo archivo como se usó el original ej: wget --input-file=wget-list-systemd-mirror --continue --directory-prefix=$LFS/sources. Así se consigue descargar todos los paquetes


Problema 2: Necesidad de verificar integridad de paquetes descargados

Causa: Descargas desde múltiples fuentes

Solución: Usar md5sum -c md5sums y md5sum -c md5sums | grep -v “OK”, regex con grep para validar todos los archivos y verificar

Problema 3: Se apagó inesperadamente la PC

Causa: Corte de electricidad inesperada

Solución: Montar $LFS de nuevo y asegurarse de que todo tenga los privilegios necesarios ejecutando los comandos de permisos nuevamente

Problema 4: md5sum: WARNING 1 line is improperly formatted 

Causa: Puede ser descarga incorrecta, no estoy muy seguro

Solución: Se volvió a descargar el archivo, y no volvió a causar errores o warnings

## Resultados Obtenidos

Variables de entorno LFS configuradas

Partición LFS montada y con permisos adecuados

Directorio sources creado con permisos a+wt

Todos los paquetes de LFS descargados

Archivos verificados con md5sum

Entorno preparado comenzar la construcción de LFS


## Reflexión Técnica

Al parecer es muy común tener que usar mirrors para descargar paquetes faltantes, así que el uso de mirrors es importante aprender a usar. La verificación con md5sum da confianza de que los paquetes o archivos se descargaron correctamente y además sirve para ver si faltó alguno, lo cual es un plus extra.
Usamos el directorio $LFS/sources (/mnt/lfs/sources ) como lugar donde descargar los paquetes y donde se va a construir cada paquete, tiene doble función para que las variables de entornos queden limpias.

## Evidencias

![wget-original-falla](../imagenes/LFS/sesion3/wget-original-falla.png)
*Figura 1: wget-list-systemd no pudo descargar todos los archivos*

![archivos-fallados-md5sum](../imagenes/LFS/sesion3/archivos-fallados-md5sum.png)
*Figura 2: Archivos fallados verificado con md5sum*

![md5-error](../imagenes/LFS/sesion3/md5-error.png)
*Figura 3: Error del archivo md5sums*

![archivos-exitoso-md5sum](../imagenes/LFS/sesion3/archivos-exitoso-md5sum.png)
*Figura 4: Integridad de archivos confirmados y no falta paquetes*


