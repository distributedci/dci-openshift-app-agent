# This role is to run the chart-verifier tool

This role is to execute the [chart-verifier](https://github.com/redhat-certification/chart-verifier) tool as part of the DCI App Agent.

## Variables

Name                               | Default                                              | Description
---------------------------------- | ---------------------------------------------------- | -------------------------------------------------------------
kubeconfig\_path                   | undefined                                            | Path to the kubeconfig file
ocp\_version\_full                 | undefined                                            | OCP version
chart\_verifier\_image             | quay.io/redhat-certification/chart-verifier:1.3.0    | Chart Verifier Image
dci\_charts                        | See defaults/main.yml                                | A list of charts with additional parameters to be used during testing. Example:<br><br>dci_charts: <br>&nbsp;&nbsp;&nbsp; -<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; chart_file: "http://xyz/chart.tgz" (required) <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; values_file: "http://xyz/values.yaml" (optional) <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; deploy_chart: true\|false. Installs and verify the chart on the the OCP cluster. <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; flags: (optional). [See helm-chart-checks](https://github.com/redhat-certification/chart-verifier/blob/main/docs/helm-chart-checks.md) for available flags <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; labels: Labels for the OWNERS file <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; submit_results: Creates a fork in the target_repository if all the test are PASS .
logs\_dir                          | /tmp                                                 | Directory to store the tests results.
github\_token\_path                | undefined                                            | GitHub token to be used to push the chart and the results to the [openshift-charts/charts](https://github.com/openshift-helm-charts/charts/) repository.
target\_repository                 | openshift-charts/charts                              | Target repository to push the chart and the results files.
submit\_results                    | false                                                | Forks and creates a PR to submit the chart and results to the `target_repository`.
partner\_name                      | undefined                                            | Partner name to be used in the pull request title.
partner\_email                     | undefined                                            | Email address to be used in the pull request.
sandbox_repository                 | undefined                                            | Target repository to submit the PRs instead of openshift-helm-charts/charts/.

### Chart requirements and installation

All the images and other required files must be reachable from the cluster nodes to complete the deployment. Other Kubernetes resources not created by the chart should be prepared in advance too. The chart report will show timeout errors if any of the images or files are not reachable. Chart deployment on a cluster can disabled but this test is mandatory for the certification.

In DCI, the project defined by `dci_openshift_app_ns` variable can be used to deploy the charts. The charts will be removed after the verification is complete. If no namespaces is defined, the resources will be deployed in the default project.

The DCI integration of helm-chart-verifier has basic support for charts deployed in disconnected environments, it will identify the images used by the chart and executes the mirroring to the local repository defined as part of the DCI disconnected settings. If the chart allows overriding the registry URL of the images used by the chart, it will be deployed in the target cluster.

### Results in DCI UI

Once the test is completed, the results will be stored in the `job_logs` directory. If the tests are executed by DCI, the results will be stored in the DCI job files section.

### Using the sandbox environment

Testing without submitting the results to the openshift-helm-charts/charts repository is possible by setting the `enable_sandbox` variable to `true` and provide a repository with a fork of [openshift-charts/charts](https://github.com/openshift-helm-charts/charts/) already available. The pull request will be done in the `sandbox_repository` repository.

### Chart submission to openshift-charts/charts

If the `submit_results` variable is set to true, the chart will be submitted to the [openshift-charts/charts](https://github.com/openshift-helm-charts/charts/) repository. This will create a fork of openshift-charts/charts repository, add the files and other metadata required by the certification process, and create the proper pull request.

This step requires the `github_token` variable set and the permissions to fork repositories in your GitHub account. See [creating-a-personal-access-token](https://docs.github.com/es/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) for more information. If the certification process is run by DCI, the token will be automatically provisioned by our dcicertbot account.

Helm Chart verifier defines 3 different test profiles: partner, redhat, and community. The DCI integration will run by default the ["partner"](https://github.com/redhat-certification/chart-verifier/blob/main/docs/helm-chart-checks.md#profiles) profile.

To fully comply with the certification process and test submission, the chart must be deployed on an OCP cluster and pass all the tests. Setting deploy_chart to `false` in the chart definition will skip the results submission. This setting combined with the use of the sandbox environment will allow to get familiar with the process and improve the chart testing before going through the certification process. The test results will be stored in the DCI job files section.

Read the certification documention in https://github.com/openshift-helm-charts/charts/tree/main/docs

### Usage from the dci-app-agent

An example of how to run the Helm chart verifier tests:

```console
$ dci-openshift-app-agent-ctl -s -- -v \
-e kubeconfig_path=path/to/kubeconfig \
-e ocp_version_full=4.7 \
-e logs_dir=results/ \
-e partner_name=telcoci/ \
-e partner_email=telcoci@redhat.com/ \
-e @helm_config.yml
```

where the config file looks like this:

```yaml
---
dci_charts:
  - chart_file: https://github.com/ansvu/samplechart/releases/download/samplechart-0.1.1/samplechart-0.1.1.tgz
    flags: -S image.repository="registry.dfwt5g.lab:4443/chart/nginx-118"
    labels: "test telcoci disconnected"
    submit_results: true
  - chart_file: https://github.com/ansvu/samplechart/releases/download/samplechart-0.1.1/samplechart-0.1.1.tgz
    labels: "test telcoci connected"
    submit_results: true
```

### Usage in a DCI Pipeline

See below for an example of how to use the chart-verifier in a DCI pipeline.

* <https://github.com/redhat-certification/chart-verifier/raw/main/pkg/chartverifier/checks/chart-0.1.0-v3.valid.tgz> is a example of a valid chart that can be used for testing purposes.

```yaml
---
- name: helm-chart-verifier
  type: cnf
  prev_stages: [ocp-upgrade, ocp]
  ansible_playbook: /usr/share/dci-openshift-app-agent/dci-openshift-app-agent.yml
  ansible_cfg: /var/lib/dci/pipelines/ansible.cfg
  ansible_inventory: /var/lib/dci/inventories/dallas/8nodes/cluster6-post.yml
  dci_credentials: /etc/dci-openshift-app-agent/dci_credentials.yml
  ansible_extravars:
    dci_cache_dir: /var/lib/dci-pipeline
    provisionhost_registry: "registry.dfwt5g.lab:4443"
    partner_creds: "/opt/pull-secret.txt"
    do_chart_verifier: true
    chart_verifier_image: quay.io/redhat-certification/chart-verifier:main
    github_token_path: "/opt/cache/token.txt"
    partner_name: "telcoci at Red Hat"
    partner_email: "telcoci@redhat.com"
    sandbox_repository: betoredhat/charts
    dci_charts:
      - chart_file: https://github.com/ansvu/samplechart/releases/download/samplechart-0.1.1/samplechart-0.1.1.tgz
        flags: -S image.repository="registry.dfwt5g.lab:4443/chart/nginx-118"
        labels: "test telcoci disconnected"
        submit_results: true
      - chart_file: https://github.com/ansvu/samplechart/releases/download/samplechart-0.1.1/samplechart-0.1.1.tgz
        labels: "test telcoci connected"
        submit_results: true
  components: []
  inputs:
    kubeconfig: kubeconfig_path
  success_tag: helm-charts-ok
```
