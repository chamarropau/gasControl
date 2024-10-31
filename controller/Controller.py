from model.ManualMode import ManualMode
from model.AutomaticMode import AutomaticMode
from model.AutoMode import AutoMode
from packets.DataMeasurement.DataMeasurement import DataMeasurement
from packets.DataMeasurement.DataMeasurementFake import DataMeasurementFake
from packets.Keithley.Keithley import Keithley
from packets.Keithley.KeithleyFake import KeithleyFake
from model.MassFlowController import MassFlowController

class Controller:
    def __init__(self, mode=None):
        self.mode = mode # This gonna be manual or automatic mode
        config_1 = {'interface': 'Ethernet 3', 'ip': '192.168.100.2', 'mask': '255.255.255.128', 'gateway': '192.168.100.1'}
        config_2 = {'interface': 'Ethernet 4', 'ip': '192.168.100.130', 'mask': '255.255.255.128', 'gateway': '192.168.100.129'}
        # self.keithleys = [Keithley(config_1), Keithley(config_2)]
        # self.data_measurement = DataMeasurement('COM4')
        # self.mfc = MassFlowController([3,6,9,12,16,20])
        # self.mfc.clear_all_flows()

    def set_mode(self, mode, flows=None, num_keithley=None, excel=None, sheet=None):
        print(f"Number of keithleys {num_keithley}")
        if mode == "manual":
            if flows is None:
                flows = self.ask_for_flows()
            self.mode = ManualMode(self.keithleys, self.mfc, flows)

        elif mode == "automatic":
            if excel is None and sheet is None:
                excel = "./data/llibre_Input_Output_Estacio_gasos.xlsx"
                sheet = "data"
            self.mode = AutomaticMode(num_keithley, self.keithleys, self.mfc, self.data_measurement, excel, sheet)
            # self.mode = AutoMode(num_keithley, self.keithleys, self.mfc, self.data_measurement, excel, sheet)
        
    def set_manual_VI(self, current, current_unit, measurement_time):
        self.mode.set_manual_VI_measurement(current, current_unit, measurement_time)

    def set_manual_IV(self, voltage, voltage_unit, measurement_time):
        self.mode.set_manual_IV_measurement(voltage, voltage_unit, measurement_time)
        
    def set_automatic_VI(self, initial_current, final_current, current_unit, n_points_current, measurement_time): 
        self.mode.set_automatic_VI_measurement(initial_current, final_current, current_unit, n_points_current, measurement_time)

    def set_automatic_IV(self, initial_voltage, final_voltage, voltage_unit, n_points_voltage, measurement_time):
        self.mode.set_automatic_IV_measurement(initial_voltage, final_voltage, voltage_unit, n_points_voltage, measurement_time)

    def set_automatic_VT(self, current, current_unit, measurement_time):
        self.mode.set_automatic_VT_measurement(current, current_unit, measurement_time)

    def set_automatic_IT(self, voltage, voltage_unit, measurement_time):
        self.mode.set_automatic_IT_measurement(voltage, voltage_unit, measurement_time)

    def set_data_manager(self, measurement_time, ad_time, sv_time):
        self.mode.set_data_manager(self.mfc, self.data_measurement, measurement_time, ad_time, sv_time)

    def ask_for_flows(self):
        max_flows = {3: 200, 6: 200, 9: 200, 12: 200, 16: 200, 20: 20}
        
        # Ask the user to input the MFCs they want to use
        selection = input("Enter the MFC IDs you want to use, separated by commas: ")

        # Convert input into a list of integers
        selected_ids = [int(x.strip()) for x in selection.split(',')]

        print(f"Selected MFCs: {selected_ids}")
        
        # Create a dictionary to store the flows
        selected_flows = {}

        for id in selected_ids:
            # Ask the user to input the flow for each MFC
            flow = float(input(f"Enter the flow for MFC {id} (max: {max_flows[id]}): "))
            if flow > max_flows[id]:
                print(f"Flow for MFC {id} is too high! Setting it to the maximum value...")
                flow = max_flows[id]
            selected_flows[id] = flow

        print(f"Selected flows: {selected_flows}")

        return selected_flows

        
        
    def run_mode(self):
        if self.mode is not None:
            return self.mode.run()
        else:
            print("No mode selected!")

    def shutdown(self):
        if self.keithleys is not None:
            for keithley in self.keithleys:
                if keithley is not None:
                    keithley.close()

        if self.data_measurement is not None:
            self.data_measurement.close()

        if self.mfc is not None:
            self.mfc.clear_all_flows()
            
        print("All devices closed!")