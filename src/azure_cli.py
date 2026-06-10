import json
import subprocess


def _run(args: list[str]) -> str:
    result = subprocess.run(
        ["az", *args, "-o", "json"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "az command failed")
    return result.stdout


def list_unattached_disks(subscription: str) -> list[dict]:
    raw = _run(["disk", "list", "--subscription", subscription, "--query", "[?diskState=='Unattached']"])
    return json.loads(raw) if raw.strip() else []


def list_unassociated_public_ips(subscription: str) -> list[dict]:
    raw = _run(
        [
            "network",
            "public-ip",
            "list",
            "--subscription",
            subscription,
            "--query",
            "[?ipConfiguration==null]",
        ]
    )
    return json.loads(raw) if raw.strip() else []


def list_stopped_vms(subscription: str) -> list[dict]:
    raw = _run(
        [
            "vm",
            "list",
            "-d",
            "--subscription",
            subscription,
            "--query",
            "[?powerState=='VM deallocated' || powerState=='VM stopped']",
        ]
    )
    return json.loads(raw) if raw.strip() else []


def list_untagged_resources(subscription: str) -> list[dict]:
    raw = _run(
        [
            "resource",
            "list",
            "--subscription",
            subscription,
            "--query",
            "[?tags==null || tags.Environment==null]",
        ]
    )
    items = json.loads(raw) if raw.strip() else []
    return items[:50]
