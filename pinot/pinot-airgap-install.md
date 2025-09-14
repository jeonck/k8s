# 에어갭 환경에서 Apache Pinot Helm 설치 가이드 (RHEL 8.10 환경)

사용자께서 제공해주신 초안을 검토하여 최신 정보를 반영하고, RHEL(Red Hat Enterprise Linux) 8.10 환경에서 Pinot 및 Zookeeper를 안정적으로 설치할 수 있도록 최종 절차서를 작성했습니다. 특히 RHEL 환경에서 Debian 기반 Zookeeper 이미지를 사용하며 발생할 수 있는 잠재적 이슈에 대한 해결책을 명확히 제시합니다.

## 1. 사전 준비: Helm 차트 및 컨테이너 이미지 다운로드 (인터넷 연결 환경)

에어갭 환경에 설치할 모든 소프트웨어를 미리 준비해야 합니다.

### Apache Pinot Helm 차트 다운로드

Pinot 공식 Helm 리포지토리를 추가하고 업데이트합니다.

```bash
helm repo add pinot https://raw.githubusercontent.com/apache/pinot/master/helm
helm repo update
```

pinot 차트를 .tgz 형식으로 다운로드합니다. 최신 안정 버전(예: 1.0.0)을 권장합니다.

```bash
helm pull pinot/pinot --version 1.0.0
```

결과: `pinot-1.0.0.tgz` 파일이 생성됩니다.

> 참고: `tar -xzf pinot-1.0.0.tgz` 명령으로 압축을 풀어 `values.yaml` 등 내부 파일을 미리 확인할 수 있습니다.

### 필요 컨테이너 이미지 식별 및 다운로드

`pinot-1.0.0.tgz` 파일 내부의 `values.yaml`에서 필요한 모든 컨테이너 이미지를 확인합니다.

#### Pinot 컴포넌트:

- 이미지: `apachepinot/pinot`
- 버전: `0.12.0` (가장 안정적인 버전을 선택)

#### Zookeeper (필수 의존성):

- 이미지: `bitnami/zookeeper`
- 버전: `3.8.1-debian-11-r0`

> 중요: RHEL 8.10 환경에서는 Bitnami의 Debian 기반 이미지가 아닌 공식 Apache Zookeeper 이미지를 사용하는 것이 호환성 측면에서 훨씬 유리합니다. `3.8.1-debian-11-r0` 이미지에서 `apt-get` 관련 에러가 발생할 가능성이 있습니다. 따라서 `zookeeper:3.8.1` (공식 이미지, Debian/Ubuntu 기반으로 RHEL 호환성 우수)를 사용하기를 강력하게 권장합니다.

### 이미지 다운로드 및 tar 파일로 저장

```bash
# Pinot 이미지 다운로드
docker pull apachepinot/pinot:0.12.0
docker save -o pinot.tar apachepinot/pinot:0.12.0

# Zookeeper 이미지 다운로드 (Apache 공식 이미지 권장)
docker pull zookeeper:3.8.1
docker save -o zookeeper.tar zookeeper:3.8.1
```

> 참고: RHEL 환경에서는 `docker` 대신 `podman`을 사용해도 동일한 명령어로 작업할 수 있습니다.

### 파일 전송

다운로드한 `pinot-1.0.0.tgz`, `pinot.tar`, `zookeeper.tar` 파일을 USB, 네트워크 드라이브 등 물리적 매체를 이용하여 에어갭 환경으로 안전하게 전송합니다.

## 2. 에어갭 환경에서 설치 준비 및 절차

### 컨테이너 이미지 로드

전송한 tar 파일들을 에어갭 환경의 호스트에 복사한 후, `podman` 또는 `docker` 명령으로 로컬 레지스트리에 이미지를 로드합니다.

```bash
# Pinot 이미지 로드
podman load -i pinot.tar
# Zookeeper 이미지 로드
podman load -i zookeeper.tar
```

### 로컬 이미지 태깅

로드한 이미지를 로컬 컨테이너 레지스트리에 푸시해야 합니다.

```bash
# 로컬 레지스트리 URL과 포트는 환경에 맞게 변경
podman tag localhost/apachepinot/pinot:0.12.0 your-local-registry:5000/apachepinot/pinot:0.12.0
podman push your-local-registry:5000/apachepinot/pinot:0.12.0

podman tag localhost/zookeeper:3.8.1 your-local-registry:5000/zookeeper:3.8.1
podman push your-local-registry:5000/zookeeper:3.8.1
```

