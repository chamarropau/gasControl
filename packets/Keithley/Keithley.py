from pymeasure.instruments.keithley import Keithley2450
from packets.Keithley.EthernetConnection import EthernetConnection
from termcolor import colored
import pyvisa as vs
import time

class Keithley:
    """
    Class to control the Keithley 2450 device using pymeasure.
    """
    def __init__(self, keithley_config):  # keithley_config = {'ip', 'interface', 'mask', 'gateway'}
        # Set up the Ethernet connection
        EthernetConnection().ip_static_configuration(keithley_config['interface'], \
                                                        keithley_config['ip'], \
                                                        keithley_config['mask'], \
                                                        keithley_config['gateway'])
        self.addr = f"TCPIP0::{keithley_config['ip']}::inst0::INSTR"
        
        while True:
            try:
                self.__device_configuration()  # Initialize the Keithley 2450 using pymeasure
                break
            except Exception as e:
                print(e.__str__())
                print(f"{colored('[INFO]', 'blue')} Trying to connect again in 5 seconds...")
                time.sleep(5)

        self.mode = None

    def __device_configuration(self):
        try: 
            self.keithley = Keithley2450(self.addr, timeout=20000)  # Initialize the Keithley 2450 using pymeasure
            
            if self.keithley is None:
                raise Exception(f"{colored('[ERROR]', 'red')} Could not find the Keithley device. Please check the connection.")
            
            #self.keithley.beep(880, 0.5)  # A short beep at 880 Hz (A5 note) for 0.5 seconds
            #self.keithley.beep(660, 0.3)  # Another beep at 660 Hz (E5 note) for 0.3 seconds

            # self.keithley.beep(261, 0.5)  # C4
            # self.keithley.beep(261, 0.5)  # C4
            # self.keithley.beep(392, 0.5)  # G4
            # self.keithley.beep(392, 0.5)  # G4
            # self.keithley.beep(440, 0.5)  # A4
            # self.keithley.beep(440, 0.5)  # A4
            # self.keithley.beep(392, 1.0)  # G4 (hold longer)

            
            self.keithley.reset()  # Reset the instrument
        except vs.VisaIOError as e:
            raise Exception(f"{colored('[ERROR]', 'red')} Could not find the Keithley device. Please check the connection.")


    def reset_measurement(self):
        self.keithley.reset()  # Reset the instrument
        self.keithley.disable_source()  # Disable the source (equivalent to smu.source.output = smu.OFF)

    def close(self):
        self.keithley.shutdown()  # Shut down the instrument

    ##################################  V(I) METHODS  #########################################

    def __init_current_mode(self):  # Apply current and measure voltage
        self.reset_measurement()
        self.keithley.apply_current()  # Set the Keithley to source current mode
        self.keithley.source_current_range = 10e-3  # Set current range (e.g., 10 mA)
        self.keithley.compliance_voltage = 21  # Set voltage compliance to 21 V
        self.keithley.enable_source()  # Enable the source

    def set_current(self, current, time_delay=0.1, unit="mA"):  # Unit: mA, uA, or nA
        if self.mode != "current":
            self.__init_current_mode()
            self.mode = "current"

        # Convert current based on the specified unit
        if unit == "mA":
            current = current * 1e-3
        elif unit == "uA":
            current = current * 1e-6
        elif unit == "nA":
            current = current * 1e-9
        else:
            raise Exception("Invalid unit. Please use mA, uA, or nA.")

        time.sleep(float(time_delay))  # Wait for the source to stabilize

        self.keithley.ramp_to_current(current) 
        self.keithley.measure_voltage()

        # Measure voltage across the DUT (Device Under Test)
        return self.keithley.voltage

    def get_voltage(self):
        return self.keithley.voltage  # Return the last measured voltage

    ##################################  I(V) METHODS  #########################################

    def __init_voltage_mode(self):  # Apply voltage and measure current
        self.reset_measurement()
        self.keithley.apply_voltage()  # Set the Keithley to source voltage mode
        self.keithley.source_voltage_range = 10  # Set voltage range (10 V in this example)
        # self.keithley.compliance_current = 21e-3  # Set current compliance to 21 mA
        self.keithley.enable_source()  # Enable the source

    def set_voltage(self, voltage, time_delay=0.1, unit="V"):  # Unit: V, mV, uV
        if self.mode != "voltage":
            self.__init_voltage_mode()
            self.mode = "voltage"

        # Convert voltage based on the specified unit
        if unit == "mV":
            voltage = voltage * 1e-3
        elif unit == "uV":
            voltage = voltage * 1e-6
        elif unit == "V":
            voltage = voltage
        else:
            raise Exception("Invalid unit. Please use V, mV, or uV.")

        time.sleep(float(time_delay))  # Wait for the source to stabilize

        self.keithley.ramp_to_voltage(voltage)
        self.keithley.measure_current()

        # Measure current across the DUT 
        return self.keithley.current

    def get_current(self):
        return self.keithley.current  # Return the last measured current
