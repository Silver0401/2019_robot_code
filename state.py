#Lugar donde se guardan  y declaran las variables 
# utilizadas a través del control, entre otras.

state = {

# Control

	"Controller": "PacificRim",

#Variables del Chasis

	"turbo_activated": False,
	"align_activated": False,
	"mov_x": 0,
	"mov_y": 0,
	"mov_z": 0,

#Variables del Piston
	
	"piston_activated": False,
	"claw_activated": 2,
	"timer_piston":0,

# Variables del Elevador

	"lift_motor": 0,
	"claw_motor": 0,
	"timer_lift_middle": 0,
	"timer_lift_taller": 0,
	"posicion" : "neutral",
	"mecanismo": "neutral"

}