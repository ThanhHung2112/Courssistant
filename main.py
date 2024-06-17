import subprocess
import os
import platform

def run_rasa():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    rasa_dir = os.path.join(current_dir, "rasa")  

    if platform.system() == "Darwin":  # macOS
        # Command to open a new Terminal tab and run the Rasa server on macOS
        command = f"""
        osascript -e 'tell application "Terminal"
            activate
            do script "cd '{rasa_dir}'; source ~/.bash_profile; conda activate rasa; rasa run --enable-api --cors \\"*\\" --debug"
        end tell'
        """
    elif platform.system() == "Windows":  # Windows
        # Command to open a new Command Prompt window and run the Rasa server on Windows
        command = f"""
        start cmd /k "cd /d "{rasa_dir}"; conda activate rasa; rasa run --enable-api --cors "*" --debug"
        """
    else:
        print("Unsupported operating system")
        return

    subprocess.Popen(command, shell=True)

def run_streamlit():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    rasa_dir = os.path.join(current_dir, "rasa") 

    if platform.system() == "Darwin":  # macOS
        # Command to open a new Terminal tab and run the Streamlit app on macOS
        command = f"""
        osascript -e 'tell application "Terminal"
            activate
            do script "cd '{rasa_dir}'; source ~/.bash_profile; conda activate rasa; streamlit run ui/app.py --server.runOnSave true"
        end tell'
        """
    elif platform.system() == "Windows":  # Windows
        # Command to open a new Command Prompt window and run the Streamlit app on Windows
        command = f"""
        start cmd /k "cd /d "{rasa_dir}"; conda activate rasa; streamlit run ui/app.py --server.runOnSave true"
        """
    else:
        print("Unsupported operating system")
        return

    subprocess.Popen(command, shell=True)

if __name__ == "__main__":
    run_rasa()
    run_streamlit()
