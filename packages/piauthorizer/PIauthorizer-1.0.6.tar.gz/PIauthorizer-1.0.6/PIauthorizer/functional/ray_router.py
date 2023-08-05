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

@ray_router.on_event("startup")
def startup_event():
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
        ray.init(f"ray://{head_service_ip}:{client_port}", runtime_env={'env_vars': dict(os.environ)})
        detached=True
    assert ray.is_initialized() == True
    serve.start(detached=detached)

@ray_router.get('/delete')
def delete(name:str):
    """ Delete a deployment by name. """
    serve.get_deployment(name).delete()
    return 'ok'

@ray_router.get('/show_deployments')
def show_deployments():
    """ Get an overview of the deployments along with their replicas, and assigned resources. """
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

@ray_router.get('/update_deployment')
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
    serve.get_deployment(name).options(num_replicas=num_replicas, ray_actor_options={'num_cpus': num_cpus, 'num_gpus': num_gpus, 'memory': 1024*1024*memory_mb}).deploy()
    return 'ok'

@ray_router.get('/cluster_resources')
def cluster_resources(): 
    """Show resources present in the cluster. """
    return ray.cluster_resources()

@ray_router.get('/available_resources')
def available_resources():
    """Show resources available in the cluster. """
    return ray.available_resources()
    
@ray_router.on_event("shutdown")  # Code to be run when the server shutdown.
async def shutdown_event():
    """ Shutdown ray and serve instances. """
    for key in serve.list_deployments().keys():
        serve.get_deployment(key).delete()
    serve.shutdown()
    ray.shutdown()
