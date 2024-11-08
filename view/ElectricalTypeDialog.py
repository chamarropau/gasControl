from PyQt5.QtWidgets import (
    QDialog, QApplication, QVBoxLayout, QGridLayout, QLabel, QPushButton, 
    QGroupBox, QRadioButton, QButtonGroup, QDoubleSpinBox, QSpinBox, QComboBox
)

class ElectricalTypeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.el_types = ["ManualIV", "ManualVI", "AutomaticIV", "AutomaticVI", "AutomaticIT", "AutomaticVT",]
        self.configured_el_type = {}

        self.setWindowTitle("Configure an Electrical Type")
        self.setFixedSize(500, 500)
        
        self.initUI()
        self.center()

    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    #--------------------------------------- INIT FUNCTIONS ---------------------------------------------#
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################

    def initUI(self):
        layout = QVBoxLayout()

        # Group box para los radio buttons
        self.group_box = QGroupBox("Configure an Electrical Type")
        grid_layout = QGridLayout()

        # Añadiendo los QRadioButton
        self.radio_buttons = {}
        self.button_group = QButtonGroup(self)  

        for idx, label in enumerate(self.el_types):
            radio_button = QRadioButton(label)
            self.radio_buttons[label] = radio_button
            self.button_group.addButton(radio_button)  
            row = idx // 2
            col = idx % 2
            grid_layout.addWidget(radio_button, row, col)

            radio_button.toggled.connect(self.on_radio_button_toggled)

        self.group_box.setLayout(grid_layout)
        layout.addWidget(self.group_box)

        # Create the spinboxes and labels
        self.voltage_spinbox = QDoubleSpinBox()
        self.final_voltage_spinbox = QDoubleSpinBox()
        self.current_spinbox = QDoubleSpinBox()
        self.final_current_spinbox = QDoubleSpinBox()
        self.n_points_spinbox = QSpinBox()

        self.unit_spinbox = QComboBox()
        self.unit_spinbox.addItems(["mA", "uA", "nA", "mV", "uV", "V"])

        self.voltage_label = QLabel("Voltage")
        self.final_voltage_label = QLabel("Final Voltage")
        self.current_label = QLabel("Current")
        self.final_current_label = QLabel("Final Current")
        self.n_points_label = QLabel("Number of Points")
        self.unit_label = QLabel("Unit")

        # Add the spinboxes and labels to the layout
        layout.addWidget(self.voltage_label)
        layout.addWidget(self.voltage_spinbox)
        layout.addWidget(self.final_voltage_label)
        layout.addWidget(self.final_voltage_spinbox)
        layout.addWidget(self.current_label)
        layout.addWidget(self.current_spinbox)
        layout.addWidget(self.final_current_label)
        layout.addWidget(self.final_current_spinbox)
        layout.addWidget(self.unit_label)
        layout.addWidget(self.unit_spinbox)
        layout.addWidget(self.n_points_label)
        layout.addWidget(self.n_points_spinbox)

        # Hide all spinboxes and labels until a radio button is selected
        self.hide_all_spinboxes()

        # Botón "CONFIGURE"
        self.configure_button = QPushButton("CONFIGURE")
        self.configure_button.clicked.connect(self.on_configure_clicked)
        layout.addWidget(self.configure_button)

        self.setLayout(layout)

    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    #-------------------------------------- TOGGLE FUNCTIONS --------------------------------------------#
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################

    def on_radio_button_toggled(self):
        selected_button = self.button_group.checkedButton()
        if selected_button:
            selected_type = selected_button.text()
            self.update_spinboxes(selected_type)

    def update_spinboxes(self, selected_type):
        # Ocultar todos los spinboxes primero
        self.hide_all_spinboxes()

        # Mostrar los spinboxes adecuados según la opción seleccionada
        if selected_type == "ManualIV":
            self.voltage_label.setText("Voltage")
            self.voltage_label.show()
            self.voltage_spinbox.show()
            self.unit_label.setText("Voltage Unit")
            self.unit_spinbox.clear()
            self.unit_spinbox.addItems(["mV", "uV", "V"])
            self.unit_label.show()
            self.unit_spinbox.show()

        elif selected_type == "ManualVI":
            self.current_label.setText("Current")
            self.current_label.show()
            self.current_spinbox.show()
            self.unit_label.setText("Current Unit")
            self.unit_spinbox.clear()
            self.unit_spinbox.addItems(["mA", "uA", "nA"])
            self.unit_label.show()
            self.unit_spinbox.show()

        elif selected_type == "AutomaticIV":
            self.voltage_label.setText("Initial Voltage")
            self.voltage_label.show()
            self.voltage_spinbox.show()
            self.final_voltage_label.setText("Final Voltage")
            self.final_voltage_label.show()
            self.final_voltage_spinbox.show()
            self.unit_label.setText("Voltage Unit")
            self.unit_spinbox.clear()
            self.unit_spinbox.addItems(["mV", "uV", "V"])
            self.unit_label.show()
            self.unit_spinbox.show()
            self.n_points_label.show()
            self.n_points_spinbox.show()

        elif selected_type == "AutomaticVI":
            self.current_label.setText("Initial Current")
            self.current_label.show()
            self.current_spinbox.show()
            self.final_current_label.setText("Final Current")
            self.final_current_label.show()
            self.final_current_spinbox.show()
            self.unit_label.setText("Current Unit")
            self.unit_spinbox.clear()
            self.unit_spinbox.addItems(["mA", "uA", "nA"])
            self.unit_label.show()
            self.unit_spinbox.show()
            self.n_points_label.show()
            self.n_points_spinbox.show()

        elif selected_type == "AutomaticIT":
            self.voltage_label.setText("Voltage")
            self.voltage_label.show()
            self.voltage_spinbox.show()
            self.unit_label.setText("Voltage Unit")
            self.unit_spinbox.clear()
            self.unit_spinbox.addItems(["mV", "uV", "V"])
            self.unit_label.show()
            self.unit_spinbox.show()

        elif selected_type == "AutomaticVT":
            self.current_label.setText("Current")
            self.current_label.show()
            self.current_spinbox.show()
            self.unit_label.setText("Current Unit")
            self.unit_spinbox.clear()
            self.unit_spinbox.addItems(["mA", "uA", "nA"])
            self.unit_label.show()
            self.unit_spinbox.show()

    def hide_all_spinboxes(self):
        # Ocultar todas las etiquetas y spinboxes
        self.voltage_label.hide()
        self.voltage_spinbox.hide()
        self.final_voltage_label.hide()
        self.final_voltage_spinbox.hide()
        self.current_label.hide()
        self.current_spinbox.hide()
        self.final_current_label.hide()
        self.final_current_spinbox.hide()
        self.unit_label.hide()
        self.unit_spinbox.hide()
        self.n_points_label.hide()
        self.n_points_spinbox.hide()

    def on_configure_clicked(self):
        selected_button = self.button_group.checkedButton()
        if selected_button:
            selected_type = selected_button.text()
        else:
            selected_type = None
        
        voltage_value = self.voltage_spinbox.value()
        final_voltage_value = self.final_voltage_spinbox.value()
        current_value = self.current_spinbox.value()
        final_current_value = self.final_current_spinbox.value()
        unit_value = self.unit_spinbox.currentText()
        n_points_value = self.n_points_spinbox.value()

        # Create a dictionary asigned to configured_el_type with the non-empty values
        self.configured_el_type = {
            "electrical_type": selected_type,
            "voltage": voltage_value or None,
            "final_voltage": final_voltage_value or None,
            "current": current_value or None,
            "final_current": final_current_value or None,
            "unit": unit_value or None,
            "n_points": n_points_value or None
        }

        # Remove the None values from the dictionary
        self.configured_el_type = {k: v for k, v in self.configured_el_type.items() if v is not None}

        # Then close the dialog
        self.close()

    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    #---------------------------------------- CENTER DIALOG ---------------------------------------------#
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################

    def center(self):
        width = 500
        height = 500

        # Obtener la resolución de la pantalla
        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()

        # Calcular las posiciones X e Y para centrar la ventana
        x = (screen_rect.width() - width) // 2
        y = (screen_rect.height() - height) // 2

        # Establecer la geometría de la ventana centrada
        self.setGeometry(x, y, width, height)