import subprocess
from text_processor import get_final_text


subprocess.run(["python", "./main_window.py", get_final_text()])
