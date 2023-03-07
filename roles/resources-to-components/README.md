# Resources to components role

This role can be called in `dci-openshift-app-agent` to create DCI components based on OCP resources that are running on the cluster, typically with cases where these resources were created prior to running `dci-openshift-app-agent`.

The resources available to check to create components are defined under the `resources_available_to_check` variable. The role checks if the resource under review has a `ownerReferences` field in the `metadata`, in whose case it will omit that resource, as there is another resource that is really creating that other resource.

## Variables

Name                                    | Default                                                                      | Description
--------------------------------------- | ---------------------------------------------------------------------------- | -------------------------------------------------------------
dci\_resources\_to\_components          | []                                                                           | List of OCP resources to be transformed to components. See the example below to check how to build this list.
resources\_available\_to\_check         | ["Pod", "Deployment", "ReplicaSet", "StatefulSet", "ClusterServiceVersion"]  | Resources that can be used to create components based on the container images used on them.

## Example of dci_resources_to_components

Each entry of this list intends to gather all the resources specified on `resource` field (must be a valid OCP type, such as `Pod`, for example) in the namespace specified in `namespace` field.

```yaml
---
dci_resources_to_components:
  - resource: Pod
    namespace: test-cnf
  - resource: ReplicaSet
    namespace: test-cnf
  - resource: Deployment
    namespace: test-cnf
  - resource: ClusterServiceVersion
    namespace: test-cnf
  - resource: Pod
    namespace: production-cnf
  - resource: StatefulSet
    namespace: production-cnf
...
```

With this configuration, this role will check all these resources in `test-cnf` and `production-cnf` namespaces, and will create a DCI component in the OCP topic where the job is launched for each container image extracted, as long as the resource does not have an `ownerReferences` field, in whose case it will be omitted.

## Component structure

This role extracts the container images used in the resources deployed in the selected namespaces. This is the main information used to build the component, as this is the real information that does not change between different jobs if using the same image for the resource (e.g. pod names can change if they are under a deployment, for example).

Naming convention followed for the components created is the following: `IMG <container_image_name> <container_image_version>`, where:

- `IMG`: string to place all the components created on this role in the same position in the component list of the job, just for making readability easier.
- `<container_image_name>`: takes the container image name removing the registry.
- `<container_image_version>`: uses the image tag or the digest, depending on what is used.

Regarding the component fields:

- Component name will be the image version, being either image tag (`latest` if ommited) or digest.
- Component type will be the image name, so that we can use that name to retrieve the different components related to the same image name but changing the version (i.e. component name).
- Component canonical project name will be the agreed string: `IMG <container_image_name> <container_image_version>`.
