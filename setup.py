import os
import subprocess
import sys
from pathlib import Path


packages = ["fastapi", "uvicorn", "mysql-connector-python", "python-dotenv", "numpy", "serial",
 "requests", "paho-mqtt", "pydantic", "python-multipart", "python-jose[cryptography]", "passlib","bcrypt","jinja2"]

venv_path = Path("Aegis")

if not venv_path.exists():
    print("Creating virtual environment: Aegis")
    subprocess.run([sys.executable, "-m", "venv", "Aegis"], check=True)

venv_python = venv_path / "bin" / "python" if os.name != "nt" else venv_path / "Scripts" / "python.exe"

print("Installing packages in virtual environment Aegis")
for package in packages:
    print("Installing package: " + package)
    subprocess.run([str(venv_python), "-m", "pip", "install", package], check=True)

print("Done")
print("To activate the virtual environment, run:")
print("source Aegis/bin/activate")
print("To deactivate the virtual environment, run:")
print("deactivate")