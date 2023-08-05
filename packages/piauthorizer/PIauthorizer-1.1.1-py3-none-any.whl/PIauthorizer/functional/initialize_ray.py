import os
import sys

import ray
from ray import serve
from ray.cluster_utils import Cluster


def initialize_ray(init: bool = False):
    """initialize ray and ray serve """
    if "pytest" in sys.modules or "--reload" in sys.argv:
        cluster = Cluster(
        initialize_head=True,
        head_node_args={
            "num_cpus": os.cpu_count(),
        })
        ray.init(address=cluster.address)
        detached = False
    else:
        head_service_ip = os.environ.get(f"NLP_CLUSTER_RAY_HEAD_SERVICE_HOST")
        client_port = os.environ.get("NLP_CLUSTER_RAY_HEAD_SERVICE_PORT_CLIENT")
        if init:
            ray.init(f"ray://{head_service_ip}:{client_port}", runtime_env={'env_vars': dict(os.environ)})
        else:
            ray.util.connect(f"{head_service_ip}:{client_port}", ray_init_kwargs={'runtime_env':{'env_vars': dict(os.environ)}})
        detached=True
    assert ray.is_initialized()
    serve.start(detached=detached)
