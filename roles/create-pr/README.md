# Create PR Role
This role groups the common tasks to create the GitHub Pull Request needed for the certification workflows.
For now, it is used by the `chart-verifier` and `preflight` roles, to handle respectively helm chart certification and operator bundle certification.

Name                                | Default   | Required                    | Description
----------------------------------- |-----------|-----------------------------| -------------------------------------------------------------
product\_name                       | undefined | true                        | Name of the chart or the operator you want to certify
product\_version                    | undefined | true                        | Version of the product
work\_dir                           | /tmp      | false                       | Directory to store the tests results.
github\_token\_path                 | undefined | true                        | GitHub token to be used to push the chart and the results to a repository.
partner\_name                       | undefined | true                        | Partner name to be used in the pull request title
partner\_email                      | undefined | true                        | Email address to be used in the pull request
target\_repository                  | undefined | true                        | Either 'openshift-helm-charts/charts' or 'redhat-openshift-ecosystem/certified-operators'
annotations\_path                   | undefined | only for certified-operator | File with the annotations of the operator bundle, specially the version the operator should be run (ex: 'v4.7' or 'v4.6-v4.10' are valid values

Those are the common variables used by both certification project.
It includes tasks to generate an SSH key needed to push to Github repository and add it to the GitHub account.
Specially, it generates an ed25519 key into the '.ssh/' folder of the ansible user's HOME and, in order to not taint any configuration, it is doing a backup of the already existing SSH key (if it already exists).

## Operator bundle certification
Requirements needed for operator bundle are the following:

1. A project in [Red Hat Partner Connect](https://connect.redhat.com/) must be created for each operator to be tested. Check the role [create-certification-project](roles/create-certification-project/README.md) to create it via this agent.
2. The Github user used when creating the fork must be added to the Project on connect.redhat.com following [these instructions from the certification project](https://github.com/redhat-openshift-ecosystem/certification-releases/blob/main/4.9/ga/troubleshooting.md#submission-validation)
3. The operator bundle image must be provided (it should already be done by the preflight).

### Role workflow
After check tests have been executed in the preflight role on the operator,  the role can be called to create a PR which is needed in the certification workflow of an operator.
The role will create a fork of the 'certified-operators' project, then add the manifests extracted from the bundle operator image and add a ci.yaml configuration file. The changes are committed and finally create a PR to be added in the catalog of certified operator.

### Annotations file
See [this documentation about annotations for bundle operator](https://github.com/operator-framework/operator-registry/blob/v1.12.6/docs/design/operator-bundle.md#bundle-annotations) here is an example of one:
```yaml
annotations:
  # Pyxis annotations.
  com.redhat.openshift.versions: "v4.7-v4.10"

  # Core bundle annotations.
  operators.operatorframework.io.bundle.mediatype.v1: registry+v1
  operators.operatorframework.io.bundle.manifests.v1: manifests/
  operators.operatorframework.io.bundle.metadata.v1: metadata/
  operators.operatorframework.io.bundle.package.v1: "my-great-operator"
  operators.operatorframework.io.bundle.channels.v1: stable
  operators.operatorframework.io.bundle.channel.default.v1: stable

  # Annotations for testing.
  operators.operatorframework.io.test.mediatype.v1: scorecard+v1
  operators.operatorframework.io.test.config.v1: tests/scorecard/
```
Note that if 'com.redhat.openshift.version annotation is missing, the role will fail.

## Helm chart certification
Check the [README](roles/chart-verifier/README.md) of 'the chart-verifier' role.