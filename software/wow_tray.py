import mss
import requests
import time
import socket
import threading  
import pystray             
from PIL import Image, ImageDraw 
import sys  # [NUEVO] Necesario para rutas
import os   # [NUEVO] Necesario para rutas

# --------- CONFIGURACION ------------
ESP_HOSTNAME = "wowrgb.local" 
PIXEL_X = 1
PIXEL_Y = 1

# LIMITES DE BRILLO (para modo manual)
MAX_PWM = 1023
GREEN_LIMIT = 600
# ------------------------------------

# Variables Globales de Control
running = True
current_mode = "AUTO" # AUTO o MANUAL
global_ip = ""        # para guardar la ip y usarla en manual

# FUNCION PARA ENCONTRAR ARCHIVOS DENTRO DEL EXE O EN LA CARPETA
def resource_path(relative_path):
    """ Obtiene la ruta absoluta al recurso, funciona para dev y para PyInstaller """
    try:
        # PyInstaller crea una carpeta temporal en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# ------------ FUNCIONES DEL MENU ---------------
def set_auto(icon, item):
    global current_mode
    current_mode = "AUTO"

def set_manual(r, g):
    def callback(icon, item):
        global current_mode, global_ip
        current_mode = "MANUAL"
        try:
            requests.get(f"http://{global_ip}/manual", params={"r": r, "g": g}, timeout=0.5)
        except:
            pass
    return callback

def on_quit(icon, item):
    global running
    running = False
    icon.stop()

#CARGA IMAGEN DESDE RESOURCES/ICON.ICO
def create_image():
    try:
        icon_path = resource_path(os.path.join("resources", "icon.ico"))
        return Image.open(icon_path)
    except:
        #si no encuentra el archivo, dibuja un circulo verde
        image = Image.new('RGB', (64, 64), (0, 0, 0))
        dc = ImageDraw.Draw(image)
        dc.ellipse((10, 10, 54, 54), fill=(0, 255, 0))
        return image
# ------------------------------------------------

def wow_logic():
    global running, current_mode, global_ip

    print("===== SISTEMA WoW RGB ====")

    # Buscar IP
    print(f"Conectando con {ESP_HOSTNAME}...")
    try:
        esp_ip = socket.gethostbyname(ESP_HOSTNAME)
        global_ip = esp_ip
        print(f"Conectado: {esp_ip}")
    except socket.gaierror:
        print("ERROR: No se encuentra el sistema RGB.")
        return 

    # Sesion persistente
    session = requests.Session()
    url = f"http://{esp_ip}/health"

    print("Sistema activo.")

    # Monitor fijo en un pixel
    monitor = {"top": PIXEL_Y, "left": PIXEL_X, "width": 1, "height": 1}
    last_health = -1

    with mss.mss() as sct:
        while running: # variable global para poder cerrar
            
            # CHECK MODO
            if current_mode == "AUTO":
                try:
                    # Captura ciega
                    img = sct.grab(monitor)
                    pixel_value = img.pixel(0, 0)[0] 
                    
                    current_health = int((pixel_value / 255) * 100)
                    
                    if abs(current_health - last_health) >= 1:
                        try:
                            session.get(url, params={"percent": current_health}, timeout=0.1)
                        except Exception:
                            pass 
                        last_health = current_health

                    time.sleep(0.05)
                    
                except Exception:
                    pass
            else:
                # Si esta en MANUAL, duermo para no gastar recursos
                time.sleep(1)

# ------- ARRANQUE CON TRAY ICON ------------
if __name__ == "__main__":
    # logica en hilo separado
    t = threading.Thread(target=wow_logic)
    t.daemon = True
    t.start()
    
    # MENU:
    menu = pystray.Menu(
        pystray.MenuItem("Modo WoW (Auto)", set_auto),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Fijo: Rojo", set_manual(MAX_PWM, 0)),
        pystray.MenuItem("Fijo: Verde", set_manual(0, GREEN_LIMIT)),
        pystray.MenuItem("Fijo: Amarillo", set_manual(MAX_PWM, GREEN_LIMIT)),
        pystray.MenuItem("Fijo: Naranja", set_manual(MAX_PWM, 150)),
        pystray.MenuItem("Apagar", set_manual(0, 0)),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Salir", on_quit)
    )

    # INIT ICON (bloquea el hilo principal)
    icon = pystray.Icon("WoWRGB", create_image(), "WoW RGB", menu)
    icon.run()