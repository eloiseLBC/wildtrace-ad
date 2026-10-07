from flask import Blueprint, redirect, request
from services.system import run

network_bp = Blueprint("network", __name__)

@network_bp.route("/hotspot/on", methods=["POST"])
def hotspot_on():
    run("sudo nmcli device disconnect wlan0")
    run("sudo nmcli device wifi hotspot ssid wildtrace-hotspot password wildtrace ifname wlan0")
    return redirect("/")

@network_bp.route("/hotspot/off", methods=["POST"])
def hotspot_off():
    run("sudo nmcli connection down Hotspot")
    return redirect("/")

@network_bp.route("/wifi/connect", methods=["POST"])
def wifi_connect():
    ssid = request.form.get("ssid", "").strip()
    password = request.form.get("password", "").strip()

    run("sudo nmcli connection down Hotspot")
    run("sleep 6")
    run("sudo nmcli device disconnect wlan0")
    run("sleep 3")

    if password:
        run(f"sudo nmcli device wifi connect '{ssid}' password '{password}' name '{ssid}'")
    else:
        run(f"sudo nmcli device wifi connect '{ssid}' name '{ssid}'")

    return f"Connecting to WiFi '{ssid}'…"