### values.yaml 파일 수정 (values-airgap.yaml)

전송한 `pinot-1.0.0.tgz` 파일을 압축 해제하고, 아래 내용을 포함하는 `values-airgap.yaml` 파일을 새로 생성합니다. 모든 `image.repository`는 로컬 레지스트리 주소를 가리키도록 변경합니다.

```yaml
# values-airgap.yaml
cluster:
  name: pinot-cluster

# 공통 Pinot 이미지 설정
image:
  repository: your-local-registry:5000/apachepinot/pinot
  tag: "0.12.0"
  pullPolicy: IfNotPresent # 에어갭 환경에서 필수 설정

# Controller, Broker, Server, Minion 등
controller:
  replicaCount: 1
  image:
    repository: your-local-registry:5000/apachepinot/pinot
    tag: "0.12.0"
    pullPolicy: IfNotPresent
  zkStr: "pinot-zookeeper:2181"

# Broker
broker:
  replicaCount: 1
  image:
    repository: your-local-registry:5000/apachepinot/pinot
    tag: "0.12.0"
    pullPolicy: IfNotPresent

# Server (Rook Ceph RBD 블록 스토리지)
server:
  replicaCount: 1
  image:
    repository: your-local-registry:5000/apachepinot/pinot
    tag: "0.12.0"
    pullPolicy: IfNotPresent
  persistence:
    enabled: true
    storageClass: "rook-ceph-block" # Rook Ceph RBD
    size: 10Gi

# Zookeeper (Apache 공식 이미지 사용)
zookeeper:
  enabled: true
  replicaCount: 3 # 고가용성(HA) 구성
  image:
    repository: your-local-registry:5000/zookeeper # 로컬 레지스트리의 Apache 공식 Zookeeper
    tag: "3.8.1" # Apache 공식 Zookeeper 버전
    pullPolicy: IfNotPresent
  persistence:
    enabled: true
    storageClass: "rook-ceph-fs" # Rook CephFS
    size: 8Gi

# 이미지 풀 시크릿 (필요 시)
# imagePullSecrets:
# - name: regcred

# 기타 서비스 설정
service:
  type: ClusterIP
```

### Helm 설치

수정된 `values-airgap.yaml` 파일을 사용하여 `pinot-1.0.0.tgz`를 설치합니다. 에어갭 환경에서는 `helm install` 명령어에 `--repo` 옵션 없이 로컬 .tgz 파일을 직접 지정해야 합니다.

```bash
helm install pinot ./pinot-1.0.0.tgz -f values-airgap.yaml --namespace pinot --create-namespace
```

## 3. 설치 검증 및 트러블슈팅

### 설치 상태 확인

Pinot 관련 Pod들이 모두 정상적으로 Running 상태인지 확인합니다.

```bash
kubectl get pods -n pinot
kubectl get pvc -n pinot
```

PVC가 정상적으로 바인딩되었는지 확인합니다. 만약 Pending 상태라면 스토리지 클래스(rook-ceph-block, rook-ceph-fs) 설정이 올바른지 다시 확인해야 합니다.

### RHEL 8.10 호환성 및 SELinux

RHEL의 기본 SELinux 정책이 컨테이너 실행을 방해할 수 있습니다. `podman run` 테스트 시 에러가 발생하면 `securityContext`를 통해 SELinux를 비활성화하거나, `privileged: true` 설정을 고려할 수 있습니다.

```yaml
zookeeper:
  securityContext:
    runAsNonRoot: true
    seLinuxOptions:
      level: "spc_t" # 또는 disabled
```

### Zookeeper 로그 확인

설치 후 Zookeeper Pod의 로그를 확인하여 `apt-get`, `dpkg` 등 Debian 관련 명령어 오류가 없는지 검토합니다.

```bash
kubectl logs -n pinot -l app.kubernetes.io/name=zookeeper
```

만약 로그에 Debian 관련 오류가 지속적으로 발생한다면, `values.yaml`에서 Zookeeper 이미지를 `zookeeper:3.8.1`로 변경하는 것이 올바른 해결책입니다.

---

이 절차서는 RHEL 8.10 환경에 최적화된 Pinot 에어갭 설치 가이드입니다. Zookeeper 이미지를 공식 Apache 이미지로 교체하여 호환성 문제를 사전에 방지하도록 구성했습니다.
