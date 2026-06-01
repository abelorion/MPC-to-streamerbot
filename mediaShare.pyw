import os
import subprocess

# Dynamic path tracking for queue.txt
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TXT_FILE_PATH = os.path.join(SCRIPT_DIR, "queue.txt")

# --- IMPORTANT: VERIFY THIS PATH ---
# This is the default Windows installation path for the 64-bit player.
# If yours is installed elsewhere (e.g., Program Files (x86)), update it here.
MPC_PATH = r"C:\Program Files\MPC-HC\mpc-hc64.exe"

def add_via_cli(video_url):
    """
    Bypasses the web server entirely and forces MPC-HC to ingest 
    the URL using native Windows command-line execution.
    """
    if not os.path.exists(MPC_PATH):
        print(f"[ERROR] Could not find mpc-hc64.exe at: {MPC_PATH}")
        print("Please update the MPC_PATH variable in the script to match your system.")
        return False

    print(f"[DEBUG] Executing command: mpc-hc64.exe /add \"{video_url}\"")
    
    try:
        # The /add flag explicitly tells the existing player instance 
        # to queue the item at the bottom of the playlist.
        subprocess.run([MPC_PATH, "/add", video_url], check=True)
        print(f"SUCCESS: Pushed video to queue -> {video_url}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] System command failed: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")
        return False

def process_queue_file():
    """Reads the URL from queue.txt and passes it to the CLI."""
    if not os.path.exists(TXT_FILE_PATH):
        with open(TXT_FILE_PATH, "w", encoding="utf-8") as f:
            pass
        print(f"Created '{TXT_FILE_PATH}'. Add a YouTube link and save.")
        return

    with open(TXT_FILE_PATH, "r", encoding="utf-8") as f:
        url = f.read().strip()

    if url:
        print(f"PROCESSING: Found URL in text file: {url}")
        success = add_via_cli(url)
        
        if success:
            # Wipes the file clean so it's ready for the next song
            with open(TXT_FILE_PATH, "w", encoding="utf-8") as f:
                f.write("") 
            print("queue.txt wiped clean.")
    else:
        print("NOTICE: queue.txt is empty.")

if __name__ == "__main__":
    process_queue_file()