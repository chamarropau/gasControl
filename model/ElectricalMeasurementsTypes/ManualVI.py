from model.ElectricalMeasurementsTypes.ElectricalMeasurementType import ElectricalMeasurementType

class ManualVI(ElectricalMeasurementType):
    def __init__(self, keithley, current, current_unit, measurement_time):
        super().__init__(keithley, measurement_time)
        self.current = current
        self.current_unit = current_unit

    def run(self, barrier=None, stop_event=None):     
        v = self.keithley.set_current(self.current, unit=self.current_unit)
        self.voltage = v

        if barrier is not None:
            barrier.wait()