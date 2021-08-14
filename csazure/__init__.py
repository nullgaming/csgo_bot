from dotenv import load_dotenv
import os
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from . import callbacks
from functools import partial
from timeit import default_timer as timer

load_dotenv()

GROUP_NAME = 'warcry_group'
IP_NAME = 'warcry-ip'
VM_NAME = 'warcry'


class CSGO_AZURE:
    def __init__(self):
        subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
        credentials = ClientSecretCredential(
            tenant_id=os.environ['AZURE_TENANT_ID'],
            client_id=os.environ['AZURE_CLIENT_ID'],
            client_secret=os.environ['AZURE_CLIENT_SECRET']
        )

        self.resource_client = ResourceManagementClient(
            credentials, subscription_id)
        self.compute_client = ComputeManagementClient(
            credentials, subscription_id)
        self.network_client = NetworkManagementClient(
            credentials, subscription_id)

    def get_instance_IP(self):
        result_get = self.network_client.public_ip_addresses.get(
            GROUP_NAME,
            IP_NAME
        )
        return result_get.ip_address

    def get_server_status(self):
        try:
            vm = self.compute_client.virtual_machines.get(
                GROUP_NAME, VM_NAME, expand='instanceView')
            status = vm.instance_view.statuses[1].code
            if status == "PowerState/running":
                return "running"
            elif status == "PowerState/deallocated":
                return "stopped"
            elif status == "PowerState/starting":
                return "starting"
            elif status == "PowerState/deallocating":
                return "stopping"
        except:
            pass

    def start_server(self, ctx):
        async_vm_start = self.compute_client.virtual_machines.begin_start(
            GROUP_NAME, VM_NAME)
        start = timer()
        async_vm_start.wait()
        end = timer()
        diff = end - start
        async_vm_start.add_done_callback(func=partial(callbacks.send_callback_msg, ctx=ctx,command=0,diff=diff))
        return async_vm_start.status()

    def restart_server(self, ctx):
        async_vm_restart = self.compute_client.virtual_machines.begin_restart(
            GROUP_NAME, VM_NAME)
        start = timer()
        async_vm_restart.wait()
        end = timer()
        diff = end - start
        async_vm_restart.add_done_callback(func=partial(callbacks.send_callback_msg, ctx=ctx,command=1,diff=diff))
        return async_vm_restart.status()

    def stop_server(self, ctx):
        async_vm_stop = self.compute_client.virtual_machines.begin_deallocate(
            GROUP_NAME, VM_NAME)
        start = timer()
        async_vm_stop.wait()
        end = timer()
        diff = end - start
        async_vm_stop.add_done_callback(func=partial(callbacks.send_callback_msg, ctx=ctx,command=2,diff=diff))
        return async_vm_stop.status()
