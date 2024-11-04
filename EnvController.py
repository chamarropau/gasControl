import os
import subprocess
import sys
import venv
import json
from colorama import Fore, Style
from pkg_resources import get_distribution, parse_version
from termcolor import colored

class EnvironmentController:
    def __init__(self, env_name="SoftwareGasControl"):
        self.env_name = env_name
        self.env_path = os.path.join(os.getcwd(), self.env_name)
        self.dependencies = [
            "bronkhorst_propar", "numpy", "pandas", "pyqtgraph", "pint", "setuptools_scm",
            "propar", "PyQt5", "PyQt5_sip", "pyserial", "PyVISA", "termcolor", "colorama",
            "tqdm", "pymeasure"
        ]

    def upgrade_pip(self):
        print(f"{colored('[INFO]', 'yellow')} UPGRADING PIP...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        os.system("cls" if os.name == "nt" else "clear")

    def upgrade_setuptools(self, pip_path):
        try:
            curr_version = subprocess.check_output([pip_path, 'show', 'setuptools']).decode().split('\n')
            for line in curr_version:
                if 'Version:' in line:
                    curr_version = line.split(' ')[-1]
                    break
            required_version = "61.0.0"
            if parse_version(curr_version) < parse_version(required_version):
                print(f"{colored('[INFO]', 'yellow')} UPGRADING SETUPTOOLS...")
                subprocess.check_call([pip_path, 'install', '--upgrade', 'setuptools'])
        except Exception as e:
            print(f"{colored('[ERROR]', 'red')} ERROR UPGRADING SETUPTOOLS...")

        os.system("cls" if os.name == "nt" else "clear")

    def check_and_install_required_packages(self, pip_path):
        self.upgrade_pip()
        for package in ["tqdm", "colorama", "pkg_resources"]:
            try:
                __import__(package)
            except ImportError:
                print(f"{colored('[INFO]', 'yellow')} INSTALLING {package}...")
                subprocess.check_call([pip_path, 'install', package])

    def create_environment(self):
        if not os.path.exists(self.env_path):
            print(f"{colored('[INFO]', 'yellow')} CREATING VIRTUAL ENVIRONMENT... {self.env_name}...")
            venv.create(self.env_path, with_pip=True)
            print(f"{colored('[STATUS]', 'green')} VIRTUAL ENVIRONMENT CREATED SUCCESSFULLY {self.env_name}...")

        os.system("cls" if os.name == "nt" else "clear")

    def install_dependencies(self):
        print(f"{colored('[INFO]', 'yellow')} INSTALLING DEPENDENCIES... {self.env_name}...")
        print()
        pip_path = os.path.join(self.env_path, 'Scripts', 'pip.exe') if os.name == 'nt' else os.path.join(self.env_path, 'bin', 'pip')
        for dependency in self.dependencies:
            print(f"{colored('[INFO]', 'yellow')} INSTALLING {dependency}...")
            try:
                subprocess.check_call([pip_path, 'install', dependency], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"{colored('[STATUS]', 'green')} {dependency} INSTALLED SUCCESSFULLY.")
                print()
            except subprocess.CalledProcessError:
                print(f"{colored('[ERROR]', 'red')} ERROR INSTALLING {dependency}")

        os.system("cls" if os.name == "nt" else "clear")

    def set_vscode_interpreter(self):
        settings_path = os.path.join(os.getcwd(), '.vscode', 'settings.json')
        if not os.path.exists(settings_path):
            os.makedirs(os.path.dirname(settings_path), exist_ok=True)
            with open(settings_path, 'w') as f:
                f.write('{}')
        with open(settings_path, 'r') as f:
            settings = json.load(f)
        settings["python.pythonPath"] = os.path.join(self.env_path, 'Scripts', 'python.exe') if os.name == 'nt' else os.path.join(self.env_path, 'bin', 'python')
        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=4)

        os.system("cls" if os.name == "nt" else "clear")

    def run_gas_main(self):
        """Run GasMain.py using the Python interpreter from the virtual environment."""
        print(f"{colored('[STATUS]', 'green')} RUNNING THE MAIN APPLICATION...")
        python_executable = os.path.join(self.env_path, 'Scripts', 'python.exe') if os.name == 'nt' else os.path.join(self.env_path, 'bin', 'python')
        gas_main_path = os.path.join(os.getcwd(), 'GasMain.py')
        try:
            subprocess.check_call([python_executable, gas_main_path])
        except subprocess.CalledProcessError as e:
            print(f"{colored('[ERROR]', 'red')} ERROR RUNNING THE MAIN APPLICATION...")

    def setup(self):
        self.create_environment()
        pip_path = os.path.join(self.env_path, 'Scripts', 'pip.exe') if os.name == 'nt' else os.path.join(self.env_path, 'bin', 'pip')
        self.upgrade_setuptools(pip_path)  # Asegúrate de que setuptools se actualice primero
        self.check_and_install_required_packages(pip_path)
        self.install_dependencies()
        self.set_vscode_interpreter()
        self.run_gas_main()
