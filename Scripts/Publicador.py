import rospy
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import B.Interfaz as Interfaz 
         
def callback(data):
    data = [value*180/np.pi for value in data.position]
    Interfaz.data_to_HMI(data)


def listener():
    rospy.Subscriber("/dynamixel_workbench/joint_states", JointState, callback)

def joint_publisher():
     pub = rospy.Publisher('/joint_trajectory', JointTrajectory, queue_size=0)
     rospy.init_node('joint_publisher', anonymous=False)
     
     while not rospy.is_shutdown():
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
         state = JointTrajectory()
         state.header.stamp = rospy.Time.now()
         state.joint_names = ["joint_1", "joint_2", "joint_3", "joint_4", "joint_5"]
         point = JointTrajectoryPoint()
         point.positions = [-0.34, 0.34, -0.34, 0.34, 0]    
         point.time_from_start = rospy.Duration(1)
         state.points.append(point)
         pub.publish(state)
         print('published command')
         rospy.sleep(5)
         state = JointTrajectory()
         state.header.stamp = rospy.Time.now()
         state.joint_names = ["joint_1", "joint_2", "joint_3", "joint_4", "joint_5"]
         point = JointTrajectoryPoint()
         point.positions = [0.52, -0.52, 0.52, -0.52, 0]    
         point.time_from_start = rospy.Duration(1)
         state.points.append(point)
         pub.publish(state)
         print('published command')
         rospy.sleep(5)
         state = JointTrajectory()
         state.header.stamp = rospy.Time.now()
         state.joint_names = ["joint_1", "joint_2", "joint_3", "joint_4", "joint_5"]
         point = JointTrajectoryPoint()
         point.positions = [-1.57, 0.26, -0.95, 0.29, 0]    
         point.time_from_start = rospy.Duration(1)
         state.points.append(point)
         pub.publish(state)
         print('published command')
         rospy.sleep(5)
         state = JointTrajectory()
         state.header.stamp = rospy.Time.now()
         state.joint_names = ["joint_1", "joint_2", "joint_3", "joint_4", "joint_5"]
         point = JointTrajectoryPoint()
         point.positions = [-1.57, 0.78, -0.95, 0.78, 0.17]    
         point.time_from_start = rospy.Duration(1)
         state.points.append(point)
         pub.publish(state)
         print('published command')
         rospy.sleep(5)

def main():
    global pub
    # Publicador de tópico de controlador de articulación
    rospy.init_node('joint_publisher', anonymous=False)
    
    Interfaz.main()
        
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
