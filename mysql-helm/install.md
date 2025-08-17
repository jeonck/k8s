아래는 MySQL을 Kubernetes 클러스터에 설치하기 위한 단계별 가이드입니다.

### 1. 네임스페이스 생성

```bash
kubectl create namespace mysql
```
**설명:** Kubernetes 클러스터 내에서 MySQL을 격리된 환경에서 실행하기 위해 `mysql`이라는 네임스페이스를 생성합니다.

---

### 2. Persistent Volume Claim (PVC) 생성

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-mysql-0
  namespace: mysql
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Gi
  storageClassName: ceph-rbd
```
**설명:** MySQL 데이터 저장을 위한 PVC를 생성합니다.

- **accessModes:** PVC의 접근 모드를 설정합니다. `ReadWriteOnce`는 단일 노드에서 읽기 및 쓰기가 가능함을 의미합니다.
- **resources.requests.storage:** 요청하는 스토리지 용량을 설정합니다. 여기서는 100Gi를 요청합니다.
- **storageClassName:** 사용할 스토리지 클래스 이름을 지정합니다. 여기서는 `ceph-rbd`를 사용합니다.

**PVC 생성 명령어:**

```bash
kubectl apply -f pvc.yaml
```
**설명:** 위의 YAML 파일을 `pvc.yaml`로 저장한 후, 해당 명령어로 PVC를 생성합니다.

---

### 3. Helm 저장소 추가 및 업데이트

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```
**설명:** Bitnami의 Helm 차트를 추가하고, 최신 차트 정보를 업데이트합니다. Helm은 Kubernetes 애플리케이션을 관리하는 패키지 매니저입니다.

---

### 4. MySQL 설치

```bash
helm install mysql -n mysql \
  --set auth.rootPassword=MyStrongPassls \
  --set primary.service.type=LoadBalancer \
  --set primary.persistence.existingClaim=data-mysql-0 \
  bitnami/mysql
```
**설명:** `mysql`이라는 이름으로 MySQL을 설치합니다.

- **auth.rootPassword:** MySQL의 root 비밀번호를 설정합니다.
- **primary.service.type:** 서비스 유형을 `LoadBalancer`로 설정하여 외부에서 접근할 수 있도록 합니다.
- **primary.persistence.existingClaim:** 앞서 생성한 PVC를 사용하여 MySQL 데이터의 지속성을 보장합니다.

---

### 5. Helm 차트 값 확인

```bash
helm show values bitnami/mysql > values.yaml
```
**설명:** Bitnami MySQL 차트의 기본 값을 `values.yaml` 파일로 저장합니다. 이 파일은 나중에 사용자 정의 설정을 적용하는 데 유용합니다.

---

### 6. 비밀번호 가져오기

```bash
kubectl get secret --namespace mysql mysql -o jsonpath="{.data.mysql-root-password}" | base64 -d
```
**설명:** 설치된 MySQL의 root 비밀번호를 Kubernetes 비밀에서 가져와서 디코딩합니다.

---

### 7. MySQL 접속 (서버 내부에서)

```bash
mysql -u root -p
```
**설명:** MySQL 클라이언트를 사용하여 root 계정으로 MySQL 서버에 접속합니다. 비밀번호 입력이 필요합니다.

---

### 8. root 계정에 모든 호스트에서 접속 허용

```sql
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
```
**설명:** root 계정이 모든 호스트에서 접속할 수 있도록 권한을 부여합니다.

---

### 9. 특정 IP만 허용

```sql
GRANT ALL PRIVILEGES ON *.* TO 'root'@'172.20.40.112' WITH GRANT OPTION;
```
**설명:** 특정 IP 주소에서만 root 계정으로 접속할 수 있도록 권한을 부여합니다.

---

### 10. 권한 적용

```sql
FLUSH PRIVILEGES;
```
**설명:** 변경된 권한을 적용합니다.

---

### 11. MySQL 접속 (외부에서)

```bash
mysql -h 172.20.40.117 -uroot -p
```
**설명:** 외부에서 MySQL 서버에 접속하기 위해 호스트 IP와 함께 MySQL 클라이언트를 사용합니다.

--- 

이 가이드를 통해 Kubernetes 클러스터에 MySQL을 성공적으로 설치하고 설정할 수 있습니다.
