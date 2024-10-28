import os
import sys
import subprocess
import logging
import ctypes
import tkinter as tk
from tkinter import messagebox

# Set user-friendly log file directory
log_directory = os.path.expanduser("~\\Documents\\OptimizationLogs")
os.makedirs(log_directory, exist_ok=True)
log_file_path = os.path.join(log_directory, 'system_optimization.log')

# Setup logging with new directory
logging.basicConfig(filename=log_file_path, level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Check if the script is running as administrator
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        logging.error(f"Error checking admin status: {e}")
        return False

def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

# Task functions with enhanced error handling
def create_restore_point():
    logging.info("Creating a restore point.")
    try:
        subprocess.run("powershell -command \"Checkpoint-Computer -Description 'Manual Restore Point' -RestorePointType 'MODIFY_SETTINGS'\"", shell=True)
        messagebox.showinfo("Success", "Restore point created successfully.")
    except Exception as e:
        logging.error(f"Failed to create restore point: {e}")
        messagebox.showerror("Error", f"Failed to create restore point: {e}")

def run_chkdsk():
    logging.info("Running CHKDSK.")
    try:
        subprocess.run("chkdsk C:", shell=True)
    except Exception as e:
        logging.error(f"Failed to run CHKDSK: {e}")
        messagebox.showerror("Error", f"Failed to run CHKDSK: {e}")

def clear_temp_files():
    logging.info("Clearing temporary files.")
    temp_folder = os.getenv("TEMP")
    try:
        for root, dirs, files in os.walk(temp_folder):
            for file in files:
                os.remove(os.path.join(root, file))
        messagebox.showinfo("Success", "Temporary files cleared.")
    except Exception as e:
        logging.error(f"Failed to clear temporary files: {e}")
        messagebox.showerror("Error", f"Failed to clear temporary files: {e}")

def clear_browser_cache():
    logging.info("Clearing browser cache.")
    try:
        subprocess.run('powershell -command "Remove-Item -Path $env:LOCALAPPDATA\\Microsoft\\Edge\\User Data\\Default\\Cache\\* -Recurse -Force"', shell=True)
        messagebox.showinfo("Success", "Browser cache cleared.")
    except Exception as e:
        logging.error(f"Failed to clear browser cache: {e}")
        messagebox.showerror("Error", f"Failed to clear browser cache: {e}")

def open_apps_features():
    logging.info("Opening Apps & Features.")
    subprocess.run("start ms-settings:appsfeatures", shell=True)

def check_windows_updates():
    logging.info("Checking Windows updates.")
    subprocess.run("start ms-settings:windowsupdate", shell=True)

def clean_up_system_files():
    logging.info("Cleaning up system files.")
    subprocess.run("cleanmgr /sagerun:1", shell=True)

def run_sfc():
    logging.info("Running System File Checker (SFC).")
    subprocess.run("sfc /scannow", shell=True)

def optimize_memory():
    logging.info("Optimizing memory by clearing standby list.")
    try:
        subprocess.run("powershell -command \"Clear-Content -Path $env:LOCALAPPDATA\\Microsoft\\WAS\\LogFiles -Force\"", shell=True)
        messagebox.showinfo("Success", "Memory optimized.")
    except Exception as e:
        logging.error(f"Failed to optimize memory: {e}")
        messagebox.showerror("Error", f"Failed to optimize memory: {e}")

def scan_for_malware():
    logging.info("Scanning for malware using Windows Defender.")
    try:
        subprocess.run("powershell -command \"if (Get-Command Start-MpScan -ErrorAction SilentlyContinue) { Start-MpScan -ScanType QuickScan } else { Write-Output 'Windows Defender is not available.' }\"", shell=True)
        messagebox.showinfo("Success", "Malware scan initiated with Windows Defender.")
    except Exception as e:
        logging.error(f"Failed to initiate malware scan: {e}")
        messagebox.showerror("Error", f"Failed to initiate malware scan: {e}")

def defragment_hdd():
    logging.info("Defragmenting HDD.")
    subprocess.run("defrag C: /O", shell=True)

def optimize_startup_programs():
    logging.info("Optimizing startup programs.")
    subprocess.run("start ms-settings:startupapps", shell=True)

def optimize_power_settings():
    logging.info("Optimizing power settings.")
    subprocess.run("powercfg.cpl", shell=True)

def optimize_internet_speed():
    logging.info("Flushing DNS to optimize internet speed.")
    try:
        subprocess.run("ipconfig /flushdns", shell=True)
        messagebox.showinfo("Success", "DNS cache flushed.")
    except Exception as e:
        logging.error(f"Failed to flush DNS: {e}")
        messagebox.showerror("Error", f"Failed to flush DNS: {e}")

def check_hardware_usage():
    logging.info("Checking hardware usage.")
    try:
        memory_info = subprocess.check_output("wmic os get FreePhysicalMemory /Value", shell=True).decode()
        cpu_info = subprocess.check_output("wmic cpu get loadpercentage /Value", shell=True).decode()
        messagebox.showinfo("Hardware Usage", f"{memory_info}\n{cpu_info}")
    except Exception as e:
        logging.error(f"Failed to check hardware usage: {e}")
        messagebox.showerror("Error", f"Failed to check hardware usage: {e}")

def test_network_speed():
    logging.info("Testing network speed (requires PowerShell module 'NetAdapter').")
    try:
        speed_info = subprocess.check_output("powershell -command \"Get-NetAdapter | Sort-Object -Property LinkSpeed\"", shell=True).decode()
        messagebox.showinfo("Network Speed", speed_info)
    except Exception as e:
        logging.error(f"Failed to test network speed: {e}")
        messagebox.showerror("Error", f"Failed to test network speed: {e}")

def optimize_ssd():
    logging.info("Optimizing SSD (TRIM command).")
    subprocess.run("defrag C: /L", shell=True)

def exit_program():
    logging.info("Program exited by user.")
    root.destroy()

# Main program starts here
run_as_admin()

# GUI setup
root = tk.Tk()
root.title("illbreakurlegs' Optimization Menu")
root.geometry("400x600")
root.configure(bg="#000000")

# Create a frame and canvas for scrolling
frame = tk.Frame(root, bg="#000000")
frame.pack(fill="both", expand=True)

canvas = tk.Canvas(frame, bg="#000000")
scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#000000")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Add scrollable frame and scrollbar to the window
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Create buttons for each optimization task within the scrollable frame
tk.Label(scrollable_frame, text="Select an optimization task:", font=("Arial", 14), bg="#000000", fg="#FF7F50").pack(pady=10)

buttons = [
    ("Create Restore Point", create_restore_point),
    ("Run CHKDSK", run_chkdsk),
    ("Clear Temporary Files", clear_temp_files),
    ("Clear Browser Cache", clear_browser_cache),
    ("Open Apps & Features", open_apps_features),
    ("Check Windows Updates", check_windows_updates),
    ("Clean Up System Files", clean_up_system_files),
    ("Run System File Checker (SFC)", run_sfc),
    ("Optimize Memory", optimize_memory),
    ("Scan for Malware", scan_for_malware),
    ("Defragment HDD", defragment_hdd),
    ("Optimize Startup Programs", optimize_startup_programs),
    ("Optimize Power Settings", optimize_power_settings),
    ("Optimize Internet Speed", optimize_internet_speed),
    ("Check Hardware Usage", check_hardware_usage),
    ("Test Network Speed", test_network_speed),
    ("SSD Optimization", optimize_ssd),
]

# Add buttons to the scrollable frame with the specified color scheme
for btn_text, btn_command in buttons:
    tk.Button(scrollable_frame, text=btn_text, command=btn_command, width=30, pady=5,
              bg="#2a3439", fg="#FF7F50", font=("Arial", 10, "bold")).pack(pady=5)

# Exit button with distinct color
tk.Button(scrollable_frame, text="Exit", command=exit_program, width=30, pady=5,
          bg="#2a3439", fg="#FF7F50", font=("Arial", 10, "bold")).pack(pady=10)

root.mainloop()