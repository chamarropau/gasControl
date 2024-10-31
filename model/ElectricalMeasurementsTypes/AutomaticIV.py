from model.ElectricalMeasurementsTypes.ElectricalMeasurementType import ElectricalMeasurementType

import time
import numpy as np

class AutomaticIV(ElectricalMeasurementType):
    def __init__(self, keithley, \
                 initial_voltage, final_voltage, voltage_unit, voltage_step, measurement_time):
        super().__init__(keithley, measurement_time)
        self.initial_voltage = initial_voltage
        self.final_voltage = final_voltage
        self.voltage_step = voltage_step
        self.voltage_unit = voltage_unit
        self.measurement_time = measurement_time

    def run(self, barrier=None, stop_event=None):
        voltage_list = np.linspace(self.initial_voltage, self.final_voltage, self.voltage_step)
        delay_time = float(self.measurement_time) / len(voltage_list)

        for n, voltage in enumerate(voltage_list):
            if stop_event is not None and stop_event.is_set():
                break
            init_time = time.time()
            i = self.keithley.set_voltage(voltage, unit=self.voltage_unit)
            self.voltage = voltage
            self.current = i
            if barrier is not None and n == 0:
                barrier.wait()

            else:
                time.sleep(delay_time - (time.time() - init_time))
