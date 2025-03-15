import os
import shutil
import sys

def install_script():
    """Installs the window centering script to the startup folder."""
    try:
        # Source path of the script
        source_path = r"C:\Users\adar\OneDrive\Documents\centerawindow\main.py"

        # Destination path in the startup folder
        appdata = os.getenv("APPDATA")
        if not appdata:
            print("Error: Could not find APPDATA environment variable.")
            return

        startup_folder = os.path.join(appdata, r"Microsoft\Windows\Start Menu\Programs\Startup")
        destination_path = os.path.join(startup_folder, "main.py")

        # Copy the script to the startup folder
        shutil.copy2(source_path, destination_path)

        # Create a .vbs script to run the python script in background.
        vbs_path = os.path.join(startup_folder, "centerawindow.vbs")
        with open(vbs_path, "w") as vbs_file:
            vbs_file.write(f'CreateObject("Wscript.Shell").Run "pythonw \\"{destination_path}\\"", 0, True')

        print(f"Script installed successfully to startup. It will run on login.")
    except FileNotFoundError:
        print("Error: Script not found at the specified source path.")
    except PermissionError:
        print("Error: Permission denied. Run the installer as administrator.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    install_script()
    input("Press Enter to exit...") #keeps the console open until user presses enter.
