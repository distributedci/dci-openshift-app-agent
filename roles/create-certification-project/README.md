# Automate creation of the certification projects

This role automatically creates a container certification project if option `create_container_project: true` is provided, and operator certification project if `create_operator_project: true`.

## Variables

Name                     | Default                                                                    | Description
-------------------      | ------------                                                               | -------------
create_container_project | false                                                                      | If set to true, it would create new container certification project
create_operator_project  | false                                                                      | If set to true, it would create new operator certification project
connect_url              | https://connect.redhat.com/projects                                        | Certification UI link
create_project_url       | https://catalog.redhat.com/api/containers/v1/projects/certification        | Pyxis API to create certification project

## Example of configuration file

```yaml
# config example
$ cat /etc/dci-openshift-app-agent/settings.yml
---
# Job name and tags to be displayed in DCI UI
dci_name: "Containers-Preflight"
dci_tags: ["debug", "standalone-containers"]

# Optional, please provide these credentials
# if your registry is private.
partner_creds: "/opt/pull-secrets/partner_config.json"

# List of images to certify,
# you could provide many containers at once.
preflight_containers_to_certify:
  - container_image: "quay.io/rh-nfv-int/bla-bla:v0.2.9"
    # Optional; provide it when you need to submit test results
    # in the existing cert project.
    # It's an id of your Container Image Project
    # https://connect.redhat.com/projects/my_nice_container_id
    pyxis_container_identifier: "my_nice_container_id"
  - container_image: "quay.io/rh-nfv-int/noc-noc:v0.2.9"
    # Optional; provide it when you need to create new cert project
    # and submit test results in that project.
    # Please never provide create_container_project and pyxis_container_identifier
    # at once, choose one option.
    create_container_project: true

# Optional; provide it when you need to submit test results.
# This token is shared between all your projects.
# To generate it: connect.redhat.com -> Product certification ->
# Container API Keys -> Generate new key
pyxis_apikey_path: "/opt/cache/pyxis-apikey.txt"
```
