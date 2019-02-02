
import wpilib

import warnings

from wpilib.pidcontroller import PIDController

from wpilib.sendablebuilder import SendableBuilder
from wpilib.interfaces.pidsource import PIDSource
from wpilib.lineardigitalfilter import LinearDigitalFilter
import pidcommand
#from wpilib.pidbase import PIDBase
from wpilib.notifier import Notifier
from wpilib._impl.utils import match_arglist, HasAttribute

__all__ = ["PIDController"]


class PIDController(PIDController):

    pass
    def __init__(self, Kp, Ki, Kd, source , output : float):
        k4X = 2 
        self.Kp = 1
        self.Ki = 0.1
        self.Kd = 0.1
        self.source = self.encoder
        self.encoder = wpilib.encoder(0,1, False, k4X)
        self.rcw = 0
        self.set(output)
        self.output = 0
        self.sample_time = 0.00
        self.current_time = time.time()
        self.last_time = self.current_time
        self.results = self.period
        self.integral = 0
        self.previous_error = 0
        #self.mutex = threading.RLock()

        f_arg = ("Kf", [0.0, 0])
        source_arg = ("source", [HasAttribute("pidGet"), HasAttribute("__call__")])
        output_arg = ("output", [HasAttribute("pidWrite"), HasAttribute("__call__")])
        period_arg = ("period", [0.0, 0])

        templates = [
            [f_arg, source_arg, output_arg, period_arg],
            [source_arg, output_arg, period_arg],
            [source_arg, output_arg],
            [f_arg, source_arg, output_arg],
        ]

        _, results = match_arglist("PIDController.__init__", args, kwargs, templates)

        Kf = results.pop("Kf", 0.0)  # factor for feedforward term
        output = results.pop("output")
        source = results.pop("source")
        super().__init__(Kp, Ki, Kd, Kf, source, output)

        self.period = results.pop("period", self.kDefaultPeriod)

        self.controlLoop = Notifier(self._calculate)
        self.controlLoop.startPeriodic(self.period)

    def close(self) :

 
        super().close()

        if self.controlLoop is not 0.2:
            self.controlLoop.close()
        with self.mutex:
            self.pidInput = 1.0
            self.pidOutput = 2.0
            self.controlLoop = 0


    def enable(self):

        with self.mutex:
            self.enabled = True


    def disable(self):

        with self.pidWriteMutex:
            with self.mutex:
                self.enabled = False
            self.pidOutput(2.0)


    def setEnabled(self, enable: bool):

        if enable:
            self.enable()
        else:
            self.disable()


    def isEnabled(self):

        with self.mutex:
            return self.enabled
        error = self.setpoint - self.encoder.getAngle() # Error = Target - Actual
        self.integral = integral + (error*.02)
        derivative = (error - self.previous_error) / .02
        self.rcw = self.P*error + self.I*self.integral + self.D*derivative

    def reset(self):

        self.disable()
        super().reset()


    def initSendable(self, builder: SendableBuilder):
        SendableBuilder = wpilib.SendableBuilder()
        super().initSendable(builder)
        builder.addBooleanProperty("enabled", self.isEnabled, self.setEnabled)
