
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

#________________________________________________________________________________

		# Inicializadores_de_PCM (en caso de que no arranque el PCM)

		self.Compressor = wpilib.Compressor(0)
		self.double_piston = wpilib.DoubleSolenoid(0,0,1)
		self.piston = wpilib.Solenoid(0,7)


		# self.Compressor.setClosedLoopControl(True)
		# self.enabled = self.Compressor.enabled()
		# self.PSV = self.Compressor.getPressureSwitchValue()
		
#________________________________________________________________________________


		# Contador
		k4X = 2
		self.ir = wpilib.DigitalInput(9)


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

		"""self.sensor_izquierdo = wpilib.DigitalInput(1)
		self.sensor_principal = wpilib.DigitalInput(2)
		self.sensor_derecho = wpilib.DigitalInput(3)"""


		#Unión de los motores para su funcionamiento
		# en conjunto de mecaunm
		self.motor1 = wpilib.Talon(4)
		self.encoder = wpilib.Encoder(0,1, True, k4X)

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


		if state["timer_piston"] < 400:
			self.Compressor.start()
		elif state["timer_piston"] < 500:
			self.Compressor.stop()
			self.piston.set(True)
		elif state["timer_piston"] < 600:
			self.piston.set(False)
			self.double_piston.set(2)
		elif state["timer_piston"] < 700:
			self.double_piston.set(1)
		elif state["timer_piston"]:
			self.double_piston.set(0)
 
		else:
			self.Compressor.stop()
			self.double_piston.set(0)
			self.piston.set(False)


		# # Avanzar 2.5s girar 1s avanzar 1s girar 1s avanzar 3s girar 1s avanzar 2s
		# if self.timer.get() < 2.5:
		# 	self.drive.driveCartesian(1,0,0,0)

		# elif self.timer.get() > 2.5 and self.timer.get() < 3.5:
		# 	self.drive.driveCartesian(0,0,1,0)

		# elif self.timer.get() > 3.5 and self.timer.get() < 4.5:
		# 	self.drive.driveCartesian(1,0,0,0)

		# elif self.timer.get() > 4.5 and self.timer.get() < 5.5:
		# 	self.drive.driveCartesian(0,0,1,0)

		# elif self.timer.get() > 5.5 and self.timer.get() < 6.5:
		# 	self.drive.driveCartesian(1,0,0,0)

		# elif self.timer.get() > 6.5 and self.timer.get() < 9.5:
		# 	self.drive.driveCartesian(1,0,0,0)

		# elif self.timer.get() > 9.5 and self.timer.get() < 10.5:
		# 	self.drive.driveCartesian(0,0,1,0)

		# elif self.timer.get() > 10.5 and self.timer.get() < 12.5:
		# 	self.drive.driveCartesian(1,0,0,0)

		# # elif self.timer.get() > 26.5 and self.timer.get() < 29.5:
		# # 	self.drive.driveCartesian(1,0,0,0)
		# # elif self.timer.get() > 29.5 and self.timer.get() < 31.5:
		# # 	self.drive.driveCartesian(0,0,-1,0)
		# else:
		# 	self.drive.driveCartesian(0,0,0,0)
		# 	#gire en direccion contraria en z 8 seg, avanza por 5 seg gira a la derecha 2 seg avanza 3 gira a la izq 2 seg

										
	def teleopPeriodic(self):


		#se leen constantemente los botones y joysticks
		oi.read_chasis_inputs()
		oi.read_abilities_inputs()
		oi.read_control_inputs()
		#pidcontroller.PIDController()

		#wpilib.DriverStation.reportWarning(str(self.ir.get()), False)

		#código para el funcionamiento del movimiento
		# de las mecanum a través del control de xbox

		x = state["mov_x"] * .7
		y = state["mov_y"] * .7
		z = state["mov_z"] * .5

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

		else:
			self.drive.driveCartesian(0,0,0,0)
			
		# Hatch pannel bajo. Código para el funcionamiento del elevador y la garra.
		
		if state["activating_lift_short"]:
			state["timer_lift_short"] += 1
			if state["timer_lift_short"] <= 100:
				self.lift_motor.set(1)
			elif state["timer_lift_short"] <= 200:
				self.lift_motor.set(0)
				self.up_claw_motor.set(.4)
				self.down_claw_motor.set(-.4)
			elif state["timer_lift_short"] <= 300:
				self.lift_motor.set(0)
				self.up_claw_motor.set(-.4)
				self.down_claw_motor.set(.4)
			elif state["timer_lift_short"] <= 400:
				self.lift_motor.set(-1)
				self.up_claw_motor.set(0)
				self.down_claw_motor.set(0)
			else:
				self.lift_motor.set(0)
		else:
			state["timer_lift_short"] = 0
			self.lift_motor.set(0)


		# Hatch pannel medio. Código para el funcionamiento del elevador y la garra.  

		if state["activating_lift_middle"]:
			state["timer_lift_middle"] += 1
			if state["timer_lift_middle"] <= 150:
				self.lift_motor.set(1)
			elif state["timer_lift_middle"] <= 250:
				self.lift_motor.set(0)
				self.up_claw_motor.set(.4)
				self.down_claw_motor.set(-.4)
			elif state["timer_lift_middle"] <= 350:
				self.lift_motor.set(0)
				self.up_claw_motor.set(-.4)
				self.down_claw_motor.set(.4)
			elif state["timer_lift_middle"] <= 500:
				self.lift_motor.set(-1)
				self.up_claw_motor.set(0)
				self.down_claw_motor.set(0)
			else:
				self.lift_motor.set(0)
		else:
			state["timer_lift_middle"] = 0


		# Hatch pannel alto. Código para el funcionamiento del elevador y la garra.

		if state["activating_lift_taller"]:
			state["timer_lift_taller"] += 1
			if state["timer_lift_taller"] <= 200:
				self.lift_motor.set(1)
			elif state["timer_lift_taller"] <= 300:
				self.lift_motor.set(0)
				self.up_claw_motor.set(.4)
				self.down_claw_motor.set(-.4)
			elif state["timer_lift_taller"] <= 400:
				self.lift_motor.set(0)
				self.up_claw_motor.set(-.4)
				self.down_claw_motor.set(.4)
			elif state["timer_lift_taller"] <= 600:
				self.lift_motor.set(-1)
				self.up_claw_motor.set(0)
				self.down_claw_motor.set(0)
			else:
				self.lift_motor.set(0)
		else:
			state["timer_lift_taller"] = 0


			# piston

		self.double_piston.set(state["is_pushing"])

		if state["Compressor_activated"]:
			self.Compressor.start()
		else:
			self.Compressor.stop()

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
