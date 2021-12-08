# This role is to run the chart-verifier tool

This role is to execute the [chart-verifier](https://github.com/redhat-certification/chart-verifier) tool as part of the DCI App Agent.

## Variables

Name                               | Default                                              | Description
---------------------------------- | ---------------------------------------------------- | -------------------------------------------------------------
cv\_image                          | quay.io/redhat-certification/chart-verifier:1.3.0    | Chart Verifier Image
cv\_dci\_charts                    | undefined                                        | A list of charts with additional parameters to be used during testing. Example:<br><br>cv_dci_charts: <br>&nbsp;&nbsp;&nbsp; -<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; name: "<RELEASE_NAME>"<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; chart: "http://xyz/chart.tgz" (required) <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; chart_values: "http://xyz/values.yaml" <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; flags: [See helm-chart-checks](https://github.com/redhat-certification/chart-verifier/blob/main/docs/helm-chart-checks.mds) for available flags.<br> * Charts deployment on an OCP cluster is not enabled at this moment.
cv\_job_logs                       | /tmp                                                 | Directory to store the tests results.

### Results

Once the test is completed, the results will be stored the job_logs directory. If the tests are executed by DCI, the results will be stored in the DCI job files section.

An example of how to run the Helm chart verifier tests:

```console
$ dci-openshift-app-agent-ctl -s -- -v \
-e kubeconfig_path=path/to/kubeconfig \
-e @helm_config.yml
```

where the config file looks like this:

```yaml
---
dci_charts:
  -
    name: mychart1
    chart: http://xyz/pub/projects/mychart1.tgz
    chart_values: http://xyz/pub/projects/mychart1.yml
  -
    name: mychart2
    chart: http://xyz/pub/projects/mychart2.tgz
    chart_values: http://xyz/pub/projects/mychart2.yml
```
