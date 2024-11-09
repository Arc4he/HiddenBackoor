# Command And Control

C2 se centra en dos funciones principales:

## Ini 🚀

```
git clone https://github.com/Arc4he/HiddenBackoor.git
```

### Pre-requisitos 📋
```
pip install -r requeriments.txt
```

### Uso

1. **En la máquina víctima**:
   - Ejecuta `icmp-script.py` con `sudo` para instalar el backdoor finalmente se **AUTODESTRUIRÁ**.
   - Usa `remove-changes.py` si deseas eliminar los rastros del ataque.

2. **En la máquina atacante**:
   - Ejecuta `main.py` para recibir conexiones de las máquinas comprometidas.

## Resumen

Este repositorio contiene dos scripts esenciales para realizar un ataque de **path traversal** y dejar un backdoor persistente en la máquina víctima, manteniendo el acceso remoto. Además, incluye un script adicional para **eliminar los cambios** hechos en la máquina víctima, dejando el sistema como estaba antes del ataque. 

### `icmp-script.py`

1. **Escaneo de Hosts en la Red Local**: El script comienza realizando un escaneo de hosts en la red local para identificar máquinas vulnerables.
   
2. **Creación del Backdoor**:
   - Utiliza `sudo` para crear un backdoor en la máquina víctima mediante un servicio `systemd`.
   - Este backdoor permite al atacante mantener un acceso persistente a la máquina, incluso después de reinicios, estableciendo una conexión en intervalos regulares con el servidor de comando y control (C&C) del atacante.

3. **Persistencia a través de Reinicios**:
   - El servicio creado por el script se vuelve persistente y se ejecuta automáticamente cada vez que la máquina víctima se reinicie, garantizando que el atacante pueda conectarse y ejecutar comandos sin que el usuario se percate.

4. **Acceso Remoto Persistente**:
   - El atacante puede ejecutar comandos como root, tener control total sobre la máquina víctima y enviar información a través del backdoor establecido por el servicio `systemd`.

### `remove-changes.py`

El script `remove-changes.py` está diseñado para **eliminar los cambios realizados** en la máquina víctima durante el ataque. Esto permite que el sistema vuelva a su estado original, dejando la máquina limpia de los artefactos del ataque.

1. **Eliminación de Backdoor**:
   - Elimina el servicio `systemd` creado por `icmp-script.py`, asegurando que el backdoor no siga activo después de ejecutar este script.

2. **Restauración del Sistema**:
   - Revierte cualquier modificación que el script `icmp-script.py` haya realizado en el sistema para restaurarlo a su estado original.
   - Elimina cualquier archivo o configuración adicional creada para permitir la ejecución del backdoor.

3. **Limpieza Completa**:
   - Elimina cualquier rastro de acceso para garantizar que el atacante no pueda recuperar el acceso.

### `main.py` - Obtener Conexiones

Una vez que el atacante ha ejecutado `icmp-script.py` y se ha establecido el backdoor, el script `main.py` debe ser ejecutado en la máquina atacante para **recibir las conexiones** de la víctima.

1. **Escucha de Conexiones**:
   - `main.py` se configura para escuchar las conexiones entrantes de las máquinas comprometidas.
   
2. **Conexión con la Víctima**:
   - Este script actúa como un servidor que recibe comandos desde las máquinas víctimas, permitiendo al atacante ejecutar comandos a través de la conexión establecida por el backdoor.

3. **Interfaz para Control**:
   - El script permite al atacante interactuar con la víctima y enviar comandos remotos a la máquina comprometida.

### Flujo del Ataque

1. **Ejecutar `icmp-script.py` en la víctima**:
   - El atacante ejecuta el script en la máquina víctima. Este script realiza un escaneo de la red, instala el backdoor y establece una conexión persistente mediante un servicio `systemd`.

2. **Ejecutar `main.py` en la máquina atacante**:
   - Mientras `icmp-script.py` está ejecutándose en la víctima, el atacante debe ejecutar `main.py` en su máquina para **escuchar y recibir las conexiones** de la víctima comprometida.

3. **Limpiar la Máquina Víctima con `remove-changes.py`**:
   - Si el atacante quiere limpiar el sistema después de completar el ataque, puede ejecutar `remove-changes.py` para eliminar el backdoor y devolver el sistema a su estado original.

---

### Notas importantes:
1. **Requiere permisos de superusuario (sudo)** en ambas máquinas para que los scripts puedan interactuar con el sistema de manera efectiva.
2. El script en la máquina atacante debe estar esperando la conexión antes de que el script de la máquina víctima se ejecute.

**Autor**: [Arc4he]
>
