## **Kubernetes Secrets를 환경 변수로 주입하는 과정**

## **1. Secret 생성**

Kubernetes 클러스터 내에서 사용할 Secret을 생성해야 합니다. Secret은 민감한 정보를 안전하게 저장하기 위한 객체로, 비밀번호, API 키, OAuth 토큰 등을 포함할 수 있습니다. Secret은 **`kubectl`** 명령어를 사용하여 생성할 수 있습니다.

```jsx
kubectl create secret generic my-secret --from-literal=password=mysecretpassword
```

## **2. Deployment 파일 수정**

Secret을 환경 변수로 주입하기 위해, 해당 Secret을 참조하는 Deployment YAML 파일을 수정해야 합니다. 각 컨테이너의 **`env`** 필드에 **`valueFrom.secretKeyRef`**를 사용하여 Secret의 키를 참조합니다.

```jsx
textapiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-container
        image: my-image
        env:
        - name: MY_SECRET_PASSWORD
          valueFrom:
            secretKeyRef:
              name: my-secret
              key: password
```

## **3. Pod 배포**

수정된 Deployment 파일을 사용하여 Pod를 배포합니다. 이때 Kubernetes는 지정된 Secret의 값을 환경 변수로 주입합니다.

`bashkubectl apply -f deployment.yaml`

## **4. 컨테이너 내에서 환경 변수 사용**

이제 컨테이너 내에서 주입된 환경 변수를 사용할 수 있습니다. 예를 들어, 애플리케이션 코드에서 **`MY_SECRET_PASSWORD`** 환경 변수를 참조하여 비밀번호를 사용할 수 있습니다.

## **주요 고려사항**

- **보안**: Secrets는 base64로 인코딩되어 etcd에 저장되지만, 기본적으로 암호화되지 않으므로, RBAC(Role-Based Access Control)를 통해 접근 권한을 철저히 관리해야 합니다.
- **환경 변수의 가시성**: 환경 변수는 컨테이너 내에서 쉽게 접근할 수 있지만, 악의적인 프로세스가 환경 변수를 수집할 수 있는 위험이 있으므로, 가능하다면 Secrets를 파일로 마운트하여 사용하는 것이 더 안전할 수 있습니다.

이러한 과정을 통해 Kubernetes Secrets를 안전하게 환경 변수로 주입하여 애플리케이션에서 민감한 정보를 사용할 수 있습니다.
