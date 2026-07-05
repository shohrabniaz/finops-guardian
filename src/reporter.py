import json

from models import Finding, Severity


def format_table(findings: list[Finding]) -> str:
    if not findings:
        return "No cost leaks detected."
    lines = [
        f"{'SEVERITY':<10} {'CHECK':<18} {'$/mo':<8} {'RESOURCE':<28} TITLE",
        "-" * 95,
    ]
    for f in findings:
        cost = f"${f.estimated_monthly_usd:.0f}" if f.estimated_monthly_usd else "-"
        lines.append(
            f"{f.severity.value:<10} {f.check_id:<18} {cost:<8} {f.resource[:26]:<28} {f.title}"
        )
    counts: dict[str, int] = {}
    total = 0.0
    for f in findings:
        counts[f.severity.value] = counts.get(f.severity.value, 0) + 1
        if f.estimated_monthly_usd:
            total += f.estimated_monthly_usd
    lines.append("")
    lines.append("Summary: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    if total:
        lines.append(f"Estimated recoverable spend: ~${total:.0f}/month")
    return "\n".join(lines)


def format_json(findings: list[Finding]) -> str:
    return json.dumps([f.to_dict() for f in findings], indent=2)


def build_response(findings: list[Finding]) -> dict:
    counts: dict[str, int] = {}
    total = 0.0
    for f in findings:
        counts[f.severity.value] = counts.get(f.severity.value, 0) + 1
        if f.estimated_monthly_usd:
            total += f.estimated_monthly_usd
    return {
        "findings": [f.to_dict() for f in findings],
        "summary": counts,
        "estimated_monthly_usd": round(total, 2) if total else None,
        "has_high_severity": exit_code(findings) == 1,
    }


def exit_code(findings: list[Finding]) -> int:
    for f in findings:
        if f.severity in (Severity.CRITICAL, Severity.HIGH):
            return 1
    return 0
