
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

	# botones del elevador con pistones

	abilities_controller = wpilib.Joystick(puerto_del_control)

	button_12 = abilities_controller.getRawButton(Controller_inputs.subir_plataforma_abajo1)
	button_10 = abilities_controller.getRawButton(Controller_inputs.subir_plataforma_medio1)
	button_8 = abilities_controller.getRawButton(Controller_inputs.subir_plataforma_alto1)

	# botones del elevador con garra

	button_11 = abilities_controller.getRawButton(Controller_inputs.subir_plataforma_abajo2)
	button_9 = abilities_controller.getRawButton(Controller_inputs.subir_plataforma_medio2)
	button_7 = abilities_controller.getRawButton(Controller_inputs.subir_plataforma_alto2)

	# funciones para el uso del elevador

	if button_12:
		state["posicion"] = 1
		state["mecanismo"] = 1

	elif button_10:

		state["posicion"] = 2
		state["mecanismo"] = 1

	elif button_8:

		state["posicion"] = 3
		state["mecanismo"] = 1


	elif button_11:

		state["posicion"] = 1
		state["mecanismo"] = 2


	elif button_9:

		state["posicion"] = 2
		state["mecanismo"] = 2


	elif button_7:

		state["posicion"] = 3
		state["mecanismo"] = 2


	#Inputs de Solenoides, pistones y compresoras
	
	Compressor_button = abilities_controller.getRawButton(7)
	state["Compressor_activated"] = Compressor_button

	turn_double_piston_on = abilities_controller.getRawButton(Controller_inputs.prender_garra)  
	turn_double_piston_off = abilities_controller.getRawButton(Controller_inputs.apagar_garra)
	turn_piston_on = abilities_controller.getRawButton(Controller_inputs.prender_piston)
	turn_piston_off = abilities_controller.getRawButton(Controller_inputs.apagar_piston)


	#Configuracion para el uso de pistones


	if turn_piston_on or state["piston_activated"] == True:
		state["piston_activated"] = True

	if  turn_piston_off or state["piston_activated"] == False:
			state["piston_activated"] = False

	if turn_double_piston_on or state["claw_activated"] == 1:
		state["claw_activated"] = 1

	if  turn_double_piston_off or state["claw_activated"] == 2:
			state["claw_activated"] = 2


	#Encoders


	

	

















