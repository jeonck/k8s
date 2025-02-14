# 1. 안전한 키 생성
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')

# 2. 쿠버네티스 시크릿으로 저장
kubectl create secret generic airflow-webserver-secret \
  --from-literal="webserver-secret-key=$SECRET_KEY" \
  -n airflow

# 3. Helm 차트에서 시크릿 참조
helm upgrade --install airflow apache-airflow/airflow \
  --namespace airflow \
  --set webserverSecretKey=webserver-secret-key
