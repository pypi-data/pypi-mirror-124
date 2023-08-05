import os
import sys

import ray
from fastapi import APIRouter
from PIauthorizer import ConfigManager
from PIauthorizer.logging.logged_route import LoggedRoute
from ray import serve
from ray.cluster_utils import Cluster

config_manager = ConfigManager()

ray_router = APIRouter(
    route_class=LoggedRoute, tags=['Ray'], dependencies=config_manager.get_dependencies()
)

if "pytest" in sys.modules or "--reload" in sys.argv:
    cluster = Cluster(
    initialize_head=True,
    head_node_args={
        "num_cpus": os.cpu_count()-1,
    })
    ray.init(address=cluster.address)
    detached = False
else:
    head_service_ip = os.environ.get(f"NLP_CLUSTER_RAY_HEAD_SERVICE_HOST")
    client_port = os.environ.get("NLP_CLUSTER_RAY_HEAD_SERVICE_PORT_CLIENT")
    ray.util.connect(f"{head_service_ip}:{client_port}", ray_init_kwargs={'runtime_env':{'env_vars': dict(os.environ)}})
    detached=True
assert ray.is_initialized() == True
serve.start(detached=detached)
    
@ray_router.on_event('shutdown')
def shutdown():
    ray.shutdown()
    
@ray_router.delete('/delete_deployment')
def delete_deployment(name:str):
    """ Delete a deployment by name. """
    serve.get_deployment(name).delete()
    return 'ok'

@ray_router.get('/show_deployments')
def show_deployments():
    """ Get an overview of the deployments along with their replicas, and assigned resources. """
    return get_formatted_deployments()

def get_formatted_deployments():
    deployment_list = serve.list_deployments()
    deployment = {}
    for key, _ in deployment_list.items():
        info = dict(deployment_list[key].ray_actor_options)
        info['num_replicas'] = deployment_list[key].num_replicas
        info['init_args'] = deployment_list[key].init_args
        info['func_or_class'] = deployment_list[key].func_or_class.__name__
        if "runtime_env" in info:
            del info["runtime_env"]
        deployment[key] = info
   
    return deployment


@ray_router.put('/update_deployment')
def update_deployment(name:str, num_replicas:int=None, num_cpus: float=None, num_gpus: float=None, memory_mb:int=None):
    """Only the options passed will be updated for the specific deployments.

    Args:
        name (str): name of the deployment
        num_replicas (int, optional): number of deployment replcias. Defaults to None.
        num_cpus (float, optional): fractional number of CPUs it is allowed to use. Defaults to None.
        num_gpus (float, optional): fractional number of GPUs it is allowed to use. Defaults to None.
        memory_mb (int, optional): memory in MBs. Defaults to None.

    Returns:
        str: 'ok if succeeeded'
    """
    formatted_deployments = get_formatted_deployments()
    if name not in formatted_deployments:
        return f'provide a correct deployment name from {self.formatted_deployments}'
    deployment = formatted_deployments[name]
    if not num_replicas:
        num_replicas = deployment['num_replicas']
    if not num_cpus:
        num_cpus = deployment['num_cpus']
    if not num_gpus:
        num_gpus = deployment['num_gpus']
    if not memory_mb:
        memory_mb = deployment['memory']/1024/1024
    serve.get_deployment(name).options(num_replicas=num_replicas, ray_actor_options={'num_cpus': num_cpus, 'num_gpus': num_gpus, 'memory': 1024*1024*memory_mb}).deploy()
    return True

@ray_router.get('/cluster_resources')
def cluster_resources(): 
    """Show resources present in the cluster. """
    return ray.cluster_resources()

@ray_router.get('/available_resources')
def available_resources():
    """Show resources available in the cluster. """
    return ray.available_resources()
    
