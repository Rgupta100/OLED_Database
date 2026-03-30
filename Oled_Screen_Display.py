import time
import psutil
import shutil
import subprocess

# Try to load Pi libraries, but don't crash if we are on a laptop
try:
    from luma.core.interface.serial import i2c
    from luma.oled.device import ssd1306
    from luma.core.render import canvas
    from PIL import ImageFont
    from gpiozero import CPUTemperature
    
    serial = i2c(port=1, address=0x3C)
    device = ssd1306(serial)
    
    my_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    my_font_2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
    
    has_display = True
except:
    has_display = False
    print("No OLED display found. Running in terminal mode...")
    time.sleep(1)

while True:
    # 1. Gather Data (Using simple try/except so Mac/Windows doesn't crash on Linux commands)
    try:
        IP = subprocess.check_output(["hostname", "-I"]).decode('utf-8').strip().split()[0]
    except:
        IP = "127.0.0.1"

    if has_display:
        try:
            temp = CPUTemperature().temperature
        except:
            temp = 0
    else:
        temp = 45.0 # Mock temp for laptop testing

    CPU_Usage = psutil.cpu_percent(interval=None)
    Ram = psutil.virtual_memory()
    Ram_Used = int(Ram.used / (1024 * 1024))
    usage = shutil.disk_usage("/")
    Memory_free = round(usage.free / (1024**3), 2)

    try:
        wifi = subprocess.check_output(["iwconfig", "wlan0"]).decode("utf-8")
        wifi = wifi.split()[3].split("\"")[1]
    except:
        wifi = "N/A"

    # 2. Display Data
    if has_display:
        if temp > 70:
            for i in range(3):
                device.clear()
                time.sleep(1)
                with canvas(device) as draw:
                    draw.text((0, 25),"Temp Too HIGH",font=my_font_2, fill="white")
                time.sleep(1)
        elif temp < 10:
            for i in range(3):
                device.clear()
                time.sleep(1)
                with canvas(device) as draw:
                    draw.text((0, 25),"Temp Too LOW",font=my_font_2, fill="white")
                time.sleep(1)
        else:
            with canvas(device) as draw:
                draw.text((0, 0), "IP = ",font=my_font, fill="white")
                draw.text((23, 0), IP ,font=my_font, fill="white")
                draw.text((0, 10), "Temperature = ",font=my_font, fill="white")
                draw.text((80, 10), str(temp) ,font=my_font, fill="white")
                draw.text((0, 20), "CPU Usage = ",font=my_font, fill="white")
                draw.text((70, 20), str(CPU_Usage) ,font=my_font, fill="white")
                draw.text((0, 30), "Ram Usage = ",font=my_font, fill="white")
                draw.text((70, 30), str(Ram_Used),font=my_font, fill="white")
                draw.text((0, 40), "Memory Free = ",font=my_font, fill="white")
                draw.text((80, 40), str(Memory_free),font=my_font, fill="white")
                draw.text((0, 50), "Wifi = ",font=my_font, fill="white")
                draw.text((33, 50), wifi,font=my_font, fill="white")
        time.sleep(1)
        
    else:
        # Simple terminal fallback
        print("\n--- System Stats ---")
        print(f"IP: {IP}")
        print(f"Temp: {temp}")
        print(f"CPU: {CPU_Usage}%")
        print(f"RAM Used: {Ram_Used}MB")
        print(f"Disk Free: {Memory_free}GB")
        print(f"WiFi: {wifi}")
        time.sleep(2)