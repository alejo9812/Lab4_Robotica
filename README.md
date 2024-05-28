# Lab4_Robotica_Cinematica_Directa - Phantom X - ROS

Hector Alejandro Montes Lobaton  

## Introducción

El objetivo de esta práctica es implementar los Joint Controllers con ROS para manipular servomotores Dynamixel AX-12 del robot Phantom X Pincher y usar tópicos de estado, servicios y comando para todos los Joint Controllers del robot Phantom X Pincher.

A continuación se muestra el script realizado en Python para ubicar el robot Pincher en las 5 posiciones especificadas:
- 0, 0, 0, 0, 0.
- 25, 25, 20, -20, 0.
- -35, 35, -30, 30, 0.
-  85, -20, 55, 25, 0.
- 80, -35, 55, -45, 0.

## Conexion ROS a Python:  [main_HMI.py](./Python/main_HMI.py).


La función joint_publisher() inicializa un publicador de ROS en el tópico `/joint_trajectory` para enviar mensajes del tipo JointTrajectory y configura un nodo de ROS llamado `joint_publisher`, asegurándose de que no sea anónimo, para controlar el movimiento de las articulaciones de un robot..
```
 def joint_publisher():
     pub = rospy.Publisher('/joint_trajectory', JointTrajectory, queue_size=0)
     rospy.init_node('joint_publisher', anonymous=False)
```
Este fragmento de código crea un mensaje `JointTrajectory`, asigna una marca de tiempo actual, define los nombres de las articulaciones y configura un punto de trayectoria con todas las posiciones inicializadas a cero y un tiempo desde el inicio de un segundo. Luego, agrega este punto al mensaje de trayectoria, publica el mensaje en el tópico correspondiente y finalmente imprime un mensaje de confirmación antes de pausar la ejecución durante cinco segundos, esto para cada posicion, el siguiente es un fragmento para la posicion 0.

```
state = JointTrajectory()
   state.header.stamp = rospy.Time.now()
   state.joint_names = ["joint_1", "joint_2", "joint_3", "joint_4", "joint_5"]
   point = JointTrajectoryPoint()
   point.positions = [0, 0, 0, 0, 0]    
   point.time_from_start = rospy.Duration(1)
   state.points.append(point)
   pub.publish(state)
   print('published command')
   rospy.sleep(5)
```

Se suscribe al topico `joint_states`.

```
def listener():
    rospy.Subscriber("/dynamixel_workbench/joint_states", JointState, callback)
```


![Graph](Graph_mlx)




# 1. Configuración del espacio de trabajo

Aunque el enfoque de la práctica es el uso de herramientas, como el toolbox de Peter Corke y ROS, buena parte del tiempo es invertida en explorar la documentación y los repositorios de referencia. Por tanto, a continuación se expone el procedimiento a seguir para configurar el espacio de trabajo, previo a la elaboración de la práctica, con el fin de que el sistema reconozca los motores y sea posible la conexión con ROS.

## Recomendaciones iniciales.

 - No es necesario y llega a ser perjudicial actualizar Python. Con la version de Python que trae la version 20.04 LTS de Ubuntu es más que suficiente.

 - No es necesario eliminar los repositorios antes utilizados en la herramienta `Catkin`, no existe evidencia alguna que determine si esto afecta el funcionamiento de la conexión de los motores con ROS.

 - Se debe conectar el robot a la fuente de alimentación y el cable de datos a la computadora, en caso contrario, tanto ROS como el software de Dynamixel NO detectaran los motores por más comandos de configuración que se ejecuten.

## a. Descarga de Dynamixel

Primero, se descarga el paquete de instalación para Ubuntu (linux) (<a href= https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_wizard2/>aquí</a>). Luego, se abre una terminal en la carpeta donde el paquete fue descargado, y se ejecutan en el mismo orden se los siguientes comandos .

- Otorgar permisos al paquete en cuestión.

```
sudo chmod 775 DynamixelWizard2Setup_x64
```

- Iniciar el programa y finalizar la instalación.

