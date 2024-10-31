from model.ElectricalMeasurementsTypes.ElectricalMeasurementType import ElectricalMeasurementType
from time import time

class ManualIV(ElectricalMeasurementType):
    def __init__(self, keithley, voltage, voltage_unit, measurement_time):
        super().__init__(keithley, measurement_time)
        self.voltage = voltage
        self.voltage_unit = voltage_unit

    def run(self, barrier=None, stop_event=None):
        i = self.keithley.set_voltage(self.voltage, unit=self.voltage_unit)
        self.current = i
        
        if barrier is not None:
            barrier.wait()

        


    