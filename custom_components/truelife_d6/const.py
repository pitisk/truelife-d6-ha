DOMAIN = "truelife_d6"
DEFAULT_NAME = "TrueLife AIR Diffuser D6"

CONF_DEVICE_ID = "device_id"
CONF_LOCAL_KEY = "local_key"

# DPS mapping (verified on device, protocol v3.5)
DPS_POWER = "1"         # bool  – main power
DPS_STATUS = "2"        # bool  – read-only: running status (mirrors power state)
DPS_MIST_LEVEL = "3"    # enum  – "small" | "large"
DPS_LIGHT = "6"         # bool  – LED on/off
DPS_RUNNING = "7"       # bool  – read-only: device running indicator
DPS_BRIGHTNESS = "8"    # int   – LED brightness 0-1000
DPS_COLOR_MODE = "9"    # enum  – LED color mode (see COLOR_MODES)
DPS_TIMER = "11"        # int   – countdown timer (minutes remaining, 0 = off)

MIST_LEVELS = ["small", "large"]
# Verified values: "white" (standby), "colourful1"–"colourful5" (colour cycling),
# "colour" (solid colour), "scene" (scene mode)
COLOR_MODES = ["white", "colour", "scene", "colourful1", "colourful2", "colourful3", "colourful4", "colourful5"]

TUYA_PROTOCOL_VERSION = 3.5
UPDATE_INTERVAL = 30  # seconds
