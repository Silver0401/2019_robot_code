
#Librerias necesarias para el uso de todo el codigo

import wpilib
import threading
from wpilib.drive import MecanumDrive
from state import state
import oi
import time
import pidcontroller
from wpilib import Encoder, IterativeRobot
import pidcommand
#from wpilib.pidbase import PIDBase


class MyRobot(wpilib.TimedRobot):

	def robotInit(self):

		# Inicializadores_de_PCM (en caso de que no arranque el PCM)

		# self.Compressor.setClosedLoopControl(True)
		# self.enabled = self.Compressor.enabled()

		#Solenoides y Compresores
		
		self.Compressor = wpilib.Compressor(0)
		self.PSV = self.Compressor.getPressureSwitchValue()
		self.double_piston = wpilib.DoubleSolenoid(0,0,1)
		self.piston = wpilib.Solenoid(0,7)

		# Encoders
		
		k4X = 2
		self.ir = wpilib.DigitalInput(9)
		self.motor1 = wpilib.Talon(4)
		self.encoder = wpilib.Encoder(0,1, True, k4X)

		# Contador

		self.timer = wpilib.Timer()

		# Motores del Chasis

		self.front_left_motor = wpilib.Talon(0)
		self.rear_left_motor = wpilib.Talon(1)
		self.front_right_motor = wpilib.Talon(2)
		self.rear_right_motor = wpilib.Talon(3)
		

		#lift and claw motors

		self.lift_motor = wpilib.Talon(7)
		self.up_claw_motor = wpilib.Talon(5)
		self.down_claw_motor = wpilib.Talon(6)

		#sensores

		self.sensor_izquierdo = wpilib.DigitalInput(2)
		self.sensor_principal = wpilib.DigitalInput(3)
		self.sensor_derecho = wpilib.DigitalInput(4)


		#Unión de los motores para su funcionamiento
		# en conjunto de mecaunm

		self.drive = MecanumDrive(
			self.front_left_motor,
			self.rear_left_motor,
			self.front_right_motor,
			self.rear_right_motor)


	def autonomousInit(self):

		self.timer.reset()
		self.timer.start()
		state["timer_piston"] = 0
		
	def autonomousPeriodic(self):
		state["timer_piston"] += 1

		# # Avanzar 2.5s girar 1s avanzar 1s girar 1s avanzar 3s girar 1s avanzar 2s
		if self.timer.get() < 2.5:
			self.drive.driveCartesian(1,0,0,0)

		elif self.timer.get() > 2.5 and self.timer.get() < 3.5:
			self.drive.driveCartesian(0,0,1,0)

		elif self.timer.get() > 3.5 and self.timer.get() < 4.5:
			self.drive.driveCartesian(1,0,0,0)

		elif self.timer.get() > 4.5 and self.timer.get() < 5.5:
			self.drive.driveCartesian(0,0,1,0)

		elif self.timer.get() > 5.5 and self.timer.get() < 6.5:
			self.drive.driveCartesian(1,0,0,0)

		elif self.timer.get() > 6.5 and self.timer.get() < 9.5:
			self.drive.driveCartesian(1,0,0,0)

		elif self.timer.get() > 9.5 and self.timer.get() < 10.5:
			self.drive.driveCartesian(0,0,1,0)

		elif self.timer.get() > 10.5 and self.timer.get() < 12.5:
			self.drive.driveCartesian(1,0,0,0)

		# elif self.timer.get() > 26.5 and self.timer.get() < 29.5:
		# 	self.drive.driveCartesian(1,0,0,0)
		# elif self.timer.get() > 29.5 and self.timer.get() < 31.5:
		# 	self.drive.driveCartesian(0,0,-1,0)
		else:
			self.drive.driveCartesian(0,0,0,0)
			#gire en direccion contraria en z 8 seg, avanza por 5 seg gira a la derecha 2 seg avanza 3 gira a la izq 2 seg

										
	def teleopPeriodic(self):

		#se leen constantemente los botones,joysticks y cambia de modalidades de controles
		
		oi.read_control_inputs("ControlPico")

		# Funcionamiento del movimiento de las mecanum a través del control de xbox con y sin turbo

		x = state["mov_x"] 
		y = state["mov_y"] 
		z = state["mov_z"] 

		powerX = 0 if x < 0.15 and x > -0.15 else x
		powerY = 0 if y < 0.15 and y > -0.15 else y
		powerZ = 0 if z < 0.15 and z > -0.15 else z
	

		if state["align_activated"]:
			if self.sensor_principal.get():
				self.drive.driveCartesian(0, 0, 0, 0)
			elif self.sensor_izquierdo.get():
				self.drive.driveCartesian(0.4, 0, 0, 0)
			elif self.sensor_derecho.get():
				self.drive.driveCartesian(-0.4, 0 ,0, 0)
			else:
				self.drive.driveCartesian(0, -0.5, 0, 0)

		elif state["turbo_activated"]:

			self.drive.driveCartesian(powerX ,-powerY , powerZ * 0.8, 0)

		else:
			self.drive.driveCartesian(powerX * 0.7,-powerY * 0.7, powerZ * 0.6, 0)
			
		# Hatch panel bajo; garra y piston
		
		if state["posicion"] == 1 and state["mecanismo"] == 1:
			state["timer_lift_short"] += 1
			if state["timer_lift_short"] < 100:
				print ("en posicion baja")
			elif state["timer_lift_short"] < 200:
				state["piston_activated"] = False
			else:
				state["timer_lift_short"] = 0

		elif state["posicion"] == 1 and state["mecanismo"] == 2:
			state["timer_lift_short"] += 1
			if state["timer_lift_short"] < 100:
				print ("en posicion baja")
			elif state["timer_lift_short"] < 200:
				state["claw_activated"] = 2
			else:
				state["timer_lift_short"] = 0


		# Hatch panel medio; garra y piston

		if state["posicion"] == 2 and state["mecanismo"] == 1:
			state["timer_lift_middle"] += 1
			if state["timer_lift_middle"] < 100:
				print ("en posicion media")
			elif state["timer_lift_middle"] < 200:
				state["piston_activated"] = False
			else:
				state["timer_lift_middle"] = 0

		elif state["posicion"] == 2 and state["mecanismo"] == 2:
			state["timer_lift_middle"] += 1
			if state["timer_lift_middle"] < 100:
				print ("en posicion media")
			elif state["timer_lift_middle"] < 200:
				state["claw_activated"] = 2
			else:
				state["timer_lift_middle"] = 0


		# Hatch panel alto; garra y piston


		if state["posicion"] == 3 and state["mecanismo"] == 1:
			state["timer_lift_taller"] += 1
			if state["timer_lift_taller"] < 100:
				print ("en posicion alta")
			elif state["timer_lift_taller"] < 200:
				state["piston_activated"] = False
			else:
				state["timer_lift_taller"] = 0

		elif state["posicion"] == 3 and state["mecanismo"] == 2:
			state["timer_lift_taller"] += 1
			if state["timer_lift_taller"] < 100:
				print ("en posicion alta")
			elif state["timer_lift_taller"] < 200:
				state["claw_activated"] = 2
			else:
				state["timer_lift_taller"] = 0


		# Piston

		self.double_piston.set(state["claw_activated"])

		self.piston.set(state["piston_activated"])
		

		if state["Compressor_activated"]:
			self.Compressor.start()
		else:
			self.Compressor.stop()


        # Encoders


		if state["encoder"]:
			if self.encoder.get() > -5000:
				self.motor1.set(0)
			else:
				self.motor1.set(1)
				wpilib.DriverStation.reportWarning(str(self.encoder.get()), False)
		else:
			self.motor1.set(0)
			self.encoder.reset()


			# wpilib.DriverStation.reportWarning(str(self.encoder.get()), False)
			#wpilib.DriverStation.reportWarning(str(PIDController.rcw.get(self)), False)
#funcion para correr el código del robot utlizando
# este archivo como el principal

if __name__ == '__main__':
	wpilib.run(MyRobot)