```
./DynamixelWizard2Setup_x64
```

- Dar acceso a los puertos USB.

```
sudo usermod -aG dialout UserName
```

*UserName*, corresponde al nombre de usuario de su cuenta Linux, con la que se inicia sesión en Ubuntu.

- Reiniciar

```
reboot
```

Una vez terminado el proceso anterior, Ubuntu esta configurado para permitir el paso de información por parte de los motores. Así el software de Dynamixel puede identificar los motores a la hora de ejecutar el Scan encargado de su búsqueda, sin embargo ROS aún no los reconoce.

<span><img id="Fig_1" src="Imágenes/CMotors Found.png" width="350"/>
<label for = "Fig_1" ><br><b>Figura 1.</b> Motores encontrados en el Scan, Dynamixel.</label></span>

## b. Configuración de *dynamixel_one_motor*

Se asume que el usuario tiene a su disposición `ROS` y la herramienta `Catkin`, con la carpeta `src`creada. 

1. Clonar el repositorio [dynamixel_one_motor](https://github.com/fegonzalez7/dynamixel_one_motor.git) en la carpeta src.

```
git clone https://github.com/fegonzalez7/dynamixel_one_motor.git
```

2. Editar el archivo `basic.yaml`, ubicado en la carpeta `config`, en la ruta `...\catkin_ws\src\dynamixel_one_motor\config\`. Allí se debe dejar la siguiente configuración, y guardar los cambios. Esta configuración es necesaria para que ROS reconozca los motores, se asignan los ID encontrados en el scan hecho en *Dynamixel*.

```
joint_1:
  ID: 1
  Return_Delay_Time: 0
  
joint_2:
 ID: 2
 Return_Delay_Time: 1
  
joint_3:
 ID: 3
 Return_Delay_Time: 2
  
joint_4:
 ID: 4
 Return_Delay_Time: 3
  
joint_5:
 ID: 5
 Return_Delay_Time: 4
 ```

 Como se puede observar `Return_Delay_Time`, es la característica encargada del retardo por articulación recomendado en la guía de trabajo. 
 
3. Con una terminal abierta en la carpeta `catkin_ws`, se ejecuta el siguiente comando para guardar los cambios.

 ```
catkin build dynamixel_one_motor
 ```

4. En la misma terminal, se ejecutan los siguientes comandos, los cuales dan pie a la ejecución y conexión de ROS con los motores.

 ``` 
 source devel/setup.bash
 roslaunch dynamixel_one_motor one_controller.launch
```

Si las recomendaciones y pasos anteriores, fueron correctamente ejecutados el resultado debe ser el siguiente. Ver **Figura 2**. Allí se evidencia como ROS reconoce los 5 motores del robot.

<span><img id="Fig_2" src="Imágenes/terminal roslaunch running.png" width="600"/>
<label for = "Fig_2" ><br><b>Figura 2.</b> ROS Corriendo correctamente.</label></span>

```
% Apagar cualquier instancia de ROS en ejecución
rosshutdown;

% Inicializar ROS
rosinit;

% Crear un publicador para enviar comandos de velocidad a la tortuga
velPub = rospublisher('/turtle1/cmd_vel','geometry_msgs/Twist');

% Crear un mensaje vacío de velocidad
velMsg = rosmessage(velPub);

% Configurar la velocidad lineal en el mensaje
velMsg.Linear.X = 1;

% Enviar el mensaje de velocidad a la tortuga
send(velPub, velMsg);

% Esperar durante 1 segundo para permitir que la tortuga se mueva
pause(1);

% Crear un suscriptor para el tópico de velocidad de la tortuga
cameraSub = rossubscriber('/turtle1/cmd_vel', 'geometry_msgs/Twist');

% Obtener el último mensaje de velocidad recibido por la tortuga
cameraMsg = cameraSub.LatestMessage;

% Extraer los componentes lineales y angulares del mensaje de velocidad
Lin = cameraMsg.Linear;
Ang = cameraMsg.Angular;
```
