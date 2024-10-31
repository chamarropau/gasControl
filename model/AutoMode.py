from packets.ExcelController.ExcelController import ExcelController
from packets.ExcelController.OutputExcel import OutputExcel
from model.ElectricalMeasurementsTypes.AutomaticIV import AutomaticIV
from model.ElectricalMeasurementsTypes.AutomaticVI import AutomaticVI
from model.ElectricalMeasurementsTypes.AutomaticIT import AutomaticIT
from model.ElectricalMeasurementsTypes.AutomaticVT import AutomaticVT
from model.DataManager import DataManager
from threading import Thread, Barrier, Event
from termcolor import colored
import pandas as pd
import time
import re

class AutoMode:
    def __init__(self, num_keithleys, keithleys, mfc, data_measurement, excel_path, excel_sheet):
        self.num_keithleys = num_keithleys
        self.keithleys = keithleys
        self.mfc = mfc
        self.data_measurement = data_measurement
        self.electrical_measurement = None
        self.excel_path = excel_path
        self.excel_sheet = excel_sheet
        # Configura la barrera según el número de Keithleys y el hilo principal
        self.barrier = Barrier(num_keithleys + 1)
        self.stop_event = Event()
        self.threads = []  # Lista para los hilos
        self.data = []

    def run(self):
        print(f"\n\n{colored('[STATUS]', 'green')} STARTING AUTOMATIC MODE...\n\n")
        excel_controller = ExcelController()
        config, measurements = excel_controller.read_excel(self.excel_path, self.excel_sheet)

        for i, measurement in enumerate(measurements):
            print(f"\n\n{colored('[STATUS]', 'green')} STARTING MEASUREMENT {i+1}...\n\n")
            smu_1_mode = measurement.get_smu_mode("SMU1")
            smu_1_value = measurement.get_smu_value("SMU1")
            smu_1_unit = measurement.get_smu_unit("SMU1")
            sv_time = measurement.get_sv_time()
            ad_time = measurement.get_ad_time()
            measurement_time = measurement.get_measurement_time()
            mfcs_flows = measurement.get_mfcs_flows()

            # Configuración de flujos de MFC
            for mfc_name, mfc_flow in mfcs_flows.items():
                mfc_id = config.get_mfc_id(mfc_name)
                max_flow = config.get_mfc_max_flow(mfc_name)
                self.mfc.set_flow(mfc_id, mfc_flow, max_flow)
            
            # Configuración de la medición eléctrica para cada Keithley
            electrical_measurement_1 = self.__get_electrical_measurement(smu_1_mode, smu_1_value, smu_1_unit, measurement_time, 0)
            
            # Condicional según el número de Keithleys
            if self.num_keithleys == 2:
                smu_2_mode = measurement.get_smu_mode("SMU2")
                smu_2_value = measurement.get_smu_value("SMU2")
                smu_2_unit = measurement.get_smu_unit("SMU2")
                electrical_measurement_2 = self.__get_electrical_measurement(smu_2_mode, smu_2_value, smu_2_unit, measurement_time, 1)
                electrical_measurements = [electrical_measurement_1, electrical_measurement_2]
            else:
                electrical_measurements = [electrical_measurement_1]

            data_manager = DataManager(self.mfc, electrical_measurements, self.data_measurement, measurement_time, ad_time, sv_time)
            
            try:
                # Creación de hilos según el número de Keithleys
                self.threads.append(Thread(target=electrical_measurement_1.run, args=(self.barrier, self.stop_event)))
                self.threads[-1].start()
                
                if self.num_keithleys == 2:
                    self.threads.append(Thread(target=electrical_measurement_2.run, args=(self.barrier, self.stop_event)))
                    self.threads[-1].start()

                # Hilo principal para el manejo de datos
                data = data_manager.run(self.barrier)
                self.data.append(data)
                
            except KeyboardInterrupt:
                self.saving_data()
                print(f"\n\n{colored('[ERROR]', 'red')} Measurement {i+1} was interrupted by the user\n\n")
                self.stop_event.set()
                print(f"\n\n{colored('[STATUS]', 'green')} Keithleys and threads stopped correctly\n\n")

            except Exception as e:
                self.saving_data()
                print(f"\n\n{colored('[ERROR]', 'red')} Error in measurement {i+1}: {e}\n\n")
                self.stop_event.set()
                print(f"\n\n{colored('[STATUS]', 'green')} Keithleys and threads stopped correctly\n\n")

            time.sleep(3)

        self.saving_data()
                
        def __get_electrical_measurement(self, smu_mode, smu_value, smu_unit, measurement_time, smu_id):
            electrical_mesurement = None
            if "/" in smu_value: # AutomaticVI or AutomaticIV
                pattern = r"(\d+)-(\d+)/(\d+)" # pattern = r"([0-9]*\.?[0-9]+)-([0-9]*\.?[0-9]+)/([0-9]+)"
                match = re.match(pattern, smu_value)
                initial_value = float(match.group(1))
                final_value = float(match.group(2))
                step = int(match.group(3))

                if smu_mode == "current": # AutomaticVI
                    electrical_mesurement =  AutomaticVI(self.keithleys[smu_id], \
                                    initial_value, final_value, smu_unit, step, measurement_time)
                else: # AutomaticIV
                    electrical_mesurement =  AutomaticIV(self.keithleys[smu_id], \
                                    initial_value, final_value, smu_unit, step, measurement_time)
                    
            else: # AutomaticVT or AutomaticIT
                smu_value = float(smu_value)
                if smu_mode == "current":
                    # AutomaticVT
                    electrical_mesurement =  AutomaticVT(self.keithleys[smu_id], \
                                    smu_value, smu_unit, measurement_time)
                else:
                    # AutomaticIT
                    electrical_mesurement = AutomaticIT(self.keithleys[smu_id], \
                                    smu_value, smu_unit, measurement_time)

            return electrical_mesurement
        

        def saving_data(self):
            if self.thread_1.is_alive():
                self.thread_1.join()
            if self.thread_2.is_alive():
                self.thread_2.join()

            name = f"Measure_{time.strftime('%Y%m%d-%H%M%S')}.xlsx"
            output = OutputExcel(f"./data/{name}", self.data)
            output.save_excel()