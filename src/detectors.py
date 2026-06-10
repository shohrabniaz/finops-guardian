from models import Finding, Severity


def demo_findings() -> list[Finding]:
    return [
        Finding(
            check_id="FIN-DISK-001",
            title="Unattached managed disk",
            severity=Severity.HIGH,
            resource="disk-orphan-data-01",
            detail="128 GB Premium_LRS, unattached 45 days",
            remediation="Snapshot if needed, then delete unattached disk.",
            estimated_monthly_usd=19.71,
        ),
        Finding(
            check_id="FIN-IP-001",
            title="Unassociated public IP",
            severity=Severity.MEDIUM,
            resource="pip-lb-retired",
            detail="Standard SKU public IP with no NIC or LB attachment",
            remediation="Release unused public IP addresses.",
            estimated_monthly_usd=3.65,
        ),
        Finding(
            check_id="FIN-VM-001",
            title="Deallocated VM with retained disks",
            severity=Severity.MEDIUM,
            resource="vm-batch-worker-03",
            detail="VM deallocated; OS + data disks still billed",
            remediation="Delete VM and disks if no longer required.",
            estimated_monthly_usd=42.0,
        ),
        Finding(
            check_id="FIN-TAG-001",
            title="Missing cost allocation tags",
            severity=Severity.LOW,
            resource="rg-analytics-dev (12 resources)",
            detail="Resources lack Environment or CostCenter tags",
            remediation="Apply mandatory tags via Azure Policy.",
            estimated_monthly_usd=None,
        ),
        Finding(
            check_id="FIN-SIZE-001",
            title="Oversized VM with low utilization",
            severity=Severity.HIGH,
            resource="vm-api-prod-01 (Standard_D4s_v5)",
            detail="Avg CPU 4% over 14 days; right-size to D2s_v5",
            remediation="Resize or enable autoscale; review Advisor recommendation.",
            estimated_monthly_usd=86.0,
        ),
    ]


def run_live_scan(subscription: str) -> list[Finding]:
    from azure_cli import (
        list_stopped_vms,
        list_unassociated_public_ips,
        list_unattached_disks,
        list_untagged_resources,
    )

    findings: list[Finding] = []

    for disk in list_unattached_disks(subscription):
        size_gb = disk.get("diskSizeGb", 0)
        sku = disk.get("sku", {}).get("name", "Standard_LRS")
        est = _disk_monthly_usd(size_gb, sku)
        findings.append(
            Finding(
                check_id="FIN-DISK-001",
                title="Unattached managed disk",
                severity=Severity.HIGH,
                resource=disk.get("name", "unknown"),
                detail=f"{size_gb} GB {sku}, diskState=Unattached",
                remediation="Snapshot if needed, then delete unattached disk.",
                estimated_monthly_usd=est,
            )
        )

    for pip in list_unassociated_public_ips(subscription):
        sku = pip.get("sku", {}).get("name", "Basic")
        est = 3.65 if sku == "Standard" else 0.0
        findings.append(
            Finding(
                check_id="FIN-IP-001",
                title="Unassociated public IP",
                severity=Severity.MEDIUM,
                resource=pip.get("name", "unknown"),
                detail=f"{sku} SKU, no attachment",
                remediation="Release unused public IP addresses.",
                estimated_monthly_usd=est or None,
            )
        )

    for vm in list_stopped_vms(subscription):
        findings.append(
            Finding(
                check_id="FIN-VM-001",
                title="Deallocated VM with retained disks",
                severity=Severity.MEDIUM,
                resource=vm.get("name", "unknown"),
                detail=vm.get("powerState", "stopped"),
                remediation="Delete VM and disks if no longer required.",
                estimated_monthly_usd=None,
            )
        )

    untagged = list_untagged_resources(subscription)
    if untagged:
        rgs = {r.get("resourceGroup", "unknown") for r in untagged}
        findings.append(
            Finding(
                check_id="FIN-TAG-001",
                title="Missing cost allocation tags",
                severity=Severity.LOW,
                resource=f"{len(untagged)} resources in {len(rgs)} RGs",
                detail="Missing Environment or CostCenter tag",
                remediation="Apply mandatory tags via Azure Policy.",
                estimated_monthly_usd=None,
            )
        )

    return findings


def _disk_monthly_usd(size_gb: int, sku: str) -> float:
    rate = 0.154 if "Premium" in sku else 0.04
    return round(size_gb * rate, 2)
