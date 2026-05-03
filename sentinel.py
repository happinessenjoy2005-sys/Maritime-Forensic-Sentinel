import os, subprocess, datetime, shutil, hashlib, time, requests
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

WATCH_DIR = os.path.expanduser("~/Conservation_Project/National_Park")
LOG_FILE = os.path.expanduser("~/Conservation_Project/Logs/patrol_report.txt")
JAIL_DIR = os.path.expanduser("~/Conservation_Project/Detention_Center")

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Error sending alert: {e}")

def get_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def convert_to_degrees(value):
    d, m, s = value
    return d + (m / 60.0) + (s / 3600.0)

def get_gps_link(file_path):
    try:
        img = Image.open(file_path)
        exif_data = img._getexif()
        if not exif_data: return None
        gps_info = {}
        for tag, value in exif_data.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_info[sub_decoded] = value[t]

        if 'GPSLatitude' in gps_info and 'GPSLongitude' in gps_info:
            lat = convert_to_degrees(gps_info['GPSLatitude'])
            if gps_info['GPSLatitudeRef'] != 'N': lat = 0 - lat
            lon = convert_to_degrees(gps_info['GPSLongitude'])
            if gps_info['GPSLongitudeRef'] != 'E': lon = 0 - lon
            return f"https://www.google.com/maps?q={lat},{lon}"
    except:
        return None

print("🛡️ Guardian V6: TELEGRAM ACTIVE. Monitoring National Park...")

cmd = ["inotifywait", "-m", "-e", "create", "-e", "moved_to", "-e", "close_write", WATCH_DIR]
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

for line in process.stdout:
    file_name = line.split()[-1]
    full_path = os.path.join(WATCH_DIR, file_name)
    
    if os.path.exists(full_path):
        time.sleep(0.5)
        file_hash = get_file_hash(full_path)
        gps_url = get_gps_link(full_path)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Build the Alert for Telegram
        loc_str = f"\n📍 Location: {gps_url}" if gps_url else "\n📍 Location: No GPS metadata."
        alert_msg = f"👮 ARRESTED!\nFile: {file_name}\nTime: {timestamp}\nHash: {file_hash[:10]}...{loc_str}"
        
        # Action!
        send_telegram_msg(alert_msg)
        print(f"Alert sent to phone for {file_name}!")
        shutil.move(full_path, os.path.join(JAIL_DIR, file_name))
