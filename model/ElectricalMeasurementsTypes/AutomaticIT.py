from model.ElectricalMeasurementsTypes.ElectricalMeasurementType import ElectricalMeasurementType

import time

class AutomaticIT(ElectricalMeasurementType):
    def __init__(self, keithley, \
                 voltage, voltage_unit, measurement_time):
        super().__init__(keithley, measurement_time)
        self.voltage = voltage
        self.voltage_unit = voltage_unit
        self.measurement_time = measurement_time

    def run(self, barrier=None, stop_event=None):
        self.keithley.set_voltage(self.voltage, unit = self.voltage_unit)
        i = self.keithley.get_current()
        if barrier is not None:
            barrier.wait()
        self.current = i
        init_time = time.time()

        while time.time() - init_time < self.measurement_time:
            if stop_event is not None and stop_event.is_set():
                break
            i = self.keithley.get_current()
            self.current = i
            time.sleep(2)
        