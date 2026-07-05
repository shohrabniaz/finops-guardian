# FinOps Guardian

Azure cost leak detector — idle VMs, orphaned disks, missing tags, and oversized workloads.

## Quick start (CLI, no Azure)

```powershell
cd finops-guardian
python -m src.cli scan --demo
```

## REST API (local, kind, or Heroku)

```powershell
cd finops-guardian
pip install -r requirements.txt
python -m src.api
# GET http://localhost:8080/health
# GET http://localhost:8080/v1/scan?demo=true
```

From workspace root: `.\scripts\run-finops-api-local.ps1`

### Deploy to kind (no credit card)

See [docs/deploy-kind.md](docs/deploy-kind.md).

```powershell
.\scripts\deploy-finops-kind.ps1
kubectl port-forward -n demo svc/finops-guardian 8081:8080
```

Image: `ghcr.io/shohrabniaz/finops-guardian:latest` — also synced via GitOps `root-app`.

### Deploy to Heroku (optional — requires card verification)

See [docs/heroku-deploy.md](docs/heroku-deploy.md) — Student Pack credit.

```powershell
heroku create your-finops-guardian
git push heroku main
curl "https://your-finops-guardian.herokuapp.com/v1/scan?demo=true"
```

## Live scan (requires Azure)

```powershell
az login
python -m src.cli scan --subscription <SUBSCRIPTION_ID>
```

## Checks

| ID | Finding | Severity |
|----|---------|----------|
| FIN-DISK-001 | Unattached managed disks | High |
| FIN-IP-001 | Unassociated public IPs | Medium |
| FIN-VM-001 | Deallocated VMs retaining disks | Medium |
| FIN-TAG-001 | Missing cost allocation tags | Low |
| FIN-SIZE-001 | Oversized VMs (demo / Advisor) | High |

## CI

Lint + CLI demo + API smoke test on every push.
