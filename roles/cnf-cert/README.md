# CNF-cert Role

This role encapulates the logic for the [test network function](https://github.com/test-network-function/test-network-function). It is responsible for deploying the tnf network function testing framework and running the tests in DCI. 

It is important to label the pods to test with autodiscovery labels before executing the CNF Cert Suite. You can do it manually or programatically. An example of this can be found in [tnf_test_example](https://github.com/redhat-cip/dci-openshift-app-agent/tree/master/samples/tnf_test_example).

## Variables

Name                             | Default                                              | Description
-------------------------------- | ---------------------------------------------------- | -------------------------------------------------------------
tnf\_suites                      | `"diagnostic access-control networking lifecycle observability platform-alteration operator"` | List of tnf suites to run
tnf\_config                      | <pre lang="yaml"><code>tnf_config:<br>   - namespace: "{{ dci_openshift_app_ns }}"<br>     targetpodlabels: []<br>     operators_regexp: ""<br>     exclude_connectivity_regexp: ""<br> </code></pre>  | A complex variable to define the configuration to be applied in CNF Cert Suite.<ul> <li> namespace: Target namespace. </li> <li>targetpodlabels: List of autodiscovery labels to be considered by the CNF Cert Suite for pod testing.</li><li> operators_regexp:  A regexp to select operators to be tested by the CNF Cert Suite. </li> <li>exclude_connectivity_regexp: A regexp to exclude containers from the connectivity test (optional).</li> </ul> See [this](https://github.com/redhat-cip/dci-openshift-app-agent/blob/master/samples/tnf_test_example/hooks/templates/test_deployment.yml.j2) for more details.<br> * Testing multiple resources on different namespaces is supported.
tnf\_non\_intrusive\_only        | true                                                 | Skip intrusive tests which may disrupt cluster operations.
tnf\_run\_cfd\_test              | false                                                | The test suites from openshift-kni/cnf-feature-deploy will be run prior to the actual CNF certification test execution and the results are incorporated in the same claim.
preflight\_namespace             | preflight-testing                                    | Namespace to use for preflight tests
tnf\_debug\_image                | quay.io/openshift-release-dev/ocp-v4.0-art-dev@sh... | Image to be used for oc debug command in CNF Cert Suite
tnf\_log\_level                  | "debug"                                              | Log level used to run the CNF Cert Suite. Possible values can be seen [here](https://github.com/test-network-function/test-network-function#log-level)
tnf\_postrun\_delete\_resources  | true                                                 | Control if the deployed resources are kept after the CNF Cert Suite execution for debugging purposes.

## Example of a tnf_config file to test pods deployed on multiple namespaces not using label prefixes.

The format of the targetpodlabels list has the following format: <label_name>=<label_value>

```yaml
---
    tnf_config:
      - namespace: "test-cnf"
        targetpodlabels: [environment=test]
        operators_regexp: ""
        exclude_connectivity_regexp: ""
      - namespace: "production-cnf"
        targetpodlabels: [environment=production]
        operators_regexp: ""
        exclude_connectivity_regexp: ""
...
```

## Example of a tnf_config file to test pods deployed on multiple namespaces using label prefixes 
The format of the targetpodlabels list has the following format: <label_prefix>/<label_name>=<label_value>

```yaml
---
    tnf_config:
      - namespace: "test-cnf"
        targetpodlabels: [test-network-function.com/environment=test]
        operators_regexp: ""
        exclude_connectivity_regexp: ""
      - namespace: "production-cnf"
        targetpodlabels: [test-network-function.com/environment=production]
        operators_regexp: ""
        exclude_connectivity_regexp: ""
...
```

## Defining Operators_regexp
In case of needing it, the code to handle it must be included in the partner's hooks