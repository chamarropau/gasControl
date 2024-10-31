from model.ElectricalMeasurementsTypes.ElectricalMeasurementType import ElectricalMeasurementType

import time

class AutomaticVT(ElectricalMeasurementType):
    def __init__(self, keithley, \
                 current, current_unit, measurement_time):
        super().__init__(keithley, measurement_time)
        self.current = current
        self.current_unit = current_unit
        self.measurement_time = measurement_time

    def run(self, barrier=None, stop_event=None):
        
        self.keithley.set_current(self.current, unit = self.current_unit)
        if barrier is not None:
            barrier.wait()
        v = self.keithley.get_voltage()
        self.voltage = v
        init_time = time.time()

        while time.time() - init_time < self.measurement_time:
            if stop_event is not None and stop_event.is_set():
                break
            v = self.keithley.get_voltage()
            self.voltage = v
            time.sleep(2)