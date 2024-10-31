import os  # Import the os module for interacting with the operating system
import subprocess  # Import subprocess for executing shell commands
import sys  # Import sys for accessing system-specific parameters and functions
import venv  # Import venv for creating virtual environments
import json  # Import json for reading and writing JSON files
from colorama import Fore, Style  # Import colorama for colored terminal text

class EnvironmentController:
    def __init__(self, env_name="SoftwareGasControl"):
        # Initialize the EnvironmentController with a default environment name
        self.env_name = env_name
        # Define the path for the virtual environment based on the current working directory
        self.env_path = os.path.join(os.getcwd(), self.env_name)
        # List of required dependencies with specific versions
        self.dependencies = [
            "bronkhorst_propar==1.1.1",
            "numpy",
            "pandas",
            "propar==1.0.2",
            "PyMeasure==0.14.0",
            "PyQt5==5.15.11",
            "PyQt5_sip==12.15.0",
            "pyserial==3.5",
            "PyVISA==1.14.1",
            "termcolor",
            "colorama",
            "tqdm"
        ]

    def check_and_install_required_packages(self):
        """Install tqdm and colorama if they are not already installed."""
        for package in ["tqdm", "colorama"]:
            try:
                __import__(package)  # Attempt to import the package
            except ImportError:
                # If the import fails, install the package
                print(f"Installing {package}...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

    def create_environment(self):
        """Create the virtual environment if it does not already exist."""
        if not os.path.exists(self.env_path):
            print(f"Creating virtual environment: {self.env_name}")
            venv.create(self.env_path, with_pip=True)  # Create the virtual environment with pip
            print("Virtual environment created successfully.")

    def install_dependencies(self):
        """Install the required dependencies with a progress bar and custom messages."""
        print("Installing dependencies...")
        # Determine the path to the pip executable based on the operating system
        pip_path = os.path.join(self.env_path, 'Scripts', 'pip.exe') if os.name == 'nt' else os.path.join(self.env_path, 'bin', 'pip')

        for dependency in self.dependencies:
            print(f"Installing {dependency}...")
            # Try to use tqdm only after ensuring it is installed
            try:
                import tqdm  # Attempt to import tqdm for progress indication
            except ImportError:
                # If tqdm is not installed, install it
                print("tqdm is not installed. Installing now...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'tqdm'])
                import tqdm  # Re-import tqdm after installation

            # Use tqdm to display a progress bar
            from tqdm import tqdm  # Ensure tqdm is imported here
            with tqdm(total=100, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]") as pbar:
                try:
                    # Execute the installation of the dependency
                    subprocess.check_call([pip_path, 'install', dependency], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    pbar.update(100)  # Complete the progress bar
                    print()
                    print(f"{Fore.GREEN}{dependency} installed successfully!{Style.RESET_ALL}")  # Print success message in green
                    print()
                except subprocess.CalledProcessError:
                    # Handle installation failure
                    print(f"{Fore.RED}Failed to install {dependency}.{Style.RESET_ALL}")  # Print error message in red
                finally:
                    # Update the progress bar to reflect the final state
                    for _ in range(100):
                        pbar.update(1)  # Complete the progress bar for final state

    def set_vscode_interpreter(self):
        """Set the Python interpreter in VSCode."""
        settings_path = os.path.join(os.getcwd(), '.vscode', 'settings.json')  # Path to VSCode settings file
        if not os.path.exists(settings_path):
            # If the settings file does not exist, create the necessary directories and an empty file
            os.makedirs(os.path.dirname(settings_path), exist_ok=True)
            with open(settings_path, 'w') as f:
                f.write('{}')  # Create an empty JSON object

        # Load existing settings from the file
        with open(settings_path, 'r') as f:
            settings = json.load(f)

        # Add the interpreter path to the configuration
        settings["python.pythonPath"] = os.path.join(self.env_path, 'Scripts', 'python.exe') if os.name == 'nt' else os.path.join(self.env_path, 'bin', 'python')

        # Save the updated settings back to the file
        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=4)  # Write the settings with indentation for readability

    def setup(self):
        """Set up the virtual environment and dependencies."""
        self.create_environment()  # Create the virtual environment
        self.check_and_install_required_packages()  # Ensure required packages are installed
        self.install_dependencies()  # Install all specified dependencies
        self.set_vscode_interpreter()  # Configure VSCode interpreter
        os.system("cls" if os.name == "nt" else "clear")  # Clear the terminal screen
