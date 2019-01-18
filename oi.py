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

	button_x = controller.getRawButton(3)
	state["button_x_active"] = button_x

	#Lift_inputs and claw_inputs

	button_y = controller.getRawButton(4)
	state["activating_lift_short"] = button_y

	button_a = controller.getRawButton(1)
	state["activating_lift_middle"] = button_a

	button_b = controller.getRawButton(2)
	state["activating_lift_taller"] =  button_b





