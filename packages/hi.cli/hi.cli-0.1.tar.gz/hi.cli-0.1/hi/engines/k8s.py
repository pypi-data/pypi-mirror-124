from hi.config import configuration

from kubernetes import config as kconfig, client as kclient
import kubernetes
from kubernetes.stream import stream

watch_logs = None
v1 = None
custom = None

def get_client():
    global v1
    if not v1:
        kconfig.load_kube_config()
        v1 = kclient.CoreV1Api()
    
    return v1

def get_custom_client():
    global custom
    if not custom:
        kconfig.load_kube_config()
        custom = kclient.CustomObjectsApi()

    return custom


def list_pods_in_namespace(namespace):
    client = get_client()
    return client.list_namespaced_pod(namespace=namespace).items

def get_pod_list_by_label(label, namespace):
    client = get_client()
    resp = client.list_namespaced_pod(namespace=namespace, label_selector=f"app.kubernetes.io/instance={ label }")
    return [ item.metadata.name for item in resp.items ]


def exec_in_pod(pod: str, namespace: str, commands: list):
    client = get_client()

    resp = stream(client.connect_get_namespaced_pod_exec,
                  pod,
                  namespace,
                  command=commands,
                  stderr=True, stdin=False,
                  stdout=True, tty=False)
    return resp


def logs_for_pod(pod: str, namespace: str, tail_logs=False, since=60000):
    client = get_client()

    for line in client.read_namespaced_pod_log(pod, namespace, _preload_content=False, follow=tail_logs, since_seconds=since, timestamps=True, pretty=True):
        print(line)

def get_secret_list(namespace: str, **kwargs):
    client = get_client()
    secrets = client.list_namespaced_secret(namespace, **kwargs)


def delete_pods(pods: list, namespace: str):
    client = get_client()

    for pod in pods:
        client.delete_namespaced_pod(pod, namespace)


def create_resource(kind, group, version, namespace, body):
    client = get_custom_client()
    try:
        return client.create_namespaced_custom_object(
            group,
            version,
            namespace,
            kind,
            body
        )
    except kubernetes.client.exceptions.ApiException as e:
        pass

def delete_resource(kind, group, version, namespace, body):
    client = get_custom_client()
    try:
        return client.create_namespaced_custom_object(
            group,
            version,
            namespace,
            kind,
            body
        )
    except kubernetes.client.exceptions.ApiException as e:
        pass

def list_resource(kind, group, version, namespace):
    client = get_custom_client()
    try:
        return client.list_namespaced_custom_object(
            group,
            version,
            namespace,
            kind,
        ).get("items")
    except kubernetes.client.exceptions.ApiException as e:
        pass
