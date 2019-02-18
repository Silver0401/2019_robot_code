
# Se importa el control requerido automáticamente

from state import state
import wpilib 

if state["Controller"] == "PacificRim":
	import PacificRim as Controller_inputs

elif state["Controller"] == "ControlPico":
	import ControlPico as Controller_inputs

elif state["Controller"] == "ControlPelon":
	import ControlPelon as Controller_inputs



def read_control_inputs(tipo_de_control):

	if tipo_de_control == "PacificRim":

		read_chasis_inputs(0)
		read_abilities_inputs(1)

	elif tipo_de_control == "ControlPico" or tipo_de_control == "ControlPelon":

		read_abilities_inputs(0)
		read_chasis_inputs(0)

	else:

		print ("tipo de control inexistente")
		wpilib.DriverStation.reportWarning(str("tipo de control inexistente"),True)


def read_chasis_inputs(puerto_del_control):

	chasis_controller = wpilib.Joystick(puerto_del_control)

	x = chasis_controller.getX()
	state["mov_x"] = x

	y = chasis_controller.getY()
	state["mov_y"] = y

	z = chasis_controller.getRawAxis(4)
	state["mov_z"] = z

	button_1 = chasis_controller.getRawButton(Controller_inputs.acomodarse)
	state["align_activated"] = button_1

	button_2 = chasis_controller.getRawButton(Controller_inputs.turbo)
	state["turbo_activated"] = button_2


def read_abilities_inputs(puerto_del_control):

	abilities_controller = wpilib.Joystick(puerto_del_control)

	# botones del elevador y predeterminados

	button_lift_up = abilities_controller.getRawButton(Controller_inputs.subir_manualmente)
	button_lift_down = abilities_controller.getRawButton(Controller_inputs.bajar_manualmente)
	eje_t = abilities_controller.getZ()
	eje_z =abilities_controller.getThrottle()

	button_medio_piston = abilities_controller.getRawButton(Controller_inputs.subir_plataforma_medio_piston)
	button_alto_piston = abilities_controller.getRawButton(Controller_inputs.subir_plataforma_alto_piston)

	button_medio_garra = abilities_controller.getRawButton(Controller_inputs.subir_plataforma_medio_garra)
	button_alto_garra = abilities_controller.getRawButton(Controller_inputs.subir_plataforma_alto_garra)

	# Uso de los botones


	if button_lift_up and state["Controller"] == "PacificRim" or state["Controller"] == "ControlPico" and eje_t > 0:
		state["lift_motor"] = 1

	elif button_lift_down and state["Controller"] == "PacificRim" or state["Controller"] == "ControlPico" and eje_z > 0:
		state["lift_motor"] = -1
	else:
		state["lift_motor"] = 0

	
	if button_medio_piston:

		state["posicion"] = "media"
		state["mecanismo"] = "piston"

	elif button_alto_piston:

		state["posicion"] = "alta"
		state["mecanismo"] = "piston"


	elif button_medio_garra:

		state["posicion"] = "media"
		state["mecanismo"] = "garra"


	elif button_alto_garra:

		state["posicion"] = "alta"
		state["mecanismo"] = "garra"


	#Inputs de Solenoides, pistones, wheelers y subir o bajar garra


	succionar_wheelers = abilities_controller.getRawButton(Controller_inputs.succionar_wheelers)  
	aventar_wheelers = abilities_controller.getRawButton(Controller_inputs.aventar_wheelers)
	subir_bajar_garra = abilities_controller.getRawButton(Controller_inputs.prender_garra)
	turn_piston_on = abilities_controller.getRawButton(Controller_inputs.prender_y_apagar_piston)
	
	#Configuracion para el uso de pistones

	if turn_piston_on or state["timer_piston"] != 0:
		state["timer_piston"] += 1
		if state["timer_piston"] < 35: 
			state["piston_activated"] = True
		elif state["timer_piston"] < 60:
			state["piston_activated"] = False
		else:
			state["timer_piston"] = 0


	#Configuracion de los wheelers
		
	if succionar_wheelers:
		state["wheeler_motor"] = -0.4

	elif aventar_wheelers:
		state["wheeler_motor"] = 0.4

	else:
		state["wheeler_motor"] = 0


	#Configuracion garra

	if subir_bajar_garra or state["timer_garra"] != 0:
		state["timer_garra"] += 1
		if state["posicion_garra"] == "abajo":
			if state["timer_garra"] < 100: 
				state["claw_motor"] = 0.5
			else:
				state["timer_garra"] = 0
				state["posicion_garra"] = "arriba"
		elif state["posicion_garra"] == "arriba":	
			if state["timer_garra"] < 100: 
				state["claw_motor"] = -0.5
			else:
				state["timer_garra"] = 0
				state["posicion_garra"] = "abajo"
	else:
		state["claw_motor"] = 0
	


		





















