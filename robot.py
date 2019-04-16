#Librerias necesarias para el uso de todo el codigo

# from networktables import NetworkTables
import wpilib
from wpilib.drive import MecanumDrive
from state import state
import oi
import time


class MyRobot(wpilib.TimedRobot):

	def robotInit(self):

		# NetworkTables.initialize()
		# self.sd = NetworkTables.getTable('SmartDashboard')
		wpilib.CameraServer.launch()

		# Inicializadores_de_PCM (en caso de que no arranque el PCM)

		# self.Compressor.setClosedLoopControl(True)
		# self.enabled = self.Compressor.enabled()

		#Solenoides y Compresores
		
		self.Compressor = wpilib.Compressor(0)
		self.PSV = self.Compressor.getPressureSwitchValue()
		self.piston = wpilib.Solenoid(0,0)
		self.impulsor_frontal = wpilib.DoubleSolenoid(0,2,3)
		self.impulsor_trasero = wpilib.DoubleSolenoid(0,4,5)

		# Encoders y otros Sensores
		
		self.encoder = wpilib.Encoder(8, 7)

		self.left_sensor = wpilib.DigitalInput(0)
		self.principal_sensor = wpilib.DigitalInput(1)
		self.right_sensor = wpilib.DigitalInput(2)

		self.ultrasonic= wpilib.Ultrasonic(3,4)

		self.prueba_sensor = wpilib.DigitalInput(5)



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



		#Union de los motores para su funcionamiento
		# en conjunto de mecaunm

		self.drive = MecanumDrive(
			self.front_left_motor,
			self.rear_left_motor,
			self.front_right_motor,
			self.rear_right_motor)

		#Motor impulsor 

		self.motor_impulsor = wpilib.Talon(6)


		
	def autonomousInit(self):

		self.timer.reset()
		self.timer.start()
		state["timer_piston"] = 0
		
	def autonomousPeriodic(self):

		if self.timer.get() < .8:
			self.drive.driveCartesian(0,-0.9,0,0)
			print ("salto de la plataforma hacia atrás")
		elif self.timer.get() < 3:
			self.drive.driveCartesian(0,-0.1,0,0)
			print ("avanza un poco más, en reversa")
		elif self.timer.get() < 4.35:
			self.drive.driveCartesian(0,0,-0.4,0)
			print ("gira en su propio eje derecha/izquierda?")
		elif self.timer.get() < 6:
			self.timer.stop()
			# while self.prueba_sensor.get():
			while self.ultrasonic.getRangeMM() < 20 and self.ultrasonic.getRangeMM() > 0:
				print ("en modo de infrarrojos")
				if self.principal_sensor.get():
					self.drive.driveCartesian(0, 0, 0, 0)
					self.timer.start()
					break

				elif self.left_sensor.get():
					self.drive.driveCartesian(0.2, 0, 0, 0)
				elif self.right_sensor.get():
					self.drive.driveCartesian(-0.2, 0 ,0, 0)
				else:
					self.drive.driveCartesian(0, -0.2, 0, 0)

			else:
				self.drive.driveCartesian(0,0.3,0,0)
				print ("avanza hacia adelante hasta ultra detect")
	
		elif self.timer.get() < 6.5:
			self.piston.set(True)
			print ("psss lanzar")

		elif self.timer.get() < 7:
			self.piston.set(False)
			print ("psss retraer")


		else:
			print ("autonomo terminado")
			self.drive.driveCartesian(0,0,0,0)
		





	def teleopPeriodic(self):

		#se leen constantemente los botones,joysticks y cambia de modalidades de controles

		oi.read_control_inputs(state["Controller"])
		self.PID()
		self.timer.start()

		# Funcion del Encoder

		def Encoder(setpoint):

			state["setpoint"] = setpoint

			if self.rcw >= 660:
				state["lift_motor"] = 0.5
			elif self.rcw <= 660 and self.rcw >= 460:
				state["lift_motor"] = 0.45
			elif self.rcw <= 460 and self.rcw >= 300:
				state["lift_motor"] = 0.4
			elif self.rcw <= 300 and self.rcw >= 200:
				state["lift_motor"] = 0.35
			elif self.rcw <= 200 and self.rcw >= 102:
				state["lift_motor"] = 0.3
			elif self.rcw <= 102.00:
				state["lift_motor"] = 0


		if state["codewide_breaker"] == False:	

			# Movimiento manual de las mecanum, align y turbo

			x = state["mov_x"] 
			y = state["mov_y"] 
			z = state["mov_z"] 

			powerX = 0 if x < 0.10 and x > -0.10 else x
			powerY = 0 if y < 0.10 and y > -0.10 else y
			powerZ = 0 if z < 0.10 and z > -0.10 else z
		

			if state["align_activated"]:

				if self.principal_sensor.get():
					self.drive.driveCartesian(0, 0, 0, 0)
				elif self.left_sensor.get():
					self.drive.driveCartesian(0.2, 0, 0, 0)
				elif self.right_sensor.get():
					self.drive.driveCartesian(-0.2, 0 ,0, 0)
				else:
					self.drive.driveCartesian(0, -0.2, 0, 0)


			elif state["turbo_activated"]:

				self.drive.driveCartesian(powerX ,-powerY , powerZ, 0)

			else:
				self.drive.driveCartesian(powerX * 0.6,-powerY * 0.6, powerZ * 0.5, 0)


			# Configuracion para el elevador automaticamente

			# Hatch panel medio y piston
			

			if state["position"] == "media" and state["mechanism"] == "piston":
				state["timer_lift_middle"] += 1
				if state["timer_lift_middle"] < 240:
					Encoder(1621) 
				elif state["timer_lift_middle"] < 275:
					state["piston_activated"] = True
				elif state["timer_lift_middle"] < 310:
					state["piston_activated"] = False
				elif state["timer_lift_middle"] < 510:
					state["lift_motor"] = -0.5
				else:
					state["timer_lift_middle"] = 0
					state["position"] = "neutral"
					state["mechanism"] = "neutral"

			if state["position"] == "high" and state["mechanism"] == "piston":
				state["timer_lift_taller"] += 1
				if state["timer_lift_taller"] < 240:
					Encoder(1621) 
				elif state["timer_lift_taller"] < 275:
					state["piston_activated"] = True
				elif state["timer_lift_taller"] < 310:
					state["piston_activated"] = False
				elif state["timer_lift_taller"] < 510:
					state["lift_motor"] = -0.5
				else:
					state["timer_lift_taller"] = 0
					state["position"] = "neutral"
					state["mechanism"] = "neutral"

			# Configuracion para mover el elevador y la claw manualmente 


			self.lift_motor.set(state["lift_motor"])
			self.lift_motor_2.set(state["lift_motor"])


			# Pistons (manual) and Compressors (automatico)


			self.piston.set(state["piston_activated"])

			if self.PSV:
				self.Compressor.stop()
			else:
				self.Compressor.start()

			# Immpulsor (Manual y automaticamente)

			self.impulsor_frontal.set(state["impulsor_situation_front"])
			self.impulsor_trasero.set(state["impulsor_situation_trasero"])
			self.motor_impulsor.set(state["impulsor_motor"])


			if state["impulsor_on"] or state["timer_impulsor"] != 0:
				state["timer_impulsor"] += 1
			
				if state["timer_impulsor"] < 150:
					state["impulsor_situation_front"] = 1
					state["impulsor_situation_trasero"] = 1
				elif state["timer_impulsor"] < 180:
					state["impulsor_situation_front"] = 0
					state["impulsor_situation_trasero"] = 0
				elif state["timer_impulsor"] < 250:
					state["impulsor_motor"] = 1
				elif state["timer_impulsor"] < 400:
					state["impulsor_situation_front"] = 2
					state["impulsor_motor"] = 1
					self.drive.driveCartesian(0,0.4,0,0)
				elif state["timer_impulsor"] < 600:
					state["impulsor_situation_trasero"] = 2
					state["impulsor_motor"] = 0
				elif state["timer_impulsor"] < 700:
					self.drive.driveCartesian(0,0.6,0,0)
					state["impulsor_situation_trasero"] = 0
				else:
					state["timer_impulsor"] = 0
					state["impulsor_situation_front"] = 0
					state["impulsor_situation_trasero"] = 0
					state["impulsor_motor"] = 0
					self.drive.driveCartesian(0,0,0,0)
			else:
				pass

		else:
			self.drive.driveCartesian(0,0,0,0)
			self.impulsor_frontal.set(0)
			self.impulsor_trasero.set(0)
			self.motor_impulsor.set(0)
			self.piston.set(False)
			self.lift_motor.set(0)
			self.lift_motor_2.set(0)

			state["impulsor_trasero"] = 0
			state["impulsor_frontal"] = 0
			state["impulsor_situation_trasero"] = 0
			state["impulsor_situation_front"] = 0
			state["impulsor_motor"] = 0
			state["piston_activated"] = False
			state["lift_motor"] = 0
			state["position"] = "neutral"
			state["mechanism"] = "neutral"
			state["timer_piston"] = 0
			state["timer_impulsor"] = 0
			state["timer_lift_taller"] = 0
			state["timer_lift_middle"] = 0
			state["align_activated"] = False
			state["turbo_activated"] = False
		


	def PID (self):

		error = state["setpoint"] - 400#self.encoder.get()
		self.integral = self.integral + (error*.02)
		derivative = (error - self.previous_error) / .02
		self.rcw = self.P*error + self.I*self.integral + self.D*derivative
		# print (self.rcw)


#funcion para correr el codigo del robot utlizando
# este archivo como el principal

if __name__ == '__main__':
	wpilib.run(MyRobot)
