from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QCheckBox, QLabel, QPushButton, QFileDialog,
    QVBoxLayout, QHBoxLayout, QSpinBox, QGridLayout, QWidget, QGroupBox,
    QMessageBox, QDoubleSpinBox, QApplication, QLineEdit
)
from view.ElectricalTypeDialog import ElectricalTypeDialog
from PyQt5.QtCore import Qt
import sys

MAX_MEASUREMENT_TIME = 5000
MAX_ADQUISITION_TIME = 5000
MAX_SAVING_TIME = 5000

NO_MODE_SELECTED = "You need to select a mode to run."
NO_FILE_SELECTED = "You need to select an Excel file to run the automatic mode."
NO_EL_TYPE_SELECTED = "You need to select an electrical type to run the manual mode."
NO_DATA_SHEET_SELECTED = "You need to select a data sheet to run the automatic mode."
NO_KEITHLEY_SELECTED = "You need to select at least one Keithley to run the program."

class App(QMainWindow):

    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        self.mfc_labels = ["MFC3", "MFC6", "MFC9", "MFC12", "MFC16", "MFC20"]

        self.selected_file_path = None
        self.configured_type = None

        # Configure the main window
        self.setWindowTitle("Development of the control software for the greenhouse gas analysis platform.")
        self.center()

        # Create the main widget
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # Create the main layout
        self.main_layout = QVBoxLayout()
        self.top_layout = QHBoxLayout()
        self.keithleys_layout = QHBoxLayout()
        self.bottom_layout = QHBoxLayout()

        # Create controller buttons
        self.manual_mode_checkbox = QCheckBox("Enable Manual Mode")
        self.automatic_mode_checkbox = QCheckBox("Enable Automatic Mode")
        self.run_btn = QPushButton("RUN")
        self.one_keithley = QPushButton("One Keithley")
        self.two_keithley = QPushButton("Two Keithley")
        self.el_type_btn = QPushButton("Electrical Type")

        # ----------------------------- Display Area -----------------------------
        self.set_graphic()
        self.set_manual_mode()
        self.set_automatic_mode()
        self.keithleys_layout.addWidget(self.one_keithley)
        self.keithleys_layout.addWidget(self.two_keithley)

        # ----------------------------- Set up signals -----------------------------
        self.manual_mode_checkbox.stateChanged.connect(self.toggle_automatic_mode)
        self.automatic_mode_checkbox.stateChanged.connect(self.toggle_manual_mode)
        self.one_keithley.clicked.connect(self.toggle_one_keithley)
        self.two_keithley.clicked.connect(self.toggle_two_keithley)
        self.run_btn.clicked.connect(self.start)

        # ----------------------------- Set the main layout -----------------------------
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.bottom_layout)
        self.main_layout.addLayout(self.keithleys_layout)
        self.main_layout.addWidget(self.run_btn)

        self.main_widget.setLayout(self.main_layout)

    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    #------------------------------------- CENTER THE WINDOW --------------------------------------------#
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    
    def center(self):
        width = 1000
        height = 800

        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()

        x = (screen_rect.width() - width) // 2
        y = (screen_rect.height() - height) // 2

        self.setGeometry(x, y, width, height)

    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    #------------------------------------------- SETTERS ------------------------------------------------#
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################

    def set_graphic(self):
        self.image_label = QLabel("Display Area")
        self.image_label.setFixedSize(600, 350)
        self.image_label.setStyleSheet("border: 2px solid purple;")
        self.top_layout.addWidget(self.image_label)

    def set_manual_mode(self):
        self.manual_mode_group = QGroupBox("Manual Mode")
        manual_layout = QGridLayout()
        manual_layout.addWidget(self.manual_mode_checkbox, 0, 0, 1, 2)
        
        self.measurement_time = QDoubleSpinBox()
        self.adquisition_time = QDoubleSpinBox()
        self.saving_time = QDoubleSpinBox()
        self.measurement_time.setRange(0, MAX_MEASUREMENT_TIME)
        self.adquisition_time.setRange(0, MAX_ADQUISITION_TIME)
        self.saving_time.setRange(0, MAX_SAVING_TIME)
        self.measurement_time.setSuffix(" min")
        self.adquisition_time.setSuffix(" min")
        self.saving_time.setSuffix(" min")
        self.measurement_time.setEnabled(False)
        self.adquisition_time.setEnabled(False)
        self.saving_time.setEnabled(False)

        # Ask for the time of the measurement, adquisition and saving
        manual_layout.addWidget(QLabel("Measurement Time"), 1, 0, 1, 1)
        manual_layout.addWidget(self.measurement_time, 1, 2, 1, 2)
        manual_layout.addWidget(QLabel("Adquisition Time"), 2, 0, 1, 1)
        manual_layout.addWidget(self.adquisition_time, 2, 2, 1, 2)
        manual_layout.addWidget(QLabel("Saving Time"), 3, 0, 1, 1)
        manual_layout.addWidget(self.saving_time, 3, 2, 1, 2)

        self.mfc_checkboxes = {}
        self.mfc_spinboxes = {}

        # Insert MFC and SpinBoxes 
        for i, label in enumerate(self.mfc_labels):
            mfc_checkbox = QCheckBox(label)
            mfc_spinbox = QSpinBox()
            mfc_spinbox.setRange(0, 20 if i == 5 else 200)
            mfc_spinbox.setEnabled(False)
            mfc_checkbox.setEnabled(False)
            self.mfc_checkboxes[label] = mfc_checkbox
            self.mfc_spinboxes[label] = mfc_spinbox

            row = 4 + (i // 2)
            column = (i % 2) * 2

            # Add checkbox and spinbox to the layout
            manual_layout.addWidget(mfc_checkbox, row, column)
            manual_layout.addWidget(mfc_spinbox, row, column + 1)  

            # Connect the checkbox state with the corresponding spinbox
            mfc_checkbox.stateChanged.connect(lambda state, key=label: self.toggle_spinbox(key, state))

        self.el_type_btn.setEnabled(False)
        self.el_type_btn.clicked.connect(self.toggle_electrical_type)

        manual_layout.addWidget(self.el_type_btn, 10, 1, 1, 2)

        # Set the layout of the manual mode group
        self.manual_mode_group.setLayout(manual_layout)
        self.bottom_layout.addWidget(self.manual_mode_group)

    def set_automatic_mode(self):
        self.automatic_mode_group = QGroupBox("Automatic Mode")

        # Layout principal para centrar vertical y horizontalmente
        vbox_layout = QVBoxLayout()

        # Añadimos la casilla de verificación en la parte superior (arriba del todo)
        vbox_layout.addWidget(self.automatic_mode_checkbox, alignment=Qt.AlignLeft)

        # Espaciador flexible para empujar el resto del contenido hacia el centro vertical
        vbox_layout.addStretch(1)

        # Creamos un layout de cuadrícula para los widgets
        automatic_layout = QGridLayout()

        # Botón Import Excel en la fila 0, centrado horizontalmente
        self.import_excel_button = QPushButton("Import Excel")
        self.import_excel_button.setEnabled(False)
        self.import_excel_button.setFixedSize(100, 50)
        self.import_excel_button.setCursor(Qt.PointingHandCursor)
        self.import_excel_button.clicked.connect(self.import_excel)

        # Añadimos el botón Import Excel centrado horizontalmente
        automatic_layout.addWidget(self.import_excel_button, 0, 0, 1, 2, alignment=Qt.AlignCenter)

        # Añadimos un QLabel y QLineEdit en la misma fila, centrados horizontalmente
        self.sheet_name_label = QLabel("Sheet Name:")
        self.sheet_name_input = QLineEdit()
        self.sheet_name_input.setPlaceholderText("Enter sheet name")

        # Añadimos ambos widgets en la fila 1
        automatic_layout.addWidget(self.sheet_name_label, 1, 0, alignment=Qt.AlignRight)
        automatic_layout.addWidget(self.sheet_name_input, 1, 1, alignment=Qt.AlignLeft)

        # Añadimos el layout de cuadrícula al layout vertical
        vbox_layout.addLayout(automatic_layout)

        # Espaciador flexible en la parte inferior para empujar el contenido hacia arriba
        vbox_layout.addStretch(1)

        # Establecemos el layout del grupo y añadimos el layout vertical
        self.automatic_mode_group.setLayout(vbox_layout)
        self.bottom_layout.addWidget(self.automatic_mode_group)

    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    #-------------------------------------- TOGGLE FUNCTIONS --------------------------------------------#
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################

    def toggle_manual_mode(self, state):
        if state == Qt.Checked:
            self.manual_mode_checkbox.setChecked(False)
            self.toggle_import_excel(True)
            self.toggle_time_spinboxes(False)
            self.toggle_mfcs(False)
            self.toggle_el_type(False)

        if not self.automatic_mode_checkbox.isChecked() and not self.manual_mode_checkbox.isChecked():
            self.toggle_time_spinboxes(False)
            self.toggle_mfcs(False)
            self.toggle_el_type(False)
            self.toggle_import_excel(False)

    def toggle_time_spinboxes(self, state):
        self.measurement_time.setEnabled(state)
        self.adquisition_time.setEnabled(state)
        self.saving_time.setEnabled(state)

    def toggle_spinbox(self, label, state):
        self.mfc_spinboxes[label].setEnabled(state == Qt.Checked)
    
    def toggle_mfcs(self, state):
        for i, label in enumerate(self.mfc_labels):
            self.mfc_checkboxes[label].setEnabled(state)

    def toggle_electrical_type(self):
        dialog = ElectricalTypeDialog(self)
        dialog.exec_()
        self.configured_type = dialog.configured_el_type

    def toggle_el_type(self, state):
        self.el_type_btn.setEnabled(state)
            
    def toggle_automatic_mode(self, state):
        if state == Qt.Checked:
            self.automatic_mode_checkbox.setChecked(False)
            self.toggle_import_excel(False)
            self.toggle_time_spinboxes(True)
            self.toggle_mfcs(True)
            self.toggle_el_type(True)
        
        if not self.manual_mode_checkbox.isChecked() and not self.automatic_mode_checkbox.isChecked():
            self.toggle_time_spinboxes(False)
            self.toggle_mfcs(False)
            self.toggle_el_type(False)
            self.toggle_import_excel(False)

    def toggle_import_excel(self, state):
        self.import_excel_button.setEnabled(state)
        self.sheet_name_input.setEnabled(state)

    def toggle_one_keithley(self):
        self.one_keithley.setEnabled(False)
        self.two_keithley.setEnabled(True)

    def toggle_two_keithley(self):
        self.one_keithley.setEnabled(True)
        self.two_keithley.setEnabled(False)

    def import_excel(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Import Excel File", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        
        if file_name:
            self.selected_file_path = file_name

    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    #------------------------------------------ WARNINGS ------------------------------------------------#
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################

    def show_warning(self, message):
        warning_box = QMessageBox()
        warning_box.setWindowTitle("Warning")
        warning_box.setText(message)
        warning_box.setIcon(QMessageBox.Warning)
        warning_box.setStandardButtons(QMessageBox.Ok)
        warning_box.exec_()

    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    #------------------------------------------- GETTERS ------------------------------------------------#
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################

    # self.configured_el_type = {
    #         "electrical_type": selected_type,
    #         "voltage": voltage_value or None,
    #         "final_voltage": final_voltage_value or None,
    #         "current": current_value or None,
    #         "final_current": final_current_value or None,
    #         "unit": unit_value or None,
    #         "n_points": n_points_value or None
    #     }

    def get_manual_values(self):
        dict_config = {}
        dict_selected_type = {}

        measurement_time = self.measurement_time.value() * 60
        adquisition_time = self.adquisition_time.value() * 60
        saving_time = self.saving_time.value() * 60
        mfc_values = {label: self.mfc_spinboxes[label].value() for label, checkbox in self.mfc_checkboxes.items() if checkbox.isChecked()}

        dict_config["measurement_time"] = measurement_time
        dict_config["adquisition_time"] = adquisition_time
        dict_config["saving_time"] = saving_time

        if self.configured_type is None:
            self.show_warning(NO_EL_TYPE_SELECTED)

        else:
            selected_type = self.configured_type.get("electrical_type", None)   
            voltage_value = self.configured_type.get("voltage", None)
            final_voltage_value = self.configured_type.get("final_voltage", None)
            current_value = self.configured_type.get("current", None)
            final_current_value = self.configured_type.get("final_current", None)
            unit_value = self.configured_type.get("unit", None)
            n_points_value = self.configured_type.get("n_points", None)
            dict_selected_type["selected_type"] = selected_type
            dict_selected_type["voltage_value"] = voltage_value
            dict_selected_type["final_voltage_value"] = final_voltage_value
            dict_selected_type["current_value"] = current_value
            dict_selected_type["final_current_value"] = final_current_value
            dict_selected_type["unit_value"] = unit_value
            dict_selected_type["n_points_value"] = n_points_value

            return dict_config, mfc_values, dict_selected_type



    def get_automatic_values(self):
        if self.selected_file_path is None:
            self.show_warning(NO_FILE_SELECTED)

        elif self.sheet_name_input.text() == "":
            self.show_warning(NO_DATA_SHEET_SELECTED)

        else:
            # Return the selected file path
            data = {}
            data["selected_file_path"] = self.selected_file_path
            data["sheet_name"] = self.sheet_name_input.text()
            return data
        

    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    #------------------------------ FUNCTIONS FOR THE MAIN PROGRAM --------------------------------------#
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    def map_selected_type(self, selected_type):
        self.input_mapping = {
            "ManualIV": 1,
            "ManualVI": 2,
            "AutomaticIV": 3,
            "AutomaticVI": 4,
            "AutomaticIT": 5,
            "AutomaticVT": 6,
        }
        return self.input_mapping[selected_type]
        
    def set_measurement_manual_mode(self, type, measurement_time):
        # Obatin the selected type
        selected_type = type["selected_type"]
        voltage_value = type["voltage_value"]
        final_voltage_value = type["final_voltage_value"]
        current_value = type["current_value"]
        final_current_value = type["final_current_value"]
        unit_value = type["unit_value"]
        n_points_value = type["n_points_value"]

        # Map the selected type
        mapped_type = self.map_selected_type(selected_type)
        print(mapped_type)

        if mapped_type == 1: # ManualIV
            self.controller.set_manual_IV(voltage_value, unit_value, measurement_time)

        elif mapped_type == 2: # ManualVI
            self.controller.set_manual_VI(current_value, unit_value, measurement_time)

        elif mapped_type == 3: # AutomaticIV
            self.controller.set_automatic_IV(voltage_value, final_voltage_value, unit_value, n_points_value, measurement_time)

        elif mapped_type == 4: # AutomaticVI
            self.controller.set_automatic_VI(current_value, final_current_value, unit_value, n_points_value, measurement_time)

        elif mapped_type == 5: # AutomaticIT
            self.controller.set_automatic_IT(voltage_value, unit_value, measurement_time)

        elif mapped_type == 6: # AutomaticVT
            self.controller.set_automatic_VT(current_value, unit_value, measurement_time)


    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    #-------------------------------------- RUN THE PROGRAM ---------------------------------------------#
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################

    def start(self):

        if not self.one_keithley.isEnabled() and not self.two_keithley.isEnabled():
            self.show_warning(NO_KEITHLEY_SELECTED)

        else:

            if self.manual_mode_checkbox.isChecked() and self.configured_type is not None:
                config, mfcs, type = self.get_manual_values()
                print(config, mfcs, type)

                self.controller.set_mode("manual", flows=mfcs)

                # Obtain the measurement time, adquisition time and saving time
                measurement_time = config["measurement_time"]
                ad_time = config["adquisition_time"]
                sv_time = config["saving_time"]

                # Set the electrical type selected
                self.set_measurement_manual_mode(type, measurement_time)

                # Set the data manager
                self.controller.set_data_manager(measurement_time, ad_time, sv_time)

                # Run the mode
                self.controller.run_mode()

            elif self.automatic_mode_checkbox.isChecked():
                excel = self.get_automatic_values()
                print(excel["selected_file_path"], excel["sheet_name"])
                file = excel['selected_file_path']
                sheet = excel['sheet_name']
                if not self.one_keithley.isEnabled():
                    self.controller.set_mode("automatic", num_keithley=1, excel=file, sheet=sheet)
                else:
                    self.controller.set_mode("automatic", num_keithley=2, excel=file, sheet=sheet)

                self.controller.run_mode()

            else:
                self.show_warning(NO_MODE_SELECTED)

