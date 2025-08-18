Kueue의 오브젝트 흐름을 중심으로 설명하면 다음과 같습니다.

## 핵심 오브젝트와 흐름 개요

- **Workload**
  - 실제 실행될 작업(예: Kubernetes Job)을 추상화한 오브젝트로, Kueue가 관리하는 단위입니다. 사용자가 Job을 제출하면 Kueue가 자동으로 Workload 오브젝트를 생성해서 관리합니다.

- **ResourceFlavor**
  - 클러스터 내에서 사용 가능한 리소스 특성을 정의하는 오브젝트입니다. 예를 들면 GPU, 구성, 가격, 아키텍처 등 노드의 속성을 분리 지정할 수 있습니다.

- **ClusterQueue**
  - 클러스터 전체에 대한 리소스 풀로, 하나 이상의 ResourceFlavor에 대해 quota(사용량 한도)와 Fair Sharing 정책 등을 정의하는 객체입니다. 여러 LocalQueue를 하나의 ClusterQueue에 연결해 다중 테넌트 환경의 리소스 공유 구조를 만듭니다.

- **LocalQueue**
  - 네임스페이스(테넌트) 단위로 업무량(Workload)을 그룹핑한 리소스 큐입니다. LocalQueue는 특정 ClusterQueue를 가리키고, 실제 큐잉 작업은 해당 ClusterQueue가 담당합니다.

## 오브젝트 흐름

1. **Job / Workload submit**
   - 사용자가 배치 작업(Job)을 생성하면, Kueue가 해당 Job에 대해 Workload 오브젝트를 자동으로 생성합니다. Workload에는 리소스 요청, 우선순위, 필요한 Pod 수 등이 정의됩니다.

2. **Workload → LocalQueue 등록**
   - Workload 오브젝트는 지정된 LocalQueue에 등록됩니다. LocalQueue는 네임스페이스별 작업들을 하나의 큐로 묶어 ClusterQueue로 전달합니다.

3. **LocalQueue → ClusterQueue 전송, 리소스 할당 결정**
   - LocalQueue가 참조하는 ClusterQueue로 Workload가 전달되고, ClusterQueue는 ResourceFlavor별 할당 가능한 quota에 따라 실행 여부를 결정합니다.
   - 할당이 결정되면 Workload가 “admitted” 상태가 되고, 실제 Job 실행이 시작됩니다.

4. **Job 실행/상태 동기화**
   - Job이 실행되면 Pod가 할당되고, Kueue가 Workload 상태와 Job 실행 상태를 동기화합니다. 필요 시, 우선순위와 quota를 반영해 프리엠션(자원 회수)도 처리합니다.

## 오브젝트 상호작용 요약

| 단계                | 오브젝트          | 주요 역할                    |
|--------------------|------------------|-----------------------------|
| 작업 제출          | Workload         | 실제 실행할 작업 표현        |
| 테넌트 큐 등록      | LocalQueue       | 네임스페이스별 큐잉          |
| 클러스터 리소스 큐  | ClusterQueue     | 자원 풀 및 quota관리         |
| 리소스 특성 정의    | ResourceFlavor   | 노드/리소스별 특성 반영      |
| 실행/관리           | Workload, Job    | 상태 동기화, 프리엠션 처리   |

## 특징 및 활용

- 각 오브젝트는 API 리소스로 관리되어 확장성과 유연성이 높습니다.
- ClusterQueue Cohort 기능을 활용하면 여러 큐가 자원 할당을 유연하게 "빌려 쓰기"할 수 있습니다. Idle 리소스 최소화와 burst workload 지원에 효과적입니다.
- 전체 흐름은 Job 제출 → Workload 생성/큐잉 → 리소스 할당/실행 → 상태 및 quota 동기화 구조로, Kubernetes의 기존 스케줄러 기능과 유기적으로 연동됩니다.

이처럼 Kueue 오브젝트들은 각 역할에 따라 긴밀하게 상호작용하여, 배치/머신러닝 등 자원 중심 대기/실행 환경을 효율적으로 구성합니다.
