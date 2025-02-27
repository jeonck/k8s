# MinIO Operator 설치 (v7.0.0 기준)
kubectl apply -k "github.com/minio/operator?ref=v7.0.0"

# tenant 생성
kubectl kustomize https://github.com/minio/operator/examples/kustomization/base/ > tenant-base.yaml
kubectl create ns minio-tenant   
kubectl apply -f tenant-base.yaml

