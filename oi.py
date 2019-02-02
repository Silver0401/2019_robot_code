

from state import state
import wpilib 
import ControlPico as Controller_inputs

def read_control_inputs():

	chasis_controller = wpilib.Joystick(1)
	abilities_controller = wpilib.Joystick(0)

def read_chasis_inputs():

	chasis_controller = wpilib.Joystick(1)

	x = chasis_controller.getX()
	state["mov_x"] = x

	y = chasis_controller.getY()
	state["mov_y"] = y

	z = chasis_controller.getRawAxis(4)
	state["mov_z"] = z

	button_1 = chasis_controller.getRawButton(Controller_inputs.acomodarse)
	state["align_activated"] = button_1

def read_abilities_inputs():

	abilities_controller = wpilib.Joystick(0)

	button_2 = abilities_controller.getRawButton(Controller_inputs.subir_plataforma_abajo)
	state["activating_lift_short"] = button_2

	#button_3 = abilities_controller.getRawButton(Controller_inputs.subir_plataforma_medio)
	#state["activating_lift_middle"] = button_3

	button_4 = abilities_controller.getRawButton(Controller_inputs.subir_plataforma_alto)
	state["activating_lift_taller"] =  button_4

	button_5 = abilities_controller.getRawButton(Controller_inputs.encoder)
	state["encoder"] =  button_5

	#piston tube configuration as well as inputs

	
	Compressor_button = abilities_controller.getRawButton(7)
	state["Compressor_activated"] = Compressor_button

	turn_piston_on = abilities_controller.getRawButton(Controller_inputs.prender_piston)  
	turn_piston_off = abilities_controller.getRawButton(Controller_inputs.apagar_piston)



	if turn_piston_on or state["is_pushing"] == 1:
		state["is_pushing"] = 1


	if  turn_piston_off:
		state["timer_piston"] += 1
		if state["timer_piston"] <= 100:
			state["is_pushing"] = 2





	

	

















