from state import state
import wpilib 
import ControlPico as robot_controller

def read_all_controller_inputs():

	#Chasis Inputs

	controller = wpilib.Joystick(0)


	x = controller.getX()
	state["mov_x"] = x

	y = controller.getY()
	state["mov_y"] = y

	z = controller.getRawAxis(4)
	state["mov_z"] = z

	button_x = controller.getRawButton(4)
	state["button_x_active"] = button_x

	#Lift_inputs and claw_inputs

	button_y = controller.getRawButton(5)
	state["activating_lift_short"] = button_y

	button_a = controller.getRawButton(3)
	state["activating_lift_middle"] = button_a

	button_W = controller.getRawButton(6)
	state["activating_lift_taller"] =  button_W


	#piston_tube_configuration

	boton_a = controller.getRawButton(2)
	state["boton_a"] = boton_a

	button_b_is_pressed = controller.getRawButton(robot_controller.prender_piston)  
	button_r_is_pressed = controller.getRawButton(robot_controller.apagar_piston)


	if button_b_is_pressed or state["is_pushing"] == 1:
		state["is_pushing"] = 1


	if  button_r_is_pressed:
		state["timer_piston"] += 1
		if state["timer_piston"] <= 100:
			state["is_pushing"] = 2
		else:
			state["is_pushing"] = 0
















