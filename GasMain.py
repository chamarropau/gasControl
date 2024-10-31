# THIS CLASS SHOULD BE CALLED APP.PY OR SOMETHING LIKE THAT BECAUSE IT IS THE ONE WHO
# RUNS THE WHOLE APPLICATION

from controller.Controller import Controller
from view.TerminalView import TerminalView
from PyQt5.QtWidgets import QApplication
from view.App import App
from EnvController import EnvironmentController
import sys

def main():

    controller = None
    controller = Controller()

    # Create the virtual environment
    env_controller = EnvironmentController()
    env_controller.setup()

    try:
        running_mode = int(input("Select the running mode (1: Terminal View, 2: GUI): "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        sys.exit(1)

    try:
        if running_mode == 1:
            terminal = TerminalView(controller)
            terminal.start()

        else:
            app = QApplication(sys.argv)
            window = App(controller)
            window.show()
            sys.exit(app.exec_())

        # When the program ends, close the Keithley devices, set the MFCs to zero, and close the data manager
        controller.shutdown()
        
        # Print a message to the user indicating that the program is closing
        print("Exiting...")
        sys.exit(0)
        
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)



if __name__ == "__main__":
    main()
