
#Librerias necesarias para el uso de todo el codigo

import wpilib
from wpilib.drive import MecanumDrive
from state import state
import oi
import time


class MyRobot(wpilib.TimedRobot):

	def robotInit(self):

		# Inicializadores_de_PCM (en caso de que no arranque el PCM)

		# self.Compressor.setClosedLoopControl(True)
		# self.enabled = self.Compressor.enabled()

		#Solenoides y Compresores
		
		self.Compressor = wpilib.Compressor(0)
		self.PSV = self.Compressor.getPressureSwitchValue()
		self.double_piston = wpilib.DoubleSolenoid(0,1,2)
		self.piston = wpilib.Solenoid(0,0)

		# Encoders
		
		self.encoder = wpilib.Encoder(8, 9)
		self.P = 0.2
		self.I = 0
		self.D = 0

		self.integral = 0
		self.previous_error = 0

		# Contador y Control

		self.timer = wpilib.Timer()

		# Motores del Chasis

		self.front_left_motor = wpilib.Talon(0)
		self.rear_left_motor = wpilib.Talon(1)
		self.front_right_motor = wpilib.Talon(2)
		self.rear_right_motor = wpilib.Talon(3)
		

		#lift and claw motors

		self.lift_motor = wpilib.Talon(4)
		self.lift_motor_2 = wpilib.Talon(5)

		self.claw_motor = wpilib.Talon(6)
		self.wheeler_motor = wpilib.Talon(7)

		#sensores

		self.sensor_izquierdo = wpilib.DigitalInput(0)
		self.sensor_principal = wpilib.DigitalInput(1)
		self.sensor_derecho = wpilib.DigitalInput(2)


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

		self.PID()
		self.timer.start()

		#se leen constantemente los botones,joysticks y cambia de modalidades de controles
		
		oi.read_control_inputs(state["Controller"])

		# Movimiento manual de las mecanum, align y turbo

		x = state["mov_x"] 
		y = state["mov_y"] 
		z = state["mov_z"] 

		powerX = 0 if x < 0.25 and x > -0.25 else x
		powerY = 0 if y < 0.25 and y > -0.25 else y
		powerZ = 0 if z < 0.25 and z > -0.25 else z
	

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
			self.drive.driveCartesian(powerX * 0.6,-powerY * 0.6, powerZ * 0.5, 0)


		# Configuracion para el elevador automaticamente

		# Hatch panel medio; garra y piston
		

		if state["posicion"] == "media" and state["mecanismo"] == "piston":
			state["timer_lift_middle"] += 1
			if state["timer_lift_middle"] < 150:
				state["lift_motor"] = 1
			elif state["timer_lift_middle"] < 185:
				state["piston_activated"] = True
			elif state["timer_lift_middle"] < 200:
				state["piston_activated"] = False
			elif state["timer_lift_middle"] < 350:
				state["lift_motor"] = -1
			else:
				state["timer_lift_middle"] = 0
				state["posicion"] = "neutral"
				state["mecanismo"] = "neutral"

		if state["posicion"] == "media" and state["mecanismo"] == "garra":
			state["timer_lift_middle"] += 1
			if state["timer_lift_middle"] < 150:
				state["lift_motor"] = 1
			elif state["timer_lift_middle"] < 185:
				state["wheeler_motor"] = 1
			elif state["timer_lift_middle"] < 335:
				state["lift_motor"] = -1
			else:
				state["timer_lift_middle"] = 0
				state["posicion"] = "neutral"
				state["mecanismo"] = "neutral"

		# Hatch panel alto; garra y piston

		if state["posicion"] == "alta" and state["mecanismo"] == "piston":
			state["timer_lift_taller"] += 1
			if state["timer_lift_taller"] < 200:
				state["lift_motor"] = 1
			elif state["timer_lift_taller"] < 235:
				state["piston_activated"] = True
			elif state["timer_lift_taller"] < 270:
				state["piston_activated"] = False
			elif state["timer_lift_taller"] < 470:
				state["lift_motor"] = -1
			else:
				state["timer_lift_taller"] = 0
				state["posicion"] = "neutral"
				state["mecanismo"] = "neutral"

		if state["posicion"] == "alta" and state["mecanismo"] == "garra":
			state["timer_lift_taller"] += 1
			if state["timer_lift_taller"] < 200:
				state["lift_motor"] = 1
			elif state["timer_lift_taller"] < 235:
				state["wheeler_motor"] = 1
			elif state["timer_lift_taller"] < 435:
				state["lift_motor"] = -1
			else:
				state["timer_lift_taller"] = 0
				state["posicion"] = "neutral"
				state["mecanismo"] = "neutral"

		# Configuracion para mover el elevador y la garra manualmente 


		self.lift_motor.set(state["lift_motor"])
		self.lift_motor_2.set(state["lift_motor"])

		self.wheeler_motor.set(state["wheeler_motor"])
		self.claw_motor.set(state["claw_motor"])
	

		# Pistons and Compressor

		# self.piston.set(state["piston_activated"])
		self.piston.set(state["piston_activated"])

		if self.PSV:
			self.Compressor.stop()
		else:
			self.Compressor.start()



	def PID (self):

		error = state["setpoint"] - 400#self.encoder.get()
		self.integral = self.integral + (error*.02)
		derivative = (error - self.previous_error) / .02
		self.rcw = self.P*error + self.I*self.integral + self.D*derivative
		# print (self.rcw)


#funcion para correr el código del robot utlizando
# este archivo como el principal

if __name__ == '__main__':
	wpilib.run(MyRobot)
