import subprocess


def run_the_video(file_path):
    try:
        subprocess.Popen(["xdg-open", str(file_path)])
    except Exception as e:
        print("Could not open the file.", e)
