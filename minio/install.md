# Helm 리포지토리 추가
helm repo add minio https://operator.min.io/
helm repo update
 
# Operator 설치 (네임스페이스 자동 생성)
helm install --namespace minio-operator \
  --create-namespace minio-operator minio/operator
 
# 테넌트 전용 네임스페이스 생성
kubectl create ns minio-tenant-1
 
# 테넌트 Helm 차트 설치
helm install minio-tenant minio/tenant \
  --namespace minio-tenant-1 \
  --set 'tenants[0].name=tenant-1' \
  --set 'tenants[0].pools[0].servers=4' \
  --set 'tenants[0].pools[0].volumesPerServer=4' \
  --set 'tenants[0].pools[0].storageClassName=direct-csi-min-io' \
  --set 'tenants[0].image=minio/minio:RELEASE.2024-01-05T18-11-18Z'
