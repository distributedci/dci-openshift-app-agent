# Detach ZTP spoke cluster

This sample performs the spoke cluster detachment from a given hub cluster, with the particularity that the spoke cluster was created based on ZTP-GitOps approach.

The following roles from redhatci.ocp collection are called:

- [redhatci.ocp.remove_ztp_gitops_resources](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/remove_ztp_gitops_resources/README.md): Remove all GitOps related resources for a given spoke cluster, excepting the cluster namespace, which is not deleted because this will imply the spoke cluster is detached from the hub cluster.
- [redhatci.ocp.acm_detach_spoke_cluster](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/acm_detach_spoke_cluster/README.md): This role allows to detach a spoke cluster from a given hub cluster.

# Inventory example

```
---

all:
  hosts:
    jumphost:
      ansible_connection: local
  vars:
    spoke_cluster_name: bevo2

...
```

# Pipeline example

Note this example takes the following input variables from previous pipelines: `hub_kubeconfig` and `spoke_kubeconfig`, which are forwarded to outputs.

```
---

- name: ztp-detach-spoke
  stage: ztp-detach-spoke
  prev_stages: [acm-hub, ztp-spoke]
  ansible_playbook: /usr/share/dci-openshift-app-agent/dci-openshift-app-agent.yml
  ansible_cfg: /path/to/ansible.cfg
  ansible_inventory: /path/to/inventory
  configuration: "@QUEUE"
  dci_credentials: ~/.config/dci-pipeline/credentials.yml
  ansible_extravars:
    dci_config_dir: /var/lib/dci-openshift-app-agent/samples/day_2_cluster_operations/detach_ztp_spoke_cluster
    dci_workarounds: []
  use_previous_topic: true
  inputs:
    hub_kubeconfig: kubeconfig_path
    spoke_kubeconfig: spoke_cluster_kubeconfig_path
  # The kubeconfig points to the attached spoke cluster
  # Also export spoke_kubeconfig and hub_kubeconfig vars
  outputs:
    kubeconfig: "spoke_cluster_kubeconfig_path"
    spoke_kubeconfig: "spoke_cluster_kubeconfig_path"
    hub_kubeconfig: "kubeconfig_path"

...
```
