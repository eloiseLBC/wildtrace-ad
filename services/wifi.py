import subprocess

def get_wifi_status():
    try:
        result = subprocess.check_output(
            "nmcli -t -f NAME,TYPE,DEVICE connection show --active",
            shell=True,
            text=True
        )

        for line in result.splitlines():
            name, ctype, device = line.split(":")
            if device == "wlan0" and ctype == "802-11-wireless":
                if name == "Hotspot":
                    return ("hotspot", None)
                else:
                    return ("wifi", name)

        return ("offline", None)

    except Exception:
        return ("unknown", None)
