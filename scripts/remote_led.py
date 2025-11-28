#!/usr/bin/env python3

import rospy
from std_msgs.msg import Bool
import sys
import tty
import termios

class LEDKeyboardControl:
    def __init__(self):
        rospy.init_node('led_keyboard_control', anonymous=True)
        
        # Publica en el mismo topic que tu nodo anterior
        self.led_publisher = rospy.Publisher('/toggle_led', Bool, queue_size=10)
        
        # Estado actual del LED
        self.led_state = False
        
        rospy.loginfo("Control de LED por teclado iniciado")
        rospy.loginfo("Presiona '1' para encender (True)")
        rospy.loginfo("Presiona '0' para apagar (False)")
        rospy.loginfo("Presiona 'ESPACIO' para alternar estado")
        rospy.loginfo("Presiona 'q' para salir")
        
    def get_key(self):
        """Obtiene una tecla presionada sin esperar Enter"""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    
    def publish_led_state(self, state):
        """Publica el estado del LED"""
        msg = Bool()
        msg.data = state
        self.led_publisher.publish(msg)
        rospy.loginfo("Publicando LED: {}".format(state))
    
    def run(self):
        """Bucle principal del control"""
        while not rospy.is_shutdown():
            try:
                key = self.get_key()
                
                if key == '1':
                    self.led_state = True
                    self.publish_led_state(self.led_state)
                    
                elif key == '0':
                    self.led_state = False
                    self.publish_led_state(self.led_state)
                    
                elif key == ' ':  # Barra espaciadora
                    self.led_state = not self.led_state
                    self.publish_led_state(self.led_state)
                    
                elif key == 'q' or key == '\x03':  # 'q' o Ctrl+C
                    rospy.loginfo("Saliendo...")
                    break
                    
            except Exception as e:
                rospy.logerr("Error: {}".format(e))
                break

if __name__ == '__main__':
    try:
        controller = LEDKeyboardControl()
        controller.run()
    except rospy.ROSInterruptException:
        pass
