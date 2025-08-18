아래는 Rook-Ceph를 이용해 Kubernetes 클러스터에 Ceph 스토리지 클러스터를 설치하는 전체 상세 절차입니다. 최신 공식 정보, 디스크 준비, YAML 파일 위치, 배포 및 확인 방법을 모두 포함하여 정리했습니다.

***

## Rook-Ceph로 Ceph 클러스터를 Kubernetes에 설치하는 상세 절차

***

### 0. 사전 준비: 디스크 준비

- Ceph용으로 사용할 **포맷되지 않은 빈 디스크 3개 이상**을 각 스토리지 노드에 준비합니다.
  - 디스크는 운영체제에 의해 마운트되어 있거나 데이터가 없어야 합니다.
  - 디스크 장치명 확인 (예: `/dev/sdb`, `/dev/sdc`, `/dev/sdd`)  
    ```bash
    lsblk
    ```
  - 각 노드에 스토리지로 할당할 디스크를 명확히 파악해 둡니다.

***

### 1. Rook-Ceph 설치 예제 YAML 파일 확보

- **공식 GitHub 저장소**에서 최신 예제 파일을 받습니다.  
  저장소 주소:  
  `https://github.com/rook/rook`  
- 경로: `deploy/examples` 폴더 내에 설치에 필요한 주요 파일들이 있습니다.
  - `crds.yaml` (CustomResourceDefinition)
  - `common.yaml` (공통 리소스)
  - `operator.yaml` (Rook-Ceph Operator)
  - `cluster.yaml` (Ceph 클러스터 설정 예시)
  - `block-pool.yaml`, `filesystem.yaml` 등 스토리지 리소스 파일들
- 다운로드 방법:
  - Git 클론 또는 각 파일 개별 Raw 다운로드 가능

```bash
git clone https://github.com/rook/rook.git
cd rook/deploy/examples
```

***

### 2. Kubernetes 네임스페이스 생성

```bash
kubectl create namespace rook-ceph
```

***

### 3. CRD 및 공통 리소스 배포

```bash
kubectl apply -f crds.yaml
kubectl apply -f common.yaml
```

***

### 4. Rook-Ceph Operator 배포

```bash
kubectl apply -f operator.yaml
```

- Operator는 Ceph 클러스터 자원들을 자동으로 관리하는 역할을 합니다.

***

### 5. Ceph 클러스터 YAML 작성 및 적용

- `cluster.yaml` 파일을 편집하여 디스크와 노드를 지정합니다.

**예: 특정 노드와 디바이스 지정 예시**

```yaml
apiVersion: ceph.rook.io/v1
kind: CephCluster
metadata:
  name: rook-ceph
  namespace: rook-ceph
spec:
  cephVersion:
    image: quay.io/ceph/ceph:v18           # 최신 Ceph 이미지 태그 확인
  mon:
    count: 3
    allowMultiplePerNode: true
  dataDirHostPath: /var/lib/rook
  storage:
    nodes:
    - name: node1-hostname
      devices:
      - name: sdb
      - name: sdc
      - name: sdd
    - name: node2-hostname
      devices:
      - name: sdb
      - name: sdc
      - name: sdd
```

- 모든 노드 모든 디바이스를 자동 사용하려면 아래처럼 설정:
```yaml
storage:
  useAllNodes: true
  useAllDevices: true
```

- YAML 수정 후 아래 명령으로 클러스터 생성:
```bash
kubectl apply -f cluster.yaml
```

***

### 6. Ceph 스토리지 자원 생성 (필요 시)

- **블록 풀 생성 (CephBlockPool)**  
  예: `block-pool.yaml`  
  ```yaml
  apiVersion: ceph.rook.io/v1
  kind: CephBlockPool
  metadata:
    name: replicapool
    namespace: rook-ceph
  spec:
    replicated:
      size: 3
  ```
- **파일 시스템 생성 (CephFilesystem)**  
  예: `filesystem.yaml`  
  ```yaml
  apiVersion: ceph.rook.io/v1
  kind: CephFilesystem
  metadata:
    name: my-cephfs
    namespace: rook-ceph
  spec:
    metadataPool:
      replicated:
        size: 3
    dataPools:
      - replicated:
          size: 3
    metadataServer:
      activeCount: 1
      activeStandby: true
  ```

```bash
kubectl apply -f block-pool.yaml
kubectl apply -f filesystem.yaml
```

***

### 7. StorageClass 설정 및 배포

- PVC에서 Ceph 스토리지를 사용할 수 있도록 StorageClass를 생성합니다.
- 공식 예제 파일 `storageclass.yaml` 활용

```bash
kubectl apply -f storageclass.yaml
```

***

### 8. 클러스터 상태 및 대시보드 확인

- Pod 상태 확인:
```bash
kubectl get pods -n rook-ceph --watch
```
- Ceph 대시보드 접속 비밀번호 확인:
```bash
kubectl -n rook-ceph get secret rook-ceph-dashboard-password -o jsonpath="{['data']['password']}" | base64 --decode && echo
```
- 대시보드 포트 포워딩 (필요 시):
```bash
kubectl -n rook-ceph port-forward deploy/rook-ceph-mgr-dashboard 7000:7000
```
- 웹 브라우저에서 `http://localhost:7000` 접속 후 비밀번호로 로그인

***

### 참고 링크

- 공식 GitHub 저장소:  
  https://github.com/rook/rook  
- 상세 배포 가이드 및 예제 모음:  
  https://nginxstore.com/blog/kubernetes/rook-ceph-클러스터-kubernetes-배포-가이드/

***

이상으로 Rook-Ceph 환경에서 Kubernetes용 Ceph 클러스터를 설치하는 데 필요한 준비부터 배포, 운영까지의 전체 절차를 최신 기준으로 상세히 정리해 드렸습니다. 각 단계별로 환경에 맞게 디스크 장치명, 노드 이름, 이미지 버전 등을 조정해 주셔야 합니다.
