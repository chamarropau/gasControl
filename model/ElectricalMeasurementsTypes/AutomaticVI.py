from model.ElectricalMeasurementsTypes.ElectricalMeasurementType import ElectricalMeasurementType

import time
import numpy as np

class AutomaticVI(ElectricalMeasurementType): 
    def __init__(self, keithley, \
                 initial_current, final_current, current_unit, current_step, measurement_time):
        super().__init__(keithley, measurement_time)
        self.initial_current = initial_current
        self.final_current = final_current
        self.current_step = current_step
        self.current_unit = current_unit
        self.measurement_time = measurement_time

    def run(self, barrier=None, stop_event=None):
        
        current_list = np.linspace(self.initial_current, self.final_current, self.current_step)
        delay_time = float(self.measurement_time) / len(current_list)
        for n, current in enumerate(current_list):
            if stop_event is not None and stop_event.is_set():
                break
            init_time = time.time()
            v = self.keithley.set_current(current, unit=self.current_unit)
            self.voltage = v
            self.current = current
            if barrier is not None and n == 0:
                barrier.wait()

            else:
                time.sleep(delay_time - (time.time() - init_time))