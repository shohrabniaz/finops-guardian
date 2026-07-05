import os

from flask import Flask, jsonify, request

from detectors import demo_findings, run_live_scan
from reporter import build_response

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "finops-guardian"})


@app.get("/v1/scan")
def scan_get():
    demo = request.args.get("demo", "").lower() in ("1", "true", "yes")
    subscription = request.args.get("subscription") or os.environ.get("AZURE_SUBSCRIPTION_ID")
    return _run_scan(demo=demo, subscription=subscription)


@app.post("/v1/scan")
def scan_post():
    body = request.get_json(silent=True) or {}
    demo = bool(body.get("demo"))
    subscription = body.get("subscription") or os.environ.get("AZURE_SUBSCRIPTION_ID")
    return _run_scan(demo=demo, subscription=subscription)


def _run_scan(*, demo: bool, subscription: str | None):
    if demo:
        findings = demo_findings()
    elif subscription:
        try:
            findings = run_live_scan(subscription)
        except RuntimeError as exc:
            return jsonify({"error": str(exc), "hint": "Configure Azure CLI or use ?demo=true"}), 503
    else:
        return jsonify(
            {
                "error": "Provide ?demo=true or subscription query/body",
                "example": "/v1/scan?demo=true",
            }
        ), 400

    return jsonify(build_response(findings))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
