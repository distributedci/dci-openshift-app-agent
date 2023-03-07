# Resources to components role

This role can be called in `dci-openshift-app-agent` to create DCI components based on OCP resources that are running on the cluster, typically with cases where these resources were created prior to running `dci-openshift-app-agent`.

For the moment, the unique resource that we're covering with this role is the creation of components based on pods' information, but this can be extended to any resource at some point.

## Variables

Name                                    | Default                                              | Description
--------------------------------------- | ---------------------------------------------------- | -------------------------------------------------------------
dci\_resources\_to\_components          | []                                                   | List of OCP resources to be transformed to components. See the example below to check how to build this list.

## Example of dci_resources_to_components

Each entry of this list intends to gather all the resources specified on `resource` field (must be a valid OCP type, such as `Pod`, for example) in the namespace specified in `namespace` field.

```yaml
---
dci_resources_to_components:
  - resource: Pod
    namespace: test-cnf
  - resource: Pod
    namespace: production-cnf
...
```

With this configuration, this role will check all the pods deployed in `test-cnf` and `production-cnf` namespaces, and will create a DCI component in the OCP topic where the job is launched for each pod discovered, using its name and the container image version for building the name.
