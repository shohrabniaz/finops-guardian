# Deploy to Heroku (GitHub Student Pack)

## Prerequisites

- [Heroku account](https://www.heroku.com/) (Student Pack credit)
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

## One-time setup

```powershell
cd finops-guardian
heroku login
heroku create finops-guardian-demo   # pick a unique name
heroku buildpacks:set heroku/python
git push heroku main
```

## Verify

```powershell
curl https://finops-guardian-demo.herokuapp.com/health
curl "https://finops-guardian-demo.herokuapp.com/v1/scan?demo=true"
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Liveness |
| GET | `/v1/scan?demo=true` | Demo cost leak findings |
| POST | `/v1/scan` | `{"demo": true}` or `{"subscription": "<id>"}` |

## Live Azure scans on Heroku

Heroku dynos do not include `az` CLI. For live scans use:

- Local CLI: `python -m src.cli scan --subscription <id>`
- Or configure a service principal + Azure SDK (future)

Demo mode works on Heroku without credentials.

## Cost

Eco/Basic dyno: covered by Student Pack for portfolio demos. Scale down when not interviewing.
