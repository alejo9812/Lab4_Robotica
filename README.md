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

## Conexion ROS a Python:  Reutilizando el codigo del turtle sim.


La función joint_publisher() inicializa un publicador de ROS en el tópico `/joint_trajectory`[^/joint_trajectory]  para enviar mensajes del tipo JointTrajectory y configura un nodo de ROS llamado joint_publisher, asegurándose de que no sea anónimo, para controlar el movimiento de las articulaciones de un robot..
```
 def joint_publisher():
     pub = rospy.Publisher('/joint_trajectory', JointTrajectory, queue_size=0)
     rospy.init_node('joint_publisher', anonymous=False)
```
En otra se incia el nodo *turtlesim*.

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
