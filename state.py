#Lugar donde se guardan  y declaran las variables 
# utilizadas a través del control, entre otras.

state = {

# Control

	"Controller": "ControlPelon",

	"codewide_breaker": False,

#Variables del Chasis

	"turbo_activated": False,
	"align_activated": False,
	"mov_x": 0,
	"mov_y": 0,
	"mov_z": 0,

#Variables del Piston e impulsor e impulsor motor

	"piston_activated": False,
	"timer_piston":0,
	"timer_impulsor":0,
	"impulsor_situation_trasero":0,
	"impulsor_situation_front":0,
	"impulsor_motor":0,
	"timer_impulsor_motor":0,
	"impulsor_on": False,
	

# Variables del Elevador

	"lift_motor": 0,
	"timer_lift_middle": 0,
	"timer_lift_taller": 0,
	"position" : "neutral",
	"mechanism": "neutral",
	"setpoint" : 0

}