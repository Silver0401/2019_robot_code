from state import state
import wpilib


def read_all_controller_inputs():

	#Chasis Inputs

	controller = wpilib.Joystick(0)


	x = controller.getX()
	state["mov_x"] = x

	y = controller.getY()
	state["mov_y"] = y

	z = controller.getZ()
	state["mov_z"] = z

	button_x = controller.getRawButton(1)
	state["button_x_active"] = button_x

	#Lift_inputs and claw_inputs

	button_y = controller.getRawButton(2)
	state["activating_lift_short"] = button_y

	button_a = controller.getRawButton(3)
	state["activating_lift_middle"] = button_a

	button_W = controller.getRawButton(4)
	state["activating_lift_taller"] =  button_W


	#piston tube
	button_b = controller.getRawButton(6)  
	state["push"] = button_b

	button_R = controller.getRawButton(5)
	state["pull"] = button_R










