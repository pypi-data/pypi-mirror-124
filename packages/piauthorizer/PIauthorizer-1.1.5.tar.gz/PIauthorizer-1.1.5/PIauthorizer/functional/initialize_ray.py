import os
import sys

import ray
from fastapi import FastAPI
from ray import serve
from ray.cluster_utils import Cluster

from .ray_router import ray_router


def initialize_ray(app: FastAPI, namespace:str, init: bool = False):
    """ Initialize ray and ray serve on a local cluster or by connecting to a long running Ray cluster. Also, adds the Ray Router to the app. """
    head_service_ip = os.environ.get(f"NLP_CLUSTER_RAY_HEAD_SERVICE_HOST")
    client_port = os.environ.get("NLP_CLUSTER_RAY_HEAD_SERVICE_PORT_CLIENT")
    
    if not head_service_ip:
        cluster = Cluster(
        initialize_head=True,
        head_node_args={
            "num_cpus": os.cpu_count(),
        })
        ray.init(address=cluster.address, namespace=namespace)
        detached = False
    else:
        if init:
            ray.init(f"ray://{head_service_ip}:{client_port}", runtime_env={'env_vars': dict(os.environ)}, namespace=namespace)
        else:
            ray.util.connect(f"{head_service_ip}:{client_port}", ray_init_kwargs={'runtime_env':{'env_vars': dict(os.environ)}, 'namespace': namespace})
        detached=True
        
    assert ray.is_initialized()
    serve.start(detached=detached)
    app.include_router(ray_router)
