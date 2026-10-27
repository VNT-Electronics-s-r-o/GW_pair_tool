import os
import platform
import sys
from pathlib import Path

DEVICE_MAP = {
    '702000': 'GW100',
    '416600': 'FM20',
    '7020PT': 'ZEBU',
    'S40010': 'AGRIFENCE'
}

DEV_MODE = False
PROD = True
IS_WINDOWS = platform.system() == "Windows"

IS_FROZEN = getattr(sys, "frozen", False)
PROGRAM_DIR = Path(sys.executable).resolve().parent if IS_FROZEN else Path(__file__).resolve().parent
CONFIG_DIR = PROGRAM_DIR.parent / "config" if IS_FROZEN else PROGRAM_DIR
ENV_PATH = CONFIG_DIR / ".env"
APP_DIR = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
ICONS_PATH = str(APP_DIR / "assets") + os.sep

SAVE_PATH_GW100 = r'\\192.168.1.95\\Vyroba\\fencee\\GatewayData\\GW-100' if IS_WINDOWS else '/mnt/vyroba/fencee/GatewayData/GW-100'
SAVE_PATH_FM20= r'\\192.168.1.95\\Vyroba\\fencee\\GatewayData\\FM-20' if IS_WINDOWS else '/mnt/vyroba/fencee/GatewayData/FM-20'
SAVE_PATH_ZEBU = r'\\192.168.1.95\\Vyroba\\fencee\\GatewayData\\Zebu' if IS_WINDOWS else '/mnt/vyroba/fencee/GatewayData/Zebu'
SAVE_PATH_AGRIFENCE = r'\\192.168.1.95\\Vyroba\\fencee\\GatewayData\\Agrifence' if IS_WINDOWS else '/mnt/vyroba/fencee/GatewayData/Agrifence'


