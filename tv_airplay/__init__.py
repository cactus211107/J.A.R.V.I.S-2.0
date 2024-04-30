import time
import pyautogui
from airplay import AirPlay

# Function to find and connect to Samsung TV
def connect_to_tv(name):
    devices = AirPlay.find(timeout=10)  # Scan for available AirPlay devices

    for device in devices:
        if device.get('name') == name:
            print(f"Found TV:{name} with IP: {device.get('host')}")
            # return device.get('host')

    print("TV not found")
    return None

# Main function to mirror screen
def mirror_to_tv(name):
    tv_ip = connect_to_tv(name)
    
    if tv_ip:
        airplay = AirPlay(tv_ip)
        airplay.play('screen')
        print("Screen mirroring started to "+name)

        try:
            while True:
                screenshot = pyautogui.screenshot()
                airplay.play(screenshot)
                time.sleep(0.1)  # Adjust delay as needed
        except KeyboardInterrupt:
            airplay.stop()
            print("\nScreen mirroring stopped")

if __name__ == "__main__":
    connect_to_tv('A10 M MCCARTHY')
