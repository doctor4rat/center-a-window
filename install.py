import os
import shutil
import sys

def install_script():
    """Installs the window centering script to the startup folder."""

    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py") #Gets the script path relative to this install script

    startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    target_path = os.path.join(startup_folder, "center_window.py") #renames the startup script

    try:
        shutil.copy2(script_path, target_path)
        print(f"Script installed to: {target_path}")
    except Exception as e:
        print(f"Error installing script: {e}")

def uninstall_script():
    """Uninstalls the window centering script from the startup folder."""

    startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    target_path = os.path.join(startup_folder, "center_window.py")

    try:
        os.remove(target_path)
        print(f"Script uninstalled from: {target_path}")
    except FileNotFoundError:
        print("Script not found in startup folder.")
    except Exception as e:
        print(f"Error uninstalling script: {e}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--uninstall":
        uninstall_script()
    else:
        install_script()

if __name__ == "__main__":
    main()
