from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime
from kubernetes.client import models as k8s

volume = k8s.V1Volume(
    name='test-volume',
    persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(claim_name='centos-pv-claim'),
)

volume_mount = k8s.V1VolumeMount(
    name='test-volume', mount_path='/root/mount_file', sub_path=None
)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 1, 1),
    'retries': 1,
}

dag = DAG(
    'run_python_script',
    default_args=default_args,
    schedule_interval='@once'
)

run_script = KubernetesPodOperator(
    task_id='run_script',
    name='run-python-script',
    namespace='airflow',
    volumes=[volume],
    volume_mounts=[volume_mount],
    env_vars={
        'PYTHONPATH': '/root/mount_file',
        'AIRFLOW_CONN_MY_MYSQL': '{{ var.value.mysql_conn }}'
    },
    image='dlambrig/week13:1.0',
    cmds=['python', '-c', 'from my_function import my_function; my_function()'],
    arguments=[],
    dag=dag,
)

run_script2 = KubernetesPodOperator(
    task_id='run_script2',
    name='run-python-script2',
    namespace='airflow',
    volumes=[volume],
    volume_mounts=[volume_mount],
    env_vars={
        'PYTHONPATH': '/root/mount_file',
        'AIRFLOW_CONN_MY_MYSQL': '{{ var.value.mysql_conn }}'
    },
    image='dlambrig/week13:1.0',
    cmds=['python', '-c', 'from my_function import my_function; my_function()'],
    arguments=[],
    dag=dag,
)

