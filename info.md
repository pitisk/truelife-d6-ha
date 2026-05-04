# TrueLife AIR Diffuser D6

Local integration for Home Assistant that controls the **TrueLife AIR Diffuser D6** directly over your local network — no cloud, no Tuya app dependency.

## Features

- **Humidifier** — power on/off, mist level (small / large)
- **LED light** — on/off, brightness control (0–100 %)
- **LED color mode** — white, colour, scene, colourful cycles
- Fully local — Tuya protocol v3.5 via LAN, no cloud polling

## Requirements

- TrueLife AIR Diffuser D6 connected to your Wi-Fi
- Tuya **Device ID** and **Local Key** (obtained via [tinytuya wizard](https://github.com/jasonacox/tinytuya#setup-wizard---getting-local-keys) or Tuya IoT Platform)
- Static/reserved IP address for the diffuser (recommended)

## Installation via HACS

1. HACS → ⋮ → **Custom repositories** → add `https://github.com/pitisk/truelife-d6-ha` as **Integration**
2. Download the integration from HACS
3. Restart Home Assistant
4. **Settings → Devices & Services → Add Integration** → search for **TrueLife AIR Diffuser D6**
5. Enter IP address, Device ID and Local Key

## How to get the Local Key

Run `tinytuya wizard` with your Tuya IoT Platform credentials:

```bash
docker run --rm -it python:3.12-slim sh -c \
  "pip install tinytuya -q && python -m tinytuya wizard"
```

The wizard will output a `devices.json` with the `key` field for your device.
