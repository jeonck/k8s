## Kafka 사용 예제
![image](https://github.com/user-attachments/assets/9fe6323a-b33a-4bff-8fdc-27685abbc2da)


이 예제에서는 Apache Kafka를 사용하여 토픽을 생성하고, 프로듀서를 통해 메시지를 보내며, 컨슈머를 통해 메시지를 읽는 과정을 단계별로 설명합니다.

**1. 토픽 생성**

토픽은 Kafka에서 메시지를 저장하는 기본 단위입니다. 먼저, 새로운 토픽을 생성해야 합니다. 다음 명령어를 사용하여 `test-topic`이라는 이름의 토픽을 생성합니다:

```bash
kubectl exec -it my-kafka-0 -- kafka-topics.sh --create --topic test-topic --bootstrap-server my-kafka:9092

```

- `kubectl exec -it my-kafka-0`: Kubernetes 클러스터 내에서 `my-kafka-0`라는 Kafka 브로커에 접속합니다.
- `kafka-topics.sh --create`: Kafka의 토픽 생성 명령어입니다.
- `-topic test-topic`: 생성할 토픽의 이름을 지정합니다.
- `-bootstrap-server my-kafka:9092`: Kafka 브로커의 주소를 지정하여 연결합니다.

이 명령어를 실행하면 `test-topic`이라는 새로운 토픽이 생성됩니다.

**2. 프로듀서 실행 (메시지 보내기)**

토픽이 생성되면, 이제 프로듀서를 사용하여 메시지를 보낼 수 있습니다. 다음 명령어를 사용하여 `test-topic`에 메시지를 전송합니다:

```bash
kubectl exec -it my-kafka-0 -- kafka-console-producer.sh --topic test-topic --bootstrap-server my-kafka:9092

```

- `kafka-console-producer.sh`: Kafka 콘솔 프로듀서 실행 명령어입니다.
- `-topic test-topic`: 메시지를 보낼 토픽의 이름을 지정합니다.
- `-bootstrap-server my-kafka:9092`: Kafka 브로커의 주소를 지정하여 연결합니다.

이 명령어를 실행하면 프로듀서가 시작되고, 사용자는 콘솔에 직접 메시지를 입력하여 `test-topic`으로 전송할 수 있습니다. 메시지를 입력한 후 Enter 키를 누르면 해당 메시지가 토픽에 전송됩니다.

**3. 컨슈머 실행 (메시지 읽기)**

마지막으로, 컨슈머를 사용하여 `test-topic`에서 메시지를 읽어옵니다. 다음 명령어를 사용하여 메시지를 소비합니다:

```bash
kubectl exec -it my-kafka-0 -- kafka-console-consumer.sh --topic test-topic --from-beginning --bootstrap-server my-kafka:9092

```

- `kafka-console-consumer.sh`: Kafka 콘솔 컨슈머 실행 명령어입니다.
- `-topic test-topic`: 읽어올 토픽의 이름을 지정합니다.
- `-from-beginning`: 토픽의 시작부터 모든 메시지를 읽어오도록 설정합니다.
- `-bootstrap-server my-kafka:9092`: Kafka 브로커의 주소를 지정하여 연결합니다.

이 명령어를 실행하면 `test-topic`에 있는 모든 메시지가 출력됩니다. 프로듀서가 보낸 메시지를 확인할 수 있습니다.

이렇게 Kafka를 사용하여 토픽을 생성하고, 메시지를 보내고, 읽는 기본적인 과정을 완료할 수 있습니다.
