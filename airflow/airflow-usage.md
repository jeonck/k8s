## Apache Airflow DAG 작성 및 업로드 방법

Apache Airflow를 사용하여 작업을 자동화하려면, 먼저 Python 파일을 특정 형식에 맞게 작성한 후, Airflow 스케줄러가 설치된 서버의 `/opt/airflow/dags/` 디렉토리에 업로드해야 합니다. 이 과정을 통해 설정한 스케줄에 따라 DAG가 자동으로 실행됩니다.

**1. Python 파일 작성**

아래는 Airflow DAG의 기본 구조를 보여주는 샘플 코드입니다. 이 코드는 매일 "Hello, Airflow!"라는 메시지를 출력하는 작업을 수행합니다.

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def my_task():
    print("Hello, Airflow!")

# DAG 정의
with DAG(
    dag_id="my_first_dag",
    start_date=datetime(2024, 2, 13),
    schedule_interval="@daily",  # 매일 실행
    catchup=False
) as dag:
    task = PythonOperator(
        task_id="print_hello",
        python_callable=my_task
    )

task  # DAG 실행

```

- `dag_id`: DAG의 고유 식별자입니다.
- `start_date`: DAG이 처음 실행될 날짜를 설정합니다.
- `schedule_interval`: DAG이 실행될 주기를 설정합니다. 여기서는 매일 실행되도록 설정했습니다.
- `catchup`: 이전 실행을 건너뛰고 현재 시점부터 실행할지 여부를 설정합니다. `False`로 설정하면 이전 실행은 무시됩니다.

**2. 파일 업로드 방법**

작성한 Python 파일을 Airflow 스케줄러가 설치된 서버의 `/opt/airflow/dags/` 디렉토리에 업로드하려면, 다음과 같은 `kubectl cp` 명령어를 사용합니다:

```bash
kubectl cp test.py airflow-scheduler-d4f745f94-c9wnz:/opt/airflow/dags/metadragon_test.py -n airflow

```

- `kubectl cp`: Kubernetes에서 파일을 복사하는 명령어입니다.
- `test.py`: 로컬에서 업로드할 파일의 이름입니다.
- `airflow-scheduler-d4f745f94-c9wnz`: Airflow 스케줄러가 실행 중인 Pod의 이름입니다.
- `/opt/airflow/dags/metadragon_test.py`: 파일이 업로드될 경로입니다.
- `n airflow`: Airflow가 실행 중인 네임스페이스를 지정합니다.

이 명령어를 실행하면, `test.py` 파일이 지정한 경로에 업로드되고, Airflow는 이 파일을 인식하여 설정된 스케줄에 따라 DAG을 실행합니다.
