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
certified\_for\_versions            | undefined | only for certified-operator | Defines on which version the operator should be run (ex: 'v4.7' or 'v4.6-v4.10' are valid values

Those are the common variables used by both certification project.

## Operator bundle certification
Requirements needed for operator bundle are the following:

1. A project in [Red Hat Partner Connect](https://connect.redhat.com/) must be created for each operator to be tested.
2. The operator bundle image must be provided (it should already be done by the preflight).

### Role workflow
After check tests haVE been executed in the preflight role on the operator,  the role can be called to create a PR which is needed in the certification workflow of an operator.
The role will create a fork of the 'certified-operators' project, then add the manifests extracted from the bundle operator image, add them in a commit and finally create a PR to be added in the catalog of certified operator.

## Helm chart certification
Check the [README](roles/chart-verifier/README.md) of 'the chart-verifier' role.