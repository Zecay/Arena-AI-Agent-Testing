#!/usr/bin/env python3
"""
Simple Arena Agent Server for MixStudio / Chat Demo.
This server listens continuously so the web app can connect.
"""
from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# This represents whether the Arena agent session is alive.
# In a real setup, this could check session/process health.
agent_alive = True
start_time = time.time()

@app.route("/health", methods=["GET"])
def health():
    global agent_alive
    # Simple self-check: if process has been running normally, we're alive.
    # A real integration might ping an internal session endpoint.
    agent_alive = True
    return jsonify({
        "available": agent_alive,
        "status": "up",
        "uptime_seconds": int(time.time() - start_time)
    })

@app.route("/chat", methods=["POST"])
def chat():
    global agent_alive
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    tier = data.get("tier", "arena")

    if tier == "arena" and not agent_alive:
        return jsonify({"reply": "Agent unavailable.", "available": False})

    # Respond like an Arena agent would
    reply_text = f"[Arena Agent] You said: '{message}'. This server is running continuously."
    return jsonify({
        "reply": reply_text,
        "available": True,
        "tier": tier
    })

@app.route("/")
def index():
    return jsonify({
        "name": "Arena Agent Server",
        "description": "Persistent agent endpoint for MixStudio chat / Better Agents tier.",
        "endpoints": ["GET /health", "POST /chat"],
        "note": "This server must stay running. Refresh/restart manually if the session resets."
    })

if __name__ == "__main__":
    # Bind to 0.0.0.0 so the preview environment and external apps can reach it.
    app.run(host="0.0.0.0", port=8000)
