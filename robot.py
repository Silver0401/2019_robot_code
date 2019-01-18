
import wpilib
from wpilib.drive import MecanumDrive
from state import state
import oi
import time



class MyRobot(wpilib.TimedRobot):

	def robotInit(self):


		#motores

		self.frontLeftMotor = wpilib.Talon(0)
		self.rearLeftMotor = wpilib.Talon(1)
		self.frontRightMotor = wpilib.Talon(2)
		self.rearRightMotor = wpilib.Talon(3)
		

		#lift_claw_motors

		self.lift_motor = wpilib.Talon(4)
		self.up_claw_motor = wpilib.Talon(5)
		self.down_claw_motor = wpilib.Talon(6)

		#push tube		
		
		self.piston = wpilib.Talon(7)

		#sensores

		self.sensor_izquierdo = wpilib.DigitalInput(1)
		self.sensor_principal = wpilib.DigitalInput(2)
		self.sensor_derecho = wpilib.DigitalInput(3)
		#invertidores de motores

		self.frontLeftMotor.setInverted(True)
		self.rearLeftMotor.setInverted(True)

		#Unión de los motores para su funcionamiento
		# en conjunto de mecaunm

		self.drive = MecanumDrive(
			self.frontLeftMotor,
			self.rearLeftMotor,
			self.frontRightMotor,
			self.rearRightMotor)
										
	def teleopPeriodic(self):   

		#se leen constantemente los botones y joysticks

		oi.read_all_controller_inputs()

		#código para el funcionamiento del movimiento
		# de las mecanum a través del control de xbox

		x = state["mov_x"] * .7
		y = state["mov_y"] * .7
		z = state["mov_z"] * .7

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
			self.drive.driveCartesian(powerX, powerY, powerZ, 0)
			
		#código para el funcionamiento del elevador y la garra. Hatch pannel bajo.
        
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


		#código para el funcionamiento del elevador y la garra. Hatch pannel medio. 

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


		#código para el funcionamiento del elevador y la garra. Hatch pannel alto.

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


#Piston retractil doble super cargado de energía 
		
		if state["push"]:
			self.piston.set(1)

		if state["pull"]:
			state["timer_piston"] += 1
			if state["timer_piston"] <= 100:
		 		self.piston.set(-1)

			
			else:
				self.piston.set(0)
				print (state)

		else:
			state["timer_piston"] = 0

#funcion para correr el código del robot utlizando
# este archivo como el principal

if __name__ == '__main__':
	wpilib.run(MyRobot)
