# Deploy to kind GitOps lab (no credit card)

Uses the local `gitops-lab` cluster from `bootstrap-gitops-local.ps1`.

## One command

```powershell
cd "D:\New folder"
.\scripts\deploy-finops-kind.ps1
```

Builds `finops-guardian:local`, loads it into kind, and applies `k8s/deploy.yaml` in namespace `demo`.

## Access

```powershell
kubectl port-forward -n demo svc/finops-guardian 8081:8080
curl http://localhost:8081/health
curl "http://localhost:8081/v1/scan?demo=true"
```

## GitOps (GHCR)

Image: `ghcr.io/shohrabniaz/finops-guardian:latest` (published on every `main` push).

Manifest in [gitops-platform](https://github.com/shohrabniaz/gitops-platform) overlay `apps/overlays/dev/finops-guardian.yaml` — synced by Argo CD `root-app`.

## Heroku alternative

Heroku requires account verification (payment method). See [heroku-deploy.md](heroku-deploy.md) if you add a card later.
