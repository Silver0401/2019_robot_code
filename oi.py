from state import state
import wpilib 
import ControlPico as Controller_inputs

def read_all_controller_inputs():

	#Chasis Inputs

	controller = wpilib.Joystick(0)


	x = controller.getX()
	state["mov_x"] = x

	y = controller.getY()
	state["mov_y"] = y

	z = controller.getRawAxis(4)
	state["mov_z"] = z

	button_1 = controller.getRawButton(3)
	state["align_activated"] = button_1

	#Lift_inputs and claw_inputs

	button_2 = controller.getRawButton(4)
	state["activating_lift_short"] = button_2

	button_3 = controller.getRawButton(5)
	state["activating_lift_middle"] = button_3

	button_4 = controller.getRawButton(6)
	state["activating_lift_taller"] =  button_4


	#piston tube configuration as well as inputs

	button_5_is_pressed = controller.getRawButton(Controller_inputs.prender_piston)  
	button_6_is_pressed = controller.getRawButton(Controller_inputs.apagar_piston)


	if button_5_is_pressed or state["is_pushing"] == 1:
		state["is_pushing"] = 1


	if  button_6_is_pressed:
		state["timer_piston"] += 1
		if state["timer_piston"] <= 100:
			state["is_pushing"] = 2
		else:
			state["is_pushing"] = 0
















