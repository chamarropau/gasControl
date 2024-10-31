from model.ElectricalMeasurementsTypes.ManualVI import ManualVI
from model.ElectricalMeasurementsTypes.ManualIV import ManualIV
from model.ElectricalMeasurementsTypes.AutomaticVI import AutomaticVI
from model.ElectricalMeasurementsTypes.AutomaticIV import AutomaticIV
from model.ElectricalMeasurementsTypes.AutomaticVT import AutomaticVT
from model.ElectricalMeasurementsTypes.AutomaticIT import AutomaticIT
from model.DataManager import DataManager
from termcolor import colored
from threading import Thread, Barrier, Event
import time

class ManualMode:
    def __init__(self, keithleys, mfcs, mfcs_flows):
        self.mfcs = mfcs
        self.mfcs_flows = mfcs_flows
        self.keithleys = keithleys
        self.electrical_measurement = None
        self.thread = None
        self.barrier = Barrier(2)
        self.data_manager = None
        self.stop_event = Event()

    def run(self):
        self.set_mfcs_flows()
        if self.electrical_measurement is not None:    
            self.thread = Thread(target = self.electrical_measurement.run, args=(self.barrier, self.stop_event))
            self.thread.start()
            if self.data_manager is None:
                raise Exception(f"{colored('[ERROR]', 'red')} No data manager created. Use set_data_manager method after run mode")
            data = self.data_manager.run(self.barrier)
            self.thread.join()
            return data
        else:
            raise Exception("No electrical measurement selected")
        
    def set_mfcs_flows(self):
        # {id, flow} set to the 
        for id, flow in self.mfcs_flows.items():
            flow_setted = self.mfcs.set_no_error_flow(id, flow)
            print(id)
            print(flow)
            print(flow_setted)

    def set_manual_VI_measurement(self, current, current_unit, measurement_time):
        self.electrical_measurement = ManualVI(self.keithleys[0], current, current_unit, measurement_time)

    
    def set_manual_IV_measurement(self, voltage, voltage_unit, measurement_time):
        self.electrical_measurement = ManualIV(self.keithleys[0], voltage, voltage_unit, measurement_time)
        
    
    def set_automatic_VI_measurement(self, initial_current, final_current, current_unit, n_points_current, measurement_time):
        self.electrical_measurement = AutomaticVI(self.keithleys[0], initial_current, final_current, current_unit, n_points_current, measurement_time)

    
    def set_automatic_IV_measurement(self, initial_voltage, final_voltage, voltage_unit, n_points_voltage, measurement_time):
        self.electrical_measurement = AutomaticIV(self.keithleys[0], initial_voltage, final_voltage, voltage_unit, n_points_voltage, measurement_time)

    
    def set_automatic_VT_measurement(self, current, current_unit, measurement_time):
        self.electrical_measurement = AutomaticVT(self.keithleys[0], current, current_unit, measurement_time)

    
    def set_automatic_IT_measurement(self, voltage, voltage_unit, measurement_time):
        self.electrical_measurement = AutomaticIT(self.keithleys[0], voltage, voltage_unit, measurement_time)


    def set_data_manager(self, mfc, data_measurement, measurement_time, ad_time, sv_time):
        self.data_manager = DataManager(mfc, [self.electrical_measurement], data_measurement, measurement_time, ad_time, sv_time)