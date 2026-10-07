from flask import Blueprint
from ui.styles import CSS
from services.wifi import get_wifi_status
from services.moods import load_moods
from services.timezone import load_zones  
from services.environments import load_environments

ui_bp = Blueprint("ui", __name__)

@ui_bp.route("/")
def index():
    status, ssid = get_wifi_status()

    if status == "wifi":
        info = f"Connected to WiFi : <b>{ssid}</b>"
        net_label = "Enable hotspot"
        net_action = "/hotspot/on"
        net_method = "post"
        net_class = "btn"
    elif status == "hotspot":
        info = "Accessible Hotspot"
        net_label = "Connect WiFi"
        net_action = "/wifi/form"
        net_method = "get"
        net_class = "btn"
    else:
        info = "Network not connected"
        net_label = "Enable hotspot"
        net_action = "/hotspot/on"
        net_method = "post"
        net_class = "btn"

    return f"""
    <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            {CSS}
        </head>
        <body>
            <div class="container">
                <div class="panel">
                    <h2 id="title">WildTrace</h2>
                    <div class="subtitle" id="subtitle">Control panel</div>

                    <div id="status">{info}</div>

                    <form action="/collect/form">
                        <button class="btn secondary">Collect data</button>
                    </form>

                    <form action="/send">
                        <button class="btn secondary">Send to bucket</button>
                    </form>
                    
                    <form action="/compute">
                        <button class="btn secondary">Compute uploaded data</button>
                    </form>
                    
                    <form action="/contextualize">
                        <button class="btn secondary">Contextualize data</button>
                    </form>

                    <form action="/logs/wildtrace">
                        <button class="btn logs">WildTrace logs</button>
                    </form>

                    <form action="/logs/flask">
                        <button class="btn logs">System logs</button>
                    </form>

                    <form action="{net_action}" method="{net_method}">
                        <button class="{net_class}">{net_label}</button>
                    </form>
                </div>
            </div>
        </body>
    </html>
    """

@ui_bp.route("/wifi/form")
def wifi_form():
    return f"""
    <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            {CSS}
        </head>
        <body>
            <div class="container">
                <div class="panel">
                    <h2 id="title">WiFi</h2>
                    <div class="subtitle">Connect to a network</div>

                    <form action="/wifi/connect" method="post">
                        <input name="ssid" placeholder="SSID" required>
                        <input name="password" type="password" placeholder="Password (optional)">
                        <button class="btn">Connect</button>
                    </form>

                    <form action="/"><button class="btn secondary">Back</button></form>
                </div>
            </div>
        </body>
    </html>
    """

@ui_bp.route("/collect/form")
def collect_form():
    moods = load_moods()
    zones = load_zones() 
    environments = load_environments()

    zone_chips = "\n".join(
        f"""
        <input type="radio" id="zone-{z['id']}" name="zone" value="{z['id']}" required>
        <label for="zone-{z['id']}">{z.get('emoji','📍')} {z['label']}</label>
        """
        for z in zones
    )

    mood_chips = "\n".join(
        f"""
        <input type="checkbox" id="mood-{m['id']}" name="moods" value="{m['id']}">
        <label for="mood-{m['id']}">{m.get('emoji','🙂')} {m['label']}</label>
        """
        for m in moods
    )
    
    environment_chips = "\n".join(
        f"""
        <input type="checkbox" id="environment-{e['id']}" name="environments" value="{e['id']}">
        <label for="environment-{e['id']}">{e.get('emoji','🙂')} {e['label']}</label>
        """
        for e in environments
    )

    return f"""
        <html>
        <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        {CSS}
        </head>
        <body>
        <div class="container">
            <div class="panel">
            <h2 id="title">Collecting</h2>
            <div class="subtitle">Get my mood before collecting</div>

            <!-- FORM COLLECT -->
            <form id="collectForm" action="/collect" method="post">

                <h3 class="section-title">Zone</h3>
                <div class="mood-chips">
                    {zone_chips}
                </div>
                
                <h3 class="section-title">Environment(s)</h3>
                <div class="mood-chips">
                    {environment_chips}
                </div>

                <h3 class="section-title">Mood(s)</h3>
                <div class="mood-chips">
                    {mood_chips}
                </div>

            </form>

            <!-- FORM ADD MOOD -->
            <form action="/moods/add" method="post">
                <input class="input-logs" name="label"
                    placeholder="New mood label (e.g. Excited)" required>
                <input class="input-logs" name="emoji"
                    placeholder="Emoji (e.g. 🤩)">
                <button class="btn secondary" type="submit">Add mood</button>
            </form>

            <!-- SUBMIT COLLECT -->
            <button class="btn" type="submit" form="collectForm">Collect</button>

            <form action="/">
                <button class="btn secondary" type="submit">Back</button>
            </form>

            </div>
        </div>
        </body>
        </html>
        """
