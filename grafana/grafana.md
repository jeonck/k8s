## 1. 네임스페이스 생성

- **명령어**:
    
    ```bash
    kubectl create namespace monitoring
    
    ```
    
- **설명**: `monitoring`이라는 네임스페이스를 생성합니다.

## 2. Helm 저장소 추가

- **명령어**:
    
    ```bash
    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
    helm repo add grafana https://grafana.github.io/helm-charts
    helm repo update
    
    ```
    
- **설명**: Prometheus와 Grafana의 Helm 저장소를 추가하고 업데이트합니다.

## 3. Prometheus 설치

- **명령어**:
    
    ```bash
    helm install prometheus prometheus-community/prometheus --namespace monitoring
    
    ```
    
- **설명**: `monitoring` 네임스페이스에 Prometheus를 설치합니다.

## 4. Grafana 설치

- **명령어**:
    
    ```bash
    helm install grafana grafana/grafana --namespace monitoring --set adminPassword='***' --set service.type=ClusterIP
    
    ```
    
- **설명**: `monitoring` 네임스페이스에 Grafana를 설치하며, 관리자 비밀번호와 서비스 유형을 설정합니다.

## 5. 도메인 할당

- **설명**: Azure portal의 DNS Zone에 A 레코드를 할당합니다.
    - 예시: `grafana-dev.treal.xyz`를 AKS ingress-controller IP로 할당합니다.

## 6. Ingress 설정

1. **인증서 적용**: TLS 비밀 생성
    - **명령어**:
        
        ```bash
        kubectl create secret tls tls-grafana --key keyfile.pem --cert certfile_chain_crt.pem -n monitoring
        
        ```
        
2. **Ingress 파일 적용**: 예시 파일 `ingress.yaml`을 적용합니다.
    - **명령어**:
        
        ```bash
        kubectl apply -f ingress.yaml
        
        ```
        

## 7. Grafana 접속

- **접속 방법**: 생성한 도메인으로 접속합니다.
    - URL: `https://grafana-sample.com`
    - 기본 로그인 정보: `sample`

## 8. 데이터 소스 추가

1. Grafana에서 왼쪽 사이드바에서 **Configuration** -> **Data Sources** 선택
2. **Add data source** 클릭
3. **Prometheus** 선택 후 설정:
    - URL: `http://prometheus-server.monitoring.svc.cluster.local`
4. **Save & Test** 클릭하여 연결 확인

## 9. 쿠버네티스 모니터링

### Grafana 대시보드 가져오기

1. Grafana에서 **+ 아이콘** 클릭 후 **Import** 선택
2. Grafana.com Dashboard에서 대시보드 ID 입력:
    - 예: Kubernetes 클러스터 모니터링 대시보드 ID `6417`
3. **Load** 클릭
4. 데이터 소스로 앞서 설정한 Prometheus 선택
5. **Import** 클릭
    - 아래의 JSON 파일로 import하여 구성 가능:
        - `dashboard-cluster.json`
        - `pod-view.json`

이 절차서를 따라 쿠버네티스 모니터링 환경을 설정할 수 있습니다.
