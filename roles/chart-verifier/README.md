# This role is to run the chart-verifier tool

This role is to execute the [chart-verifier](https://github.com/redhat-certification/chart-verifier) tool as part of the DCI App Agent.

## Variables

Name                               | Default                                              | Description
---------------------------------- | ---------------------------------------------------- | -------------------------------------------------------------
kubeconfig\_path                   | undefined                                            | Path to the kubeconfig file
ocp\_version\_full                 | undefined                                            | OCP version
chart\_verifier\_image             | quay.io/redhat-certification/chart-verifier:1.3.0    | Chart Verifier Image
<<<<<<< HEAD
dci\_charts                        | See defaults/main.yml                                | A list of charts with additional parameters to be used during testing. Example:<br><br>dci_charts: <br>&nbsp;&nbsp;&nbsp; -<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; name: "<RELEASE_NAME>"<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; chart_file: "http://xyz/chart.tgz" (required) <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; values_file: "http://xyz/values.yaml" (optional) <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; install: true\|false (required). Installs and verify the chart on the the OCP cluster. <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  flags: (optional). [See helm-chart-checks](https://github.com/redhat-certification/chart-verifier/blob/main/docs/helm-chart-checks.md) for available flags.
logs\_dir                          | /tmp                                                | Directory to store the tests results.
=======
dci\_charts                        | See defaults/main.yml                                | A list of charts with additional parameters to be used during testing. Example:<br><br>dci_charts: <br>&nbsp;&nbsp;&nbsp; -<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; chart_file: "http://xyz/chart.tgz" (required) <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; values_file: "http://xyz/values.yaml" (optional) <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; install: true\|false (required). Installs and verify the chart on the the OCP cluster. <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  flags: (optional). [See helm-chart-checks](https://github.com/redhat-certification/chart-verifier/blob/main/docs/helm-chart-checks.mds) for available flags <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; classification: Directory on the target repository (partner\|redhat\|community) <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; labels: Labels for the OWNERS file <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; submit_results: Creates a fork in the target_repository if all the test are PASS .
logs\_dir                          | /tmp                                                 | Directory to store the tests results.
github\_token\_path                | undefined                                            | GitHub token to be used to push the chart and the results to the [openshift-charts/charts](https://github.com/openshift-helm-charts/charts/) repository.
target\_repository                 | openshift-charts/charts                              | Target repository to push the chart and the results files.
submit\_results                    | false                                                | Forks and creates a PR to submit the chart and results to the `target_repository`.
partner\_name                      | undefined                                            | Partner name to be used in the PR title.
enable\_sandbox                    | true                                                 | Enable the sandbox environment. This submit the PR to the sandbox_repository ( betoredhat/charts) instead of openshift-helm-charts/charts.
sandbox_repository                 | betoredhat/charts                                    | Target repository to submit the PR to.
>>>>>>> 0bdc1c5 (Adding PR support - initial)

### Chart requirements and installation

If installation is enabled for a chart, all the images and other required files must be reachable from the cluster nodes in order to complete the deployment. Other Kubernetes resources not created by the chart should be prepared in advance too.

The chart report will show timeout errors if any of the images or files are not reachable.

In DCI, the namespaces defined and created by {{ dci_openshift_app_ns }} variable can be used to deploy chart. The chart will removed after the test verification is complete.

<<<<<<< HEAD
### Results
=======
### Results in DCI UI
>>>>>>> 0bdc1c5 (Adding PR support - initial)

Once the test is completed, the results will be stored the job_logs directory. If the tests are executed by DCI, the results will be stored in the DCI job files section.

### Using the sandbox environment

Testing without submitting the results to the openshift-helm-charts/charts repository is possible by setting the `enable_sandbox` variable to `true`. The results will be stored in the `sandbox_repository` repository. By default, the sandbox repository is `betoredhat/charts`. A different repository can be specified by setting the `sandbox_repository` variable but it should have already contain a fork of [openshift-charts/charts](https://github.com/openshift-helm-charts/charts/). Sandbx environment is enabled by default.

### Chart submission to openshift-charts/charts

If the `submit_results` variable is set to true, the chart will be submitted to the [openshift-charts/charts](https://github.com/openshift-helm-charts/charts/) repository. This will create a fork of openshift-charts/charts repository, add the files and other metadata required by the certification process and created the proper pull request.

This step requires the `github_token` variable set and with the permissions to fork repostories in your GitHub account. See [creating-a-personal-access-token](https://docs.github.com/es/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) for more information. If the certification process is run by DCI, the token will be automatically provisioned by our dcicertbot account. 

Read the certification documention in https://github.com/openshift-helm-charts/charts/tree/main/docs

### Usage from the dci-app-agent

An example of how to run the Helm chart verifier tests:

```console
$ dci-openshift-app-agent-ctl -s -- -v \
-e kubeconfig_path=path/to/kubeconfig \
-e ocp_version_full=4.7 \
-e logs_dir=results/ \
-e partner_name=telcoci/ \
-e @helm_config.yml
```

where the config file looks like this:

```yaml
---
dci_charts:
  -
    chart_file: http://xyz/pub/projects/mychart1.tgz
    values_file: http://xyz/pub/projects/mychart1.yml
    install: false
    classification: "partners"
    labels: "test telcoci cert"
    submit_results: true   
  -
    chart: http://xyz/pub/projects/mychart2.tgz
    chart_values: http://xyz/pub/projects/mychart2.yml
    install: true
    classification: "partners"
    labels: "mychart telcoci cert"
    submit_results: false   
```

### Usage in a DCI Pipeline

See below for an example of how to use the chart-verifier in a DCI pipeline.

* <https://github.com/redhat-certification/chart-verifier/raw/main/pkg/chartverifier/checks/chart-0.1.0-v3.valid.tgz> is a example of a valid chart that can be used for testing purposes.

```yaml
type: cnf
  prev_stages: [ocp-upgrade, ocp]
  ansible_playbook: /usr/share/dci-openshift-app-agent/dci-openshift-app-agent.yml
  ansible_cfg: /var/lib/dci/pipelines/ansible.cfg
  ansible_inventory: /var/lib/dci/inventories/myinventory.yml
  dci_credentials: /etc/dci-openshift-app-agent/dci_credentials.yml
  ansible_extravars:
    dci_cache_dir: /var/lib/dci-pipeline
    dci_config_dir: /var/lib/dci-openshift-app-agent/samples/my_hooks_dir
    provisionhost_registry: "registry:port"
    partner_creds: "/opt/pull-secret.txt"
    do_chart_verifier: true
    chart_verifier_image: quay.io/redhat-certification/chart-verifier:main
    github_token: "/opt/cache/token.txt"
    partner_name: "telcoci"
    dci_charts:
        -
          chart_file: http://xyz/pub/projects/mychart1.tgz
          values_file: http://xyz/pub/projects/mychart1.yml
          install: false
          classification: "partners"
          labels: "test telcoci cert"
          submit_results: true   
        -
          chart: https://github.com/redhat-certification/chart-verifier/raw/main/pkg/chartverifier/checks/chart-0.1.0-v3.valid.tgz
          chart_values: http://xyz/pub/projects/mychart2.yml
          flags: -S image.repository=registry:port/certified_image # Overriding chart values
          install: true
          classification: "partners"
          labels: "mychart telcoci cert"
          submit_results: false
  components: []
  inputs:
    kubeconfig: kubeconfig_path
  success_tag: helm-charts-ok
```
