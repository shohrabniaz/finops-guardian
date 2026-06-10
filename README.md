# FinOps Guardian

Azure cost leak detector — idle VMs, orphaned disks, missing tags, and oversized workloads.

## Quick start (no Azure)

```powershell
cd finops-guardian
python -m src.cli scan --demo
```

JSON output:

```powershell
python -m src.cli scan --demo --format json
```

## Live scan (requires Azure)

```powershell
az login
python -m src.cli scan --subscription <SUBSCRIPTION_ID>
```

App registration needs **Cost Management Reader** + **Reader** on the subscription.

## Checks

| ID | Finding | Severity |
|----|---------|----------|
| FIN-DISK-001 | Unattached managed disks | High |
| FIN-IP-001 | Unassociated public IPs | Medium |
| FIN-VM-001 | Deallocated VMs retaining disks | Medium |
| FIN-TAG-001 | Missing cost allocation tags | Low |
| FIN-SIZE-001 | Oversized VMs (demo / Advisor) | High |

Exit code `1` when HIGH or CRITICAL findings exist (useful for CI gates).

## CI

```yaml
python -m src.cli scan --demo
```

## Roadmap

- Deploy scan API to Heroku (Student Pack credit)
- Azure Cost Management API integration for spend trends
- Scheduled GitHub Action with OIDC
