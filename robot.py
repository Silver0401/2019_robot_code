
import wpilib
from wpilib.drive import MecanumDrive
from state import state
import oi
import time




class MyRobot(wpilib.TimedRobot):

	def robotInit(self):

#________________________________________________________________________________

		#Inicializadores_de_PCM (en caso de que no arranque el PCM)

		# self.Compressor.setClosedLoopControl(True)
		# self.enabled = self.Compressor.enabled()
		# self.PSV = self.Compressor.getPressureSwitchValue()
		
#________________________________________________________________________________


		# Contador

		self.timer = wpilib.Timer()

		# Motores

		self.front_left_motor = wpilib.Talon(0)
		self.rear_left_motor = wpilib.Talon(1)
		self.front_right_motor = wpilib.Talon(2)
		self.rear_right_motor = wpilib.Talon(3)

		#Push tube
		
		self.Compressor = wpilib.Compressor(0)
		self.piston = wpilib.DoubleSolenoid(0,0,1)


		#lift_claw_motors

		self.lift_motor = wpilib.Talon(4)
		self.up_claw_motor = wpilib.Talon(5)
		self.down_claw_motor = wpilib.Talon(6)

		#sensores

		self.sensor_izquierdo = wpilib.DigitalInput(1)
		self.sensor_principal = wpilib.DigitalInput(2)
		self.sensor_derecho = wpilib.DigitalInput(3)


		#Unión de los motores para su funcionamiento
		# en conjunto de mecaunm

		self.drive = MecanumDrive(
			self.front_left_motor,
			self.rear_left_motor,
			self.front_right_motor,
			self.rear_right_motor)


	def autonomousInit(self):
		"""This function is run once each time the robot enters autonomous mode."""
		self.timer.reset()
		self.timer.start()
		
	def autonomousPeriodic(self):
		"""This function is called periodically during autonomous."""

		pass
		# Avanzar 2.5s girar 1s avanzar 1s girar 1s avanzar 3s girar 1s avanzar 2s


										
	def teleopPeriodic(self):	


		#se leen constantemente los botones y joysticks

		oi.read_all_controller_inputs()

		#código para el funcionamiento del movimiento
		# de las mecanum a través del control de xbox

		x = state["mov_x"] * .7
		y = state["mov_y"] * .7
		z = state["mov_z"] * .5

		powerX = 0 if x < 0.15 and x > -0.15 else x
		powerY = 0 if y < 0.15 and y > -0.15 else y
		powerZ = 0 if z < 0.15 and z > -0.15 else z
	

		if state["button_x_active"]:
			if self.sensor_principal.get():
				self.drive.driveCartesian(0, 0, 0, 0)
			elif self.sensor_izquierdo.get():
				self.drive.driveCartesian(0.4, 0, 0, 0)
			elif self.sensor_derecho.get():
				self.drive.driveCartesian(-0.4, 0 ,0, 0)
			else:
				self.drive.driveCartesian(0, -0.5, 0, 0)

		else:
			self.drive.driveCartesian(powerX, -powerY, powerZ, 0)
			
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


		# codigo_del_piston

		self.piston.set(state["is_pushing"])

		if state["is_pushing"] == 1:
			self.Compressor.start()
		else:
			self.Compressor.stop()




#funcion para correr el código del robot utlizando
# este archivo como el principal

if __name__ == '__main__':
	wpilib.run(MyRobot)
