# Local Kubernetes deployment

This guide deploys the app to a local `kind` cluster. It is a practice
environment, not a public production release.

## 1. Create the cluster and image

```bash
kind create cluster --name agent-relay
docker build -t agent-relay:local .
kind load docker-image agent-relay:local --name agent-relay
```

## 2. Create local credentials

Create the Kubernetes Secret directly in the cluster. Use unique, strong local
values; do not save them in Git:

```bash
kubectl create secret generic relay-secrets \
  --from-literal=postgres-password='replace-with-a-local-secret' \
  --from-literal=enrollment-secret='replace-with-another-local-secret' \
  --from-literal=database-url='postgresql+psycopg://relay:replace-with-a-local-secret@postgres:5432/relay'
```

## 3. Start the database, then the API

```bash
kubectl apply -f k8s/postgres.yaml
kubectl rollout status statefulset/postgres --timeout=180s
```

Replace `${IMAGE_TAG}` in `k8s/agent-relay.yaml` with `local`, then apply:

```bash
sed 's/${IMAGE_TAG}/local/g' k8s/agent-relay.yaml | kubectl apply -f -
kubectl rollout status deployment/agent-relay --timeout=180s
kubectl get pods,pvc,services
```

The PostgreSQL StatefulSet uses a PersistentVolumeClaim. The API Deployment
uses `/health` for liveness and `/ready` for readiness; the app is not marked
ready until its database tables respond.

## 4. Test through a port-forward

```bash
kubectl port-forward service/agent-relay 8000:8000
```

In another terminal, verify `http://127.0.0.1:8000/ready` returns
`{"status":"ready"}` and open `http://127.0.0.1:8000/` for the dashboard.

## Clean up

Delete only this practice cluster when finished:

```bash
kind delete cluster --name agent-relay
```

Deleting the cluster also deletes its local database storage. Back up anything
you want to keep first.
