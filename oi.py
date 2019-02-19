
# Se importa el control requerido automáticamente

from state import state
import wpilib 

if state["Controller"] == "PacificRim":
	import PacificRim as Controller_inputs

elif state["Controller"] == "ControlPico":
	import ControlPico as Controller_inputs

elif state["Controller"] == "ControlPelon":
	import ControlPelon as Controller_inputs



def read_control_inputs(control_type):

	if control_type == "PacificRim":

		read_chasis_inputs(0)
		read_abilities_inputs(1)

	elif control_type == "ControlPico" or control_type == "ControlPelon":

		read_abilities_inputs(0)
		read_chasis_inputs(0)

	else:

		print ("Non-existent control type")
		wpilib.DriverStation.reportWarning(str("Non-existent control type"),True)


def read_chasis_inputs(control_port):

	chasis_controller = wpilib.Joystick(control_port)

	x = chasis_controller.getX()
	state["mov_x"] = x

	y = chasis_controller.getY()
	state["mov_y"] = y

	z = chasis_controller.getRawAxis(4)
	state["mov_z"] = z

	button_1 = chasis_controller.getRawButton(Controller_inputs.accomodate)
	state["align_activated"] = button_1

	button_2 = chasis_controller.getRawButton(Controller_inputs.turbo)
	state["turbo_activated"] = button_2


def read_abilities_inputs(control_port):

	abilities_controller = wpilib.Joystick(control_port)

	# botones del elevador y predeterminados

	button_lift_up = abilities_controller.getRawButton(Controller_inputs.up_by_hand)
	button_lift_down = abilities_controller.getRawButton(Controller_inputs.down_by_hand)
	eje_t = abilities_controller.getZ()
	eje_z =abilities_controller.getThrottle()

	button_medio_piston = abilities_controller.getRawButton(Controller_inputs.up_platform_middle_piston)
	button_alto_piston = abilities_controller.getRawButton(Controller_inputs.up_platform_high_piston)

	button_medio_garra = abilities_controller.getRawButton(Controller_inputs.up_platform_middle_claw)
	button_alto_garra = abilities_controller.getRawButton(Controller_inputs.up_platform_high_claw
		)

	# Uso de los botones


	if button_lift_up and state["Controller"] == "PacificRim" or state["Controller"] == "ControlPico" and eje_t > 0:
		state["lift_motor"] = 0.5

	elif button_lift_down and state["Controller"] == "PacificRim" or state["Controller"] == "ControlPico" and eje_z > 0:
		state["lift_motor"] = -1
	else:
		state["lift_motor"] = 0

	
	if button_medio_piston:

		state["position"] = "media"
		state["mechanism"] = "piston"

	elif button_alto_piston:

		state["position"] = "high"
		state["mechanism"] = "piston"


	elif button_medio_garra:

		state["position"] = "media"
		state["mechanism"] = "garra"


	elif button_alto_garra:

		state["position"] = "high"
		state["mechanism"] = "garra"


	#Inputs de Solenoides, pistones, wheelers y subir o bajar garra


	succionar_wheelers = abilities_controller.getRawButton(Controller_inputs.sucks_wheelers)  
	aventar_wheelers = abilities_controller.getRawButton(Controller_inputs.throw_wheelers)
	subir_bajar_garra = abilities_controller.getRawButton(Controller_inputs.claw_turn_on)
	turn_piston_on = abilities_controller.getRawButton(Controller_inputs.on_and_off_piston)
	
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

	if subir_bajar_garra or state["claw_timer"] != 0:
		state["claw_timer"] += 1
		if state["claw_position"] == "abajo":
			if state["claw_timer"] < 100: 
				state["claw_motor"] = 0.5
			else:
				state["claw_timer"] = 0
				state["claw_position"] = "up"
		elif state["claw_position"] == "up":	
			if state["claw_timer"] < 100: 
				state["claw_motor"] = -0.5
			else:
				state["claw_timer"] = 0
				state["claw_position"] = "abajo"
	else:
		state["claw_motor"] = 0
	


		





















