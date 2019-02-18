#Lugar donde se guardan  y declaran las variables 
# utilizadas a través del control, entre otras.

state = {

# Control

	"Controller": "ControlPico",

#Variables del Chasis

	"turbo_activated": False,
	"align_activated": False,
	"mov_x": 0,
	"mov_y": 0,
	"mov_z": 0,

#Variables del Piston y garra

	"piston_activated": False,
	"timer_piston":0,
	"claw_motor": 0,
	"wheeler_motor": 0,
	"timer_garra":0,
	"posicion_garra": "arriba",
	


# Variables del Elevador

	"lift_motor": 0,
	"timer_lift_low": 0,
	"timer_lift_middle": 0,
	"timer_lift_taller": 0,
	"posicion" : "neutral",
	"mecanismo": "neutral",
	"setpoint" : 0

}