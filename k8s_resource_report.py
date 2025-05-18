from kubernetes import client, config
from tabulate import tabulate

def parse_quantity(quantity):
    """Converte as unidades do Kubernetes para números"""
    if quantity.endswith("m"):
        return float(quantity[:-1]) / 1000
    elif quantity.endswith("Mi"):
        return float(quantity[:-2]) / 1024
    elif quantity.endswith("Gi"):
        return float(quantity[:-2])
    else:
        try:
            return float(quantity)
        except:
            return 0.0

def analyze_pod_resources():
    config.load_kube_config()
    v1 = client.CoreV1Api()

    pods = v1.list_pod_for_all_namespaces(watch=False)

    report = []
    for pod in pods.items:
        for container in pod.spec.containers:
            name = f"{pod.metadata.namespace}/{pod.metadata.name}"
            cname = container.name
            limits = container.resources.limits or {}
            requests = container.resources.requests or {}

            cpu_req = parse_quantity(requests.get('cpu', '0'))
            mem_req = parse_quantity(requests.get('memory', '0'))
            cpu_lim = parse_quantity(limits.get('cpu', '0'))
            mem_lim = parse_quantity(limits.get('memory', '0'))

            suggestion = []
            if cpu_req == 0 and mem_req == 0:
                suggestion.append("⚠️ Definir requests")
            if cpu_lim == 0 and mem_lim == 0:
                suggestion.append("⚠️ Definir limits")
            if cpu_lim < cpu_req or mem_lim < mem_req:
                suggestion.append("⚠️ Limits < Requests")

            report.append([
                name,
                cname,
                f"{cpu_req:.2f}",
                f"{cpu_lim:.2f}",
                f"{mem_req:.2f}Gi",
                f"{mem_lim:.2f}Gi",
                ", ".join(suggestion) if suggestion else "✅"
            ])

    headers = ["Pod", "Container", "CPU Req", "CPU Lim", "Mem Req", "Mem Lim", "Sugestão"]
    print(tabulate(report, headers=headers, tablefmt="fancy_grid"))

if __name__ == "__main__":
    analyze_pod_resources()
