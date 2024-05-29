# Lab4_Robotica_Cinematica_Directa - Phantom X - ROS

Hector Alejandro Montes Lobaton  
Bryan Steven Pinilla Castro

## Introducción

El objetivo de esta práctica es implementar los Joint Controllers con ROS para manipular servomotores Dynamixel AX-12 del robot Phantom X Pincher y usar tópicos de estado, servicios y comando para todos los Joint Controllers del robot Phantom X Pincher.

A continuación se muestra el script realizado en Python para ubicar el robot Pincher en las 5 posiciones especificadas:
- 0, 0, 0, 0, 0.
- 25, 25, 20, -20, 0.
- -35, 35, -30, 30, 0.
-  85, -20, 55, 25, 0.
- 80, -35, 55, -45, 0.

## Parametros DH del robot Phantom X Pincher



## Conexion ROS:  [main.py](./Scripts/main.py).


La función joint_publisher() inicializa un publicador de ROS en el tópico `/joint_trajectory` para enviar mensajes del tipo JointTrajectory y configura un nodo de ROS llamado `joint_publisher`, asegurándose de que no sea anónimo, para controlar el movimiento de las articulaciones de un robot..
```
 def joint_publisher():
     pub = rospy.Publisher('/joint_trajectory', JointTrajectory, queue_size=0)
     rospy.init_node('joint_publisher', anonymous=False)
```
Este fragmento de código crea un mensaje `JointTrajectory`, asigna una marca de tiempo actual, define los nombres de las articulaciones y configura un punto de trayectoria con todas las posiciones inicializadas a cero y un tiempo desde el inicio de un segundo. Luego, agrega este punto al mensaje de trayectoria, publica el mensaje en el tópico correspondiente y finalmente imprime un mensaje de confirmación antes de pausar la ejecución durante cinco segundos, esto para cada posicion, el siguiente es un fragmento para la posicion 0.

```
def joint_publisher(postura: list, pub: rospy.Publisher):
    state = JointTrajectory()
    state.header.stamp = rospy.Time.now()
    state.joint_names = ["joint_1","joint_2","joint_3","joint_4","joint_5"]
    point = JointTrajectoryPoint()
    point.positions = postura  
    point.time_from_start = rospy.Duration(1)
    state.points.append(point)
    pub.publish(state)
    print('published command')
    rospy.sleep(1)
```

Se suscribe al topico `joint_states`.

```
def listener():
    rospy.Subscriber("/dynamixel_workbench/joint_states", JointState, callback)
```


## Toolbox

```
clear
close all
clc


%Función que genera una matriz de transformación homogénea con los Parámetros de Denavit-Hartenberg
function matriz = H(the,d,a,alp) 
%matriz que contiene la rotación en z
T=cos(the);
A=sin(the);
if isnumeric(the) == 1
    if abs(T) < 0.0000000000001  
        T=0;
    end
    if abs(A) < 0.0000000000001
         A=0;
    end 
end   
Rz=[T -A 0 0; A T 0 0; 0 0 1 0; 0 0 0 1];
%matriz que contiene la traslación en z
Dz=[1 0 0 0; 0 1 0 0; 0 0 1 d; 0 0 0 1];
%matriz que contiene la traslación en x
Dx=[1 0 0 a; 0 1 0 0; 0 0 1 0; 0 0 0 1];
%matriz que contiene la rotación en x
Y=cos(alp);
U=sin(alp);
if isnumeric(alp) == 1
    if abs(Y) < 0.0000000000001  
        Y=0;
    end
    if abs(U) < 0.0000000000001
         U=0;
    end 
end  
Rx=[1 0 0 0; 0 Y -U 0; 0 U Y 0; 0 0 0 1];
%matriz de transformación homogénea 
matriz = Rz*Dz*Dx*Rx;
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Comparacion de Graficas
L = [95 -105 -102 68];
off = [0 pi/2 pi/2 pi];
q1 = [0 0 0 0]*pi/180;
q2 = [25 25 20 -20]*pi/180;
q3 = [-35 35 -30 30]*pi/180;
q4 = [85 -20 55 25]*pi/180;
q5 = [80 -35 55 -45]*pi/180;


Ln1 = Link('revolute', 'd', L(1), 'a', 0, 'alpha', -pi/2, 'offset', off(1));
Ln2 = Link('revolute', 'd', 0, 'a', L(2), 'alpha', 0, 'offset',   off(2));
Ln3 = Link('revolute', 'd', 0, 'a', L(3), 'alpha', 0, 'offset',   off(3));
Ln4 = Link('revolute', 'd', 0, 'a', L(4), 'alpha', -pi, 'offset',   off(4));

Eslab = [Ln1;Ln2;Ln3;Ln4];
T_tool = eye(4);
Robot1 = SerialLink(Eslab, 'tool', T_tool)


figure()
ws = [-300 300 -300 300 -50 500];
Robot1.plot ([0 0 0 0], 'workspace', ws, 'noa','noname')
hold on
trplot (eye(4), 'witdh', 2, 'arrow', 'length', 30)
Robot1.teach(q5) %% Usar el q que se desea de entre las opciones
hold off
```

- 0, 0, 0, 0, 0.
![1](/Imagenes/1.png)

- 25, 25, 20, -20, 0.
![2](/Imagenes/2.png)

- -35, 35, -30, 30, 0.
![3](/Imagenes/3.png)

- 85, -20, 55, 25, 0.
![4](/Imagenes/4.png)

- 80, -35, 55, -45, 10.
![5](/Imagenes/5.png)

Link del video https://youtu.be/fBi8oY1wv1c?si=LQ2hGFMvziA7KhZC







## Ejecutar scripts


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


Para poder probar la interfaz desarrollada, se ubican en un mismo directorio los scripts de python [HMI.py](./Python/HMI.py) y [main_HMI.py](./Python/main_HMI.py). Por ejemplo, en la carpeta catkin_ws/src/dynamixel_one_motor/scripts.

Luego, se abre una terminal, para ejecutar los comandos:

 ```
catkin build dynamixel_one_motor
source devel/setup.bash
roslaunch dynamixel_one_motor one_controller.launch
```

Finalmente, en otra terminal se ejecuta el script [main_HMI.py](./Python/main_HMI.py).

```
python3 main_HMI.py
```

Si las recomendaciones y pasos anteriores, fueron correctamente ejecutados el resultado debe ser el siguiente. Ver **Figura 11.**, allí se evidencia la correcta ejecución de la interfaz.

<span><img id="Fig_12" src="Imágenes/6. beginning interfaz.png" width="700"/>
<label for = "Fig_12" ><br><b>Figura 12.</b> Demostración del funcionamiento de la interfaz</label></span>

Se optó por hacer un video donde se vean ambos requerimientos, la demostración de uso de la interfaz de usuario y el brazo alcanzando cada posición solicitada. Dicho video se encuentra en Google Drive, se puede acceder a el mediante este <a href=https://drive.google.com/file/d/1fMCtE7DXn7XliofkItHqumCnGdevGWHD/view?usp/>link</a>, es importante que acceda con la cuenta institucional *(ejemplo@unal.edu.co)*.

Allí se observa el correcto funcionamiento de la interfaz y al robot alcanzando las 5 posiciones solicitadas.
