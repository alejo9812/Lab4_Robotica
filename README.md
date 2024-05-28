# Lab4_Robotica_Cinematica_Directa - Phantom X - ROS

Hector Alejandro Montes Lobaton  

## Introducción

En este laboratorio se utilizó ROS en el que se hizo uso de la herramienta turtlesim para comprender los conceptos básicos de la programcación de robots en este ambiente de programación.  



## Conexion ROS a Python:  Reutilizando el codigo del turtle sim.


Tomamos un publicador dentro de la arquitectura ROS.
```
 def joint_publisher():
     pub = rospy.Publisher('/joint_trajectory', JointTrajectory, queue_size=0)
     rospy.init_node('joint_publisher', anonymous=False)
```
En otra se incia el nodo *turtlesim*.

```
rosrun turtlesim turtlesim_node
```

Abriendo en Matlab  se ejecuta el siguiente script *Matlab.mlx*.

```
Matlab.mlx
```


![Graph](Graph_mlx)



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
