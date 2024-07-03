# Attach ZTP spoke cluster

This sample performs the spoke cluster attachment to a given hub cluster.

The following role from redhatci.ocp collection is called:

- [redhatci.ocp.acm_attach_spoke_cluster](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/acm_attach_spoke_cluster/README.md): This role allows to attach a spoke cluster to a given hub cluster.

# Inventory example

```
---

all:
  hosts:
    jumphost:
      ansible_connection: local
  vars:
    spoke_cluster_name: bevo2
    spoke_cluster_kubeconfig_path: "/var/lib/dci-openshift-agent/clusterconfigs-{{ spoke_cluster_name }}/kubeconfig"

...
```

# Pipeline example

Note this example takes the following input variables from previous pipelines: `hub_kubeconfig` and `spoke_kubeconfig`, which are forwarded to outputs.

```
---

- name: ztp-attach-spoke
  stage: ztp-attach-spoke
  prev_stages: [ztp-detach-spoke]
  ansible_playbook: /usr/share/dci-openshift-app-agent/dci-openshift-app-agent.yml
  ansible_cfg: /path/to/ansible.cfg
  ansible_inventory: /path/to/inventory
  configuration: "@QUEUE"
  dci_credentials: ~/.config/dci-pipeline/credentials.yml
  ansible_extravars:
    dci_config_dir: /var/lib/dci-openshift-app-agent/samples/day_2_cluster_operations/attach_spoke_cluster
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
