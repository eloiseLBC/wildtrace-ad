from flask import Blueprint, request, redirect
from services.wildtrace import run_collect, run_send, run_compute, run_contextualize
from services.moods import add_mood
from services.timezone import get_timezone_option

actions_bp = Blueprint("actions", __name__)

@actions_bp.route("/collect", methods=["POST"])
def collect():
    moods = request.form.getlist("moods")
    zone = request.form.getlist("zone")
    timezone_option = get_timezone_option(zone[0]) if zone else None
    environments = request.form.getlist("environments")
    run_collect(moods, timezone_option, environments)
    return redirect("/")

@actions_bp.route("/send")
def send():
    run_send()
    return redirect("/")

@actions_bp.route("/compute")
def compute():
    run_compute()
    return redirect("/")

@actions_bp.route("/contextualize")
def contextualized():
    run_contextualize()
    return redirect("/")

@actions_bp.route("/moods/add", methods=["POST"])
def add_mood_route():
    label = request.form.get("label", "").strip()
    emoji = request.form.get("emoji", "🙂").strip()

    if label:
        add_mood(label, emoji)

    return redirect("/collect/form")
