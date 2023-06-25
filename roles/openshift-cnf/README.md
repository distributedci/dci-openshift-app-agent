# Automate creation of the Openshift-cnf project for vendor validated

This role automatically creates an Openshift-cnf certification project if option `create_cnf_project: true` is provided.
And this new role is re-used some of tasks from `create-certification-project` and new templates are stored under this role.
There is no mandatory parameters are needed to update on new role for now.

Note: This new role `openshift-cnf` is just inital automation but later it will be updated more once the backend REST API given more option e.g. automatic approval and start/continue parameters as PATCH to update. 

## Global Variables
Since this new role `openshift-cnf` is re-used some existing tasks, therefore some global variables are same so please read the description from this role `create-certification-project`

## Variables to define for each Openshift-cnf

Name                     | Default                                                                    | Description
-------------------      | ------------                                                               | -------------
attach_product_listing   | false                                                                      | If set to true, it would attach product-listing to Openshift-cnf certification project.
create_cnf_project  | false                                                                      | If set to true, it would create a new Openshift-cnf certification project.

## Variables to define for project settings under `cert_listings` main variable (Optional)

Name                          | Default                              | Description
----------------------------- | ------------------------------------ | -------------
pyxis_product_list_identifier | None                                 | Product-listing ID, it has to be created before [See doc](https://redhat-connect.gitbook.io/red-hat-partner-connect-general-guide/managing-your-account/product-listing)
published                     | false                                | Boolean to enable publishing list of products
type                          | "container stack"                    | String. Type of product list
email_address                 | "mail@example.com"                   | String. email address is needed for creating openshift-cnf project



## Example Configuration of Openshift-cnf certification project creation
```yaml
---
dci_topic: OCP-4.11
dci_name: Testing Openshift-cnf auto creation and attach
dci_configuration: Using DCI create cnf project and attach product-list
check_for_existing_projects: true
ignore_project_creation_errors: true
dci_config_dirs: [/etc/dci-openshift-agent]
partner_creds: "/var/lib/dci-openshift-app-agent/auth.json"
organization_id: 15451045
#cnf_name is a free-text but format: CNF-version + OCP-version e.g "CNF23.5 OCP4.12.9"
cnf_to_certify:
  - cnf_name: "test-smf23.5 OCP4.11.5"
    create_cnf_project: true
    attach_product_listing: true

  - cnf_name: "test-upf23.5 OCP4.11.5"
    create_cnf_project: true
    attach_product_listing: true

cert_listings:
  #email_address is mandatory when creating openshift-cnf for vendor validation but does not hurt to define it
  email_address: "email@example.com"
  published: false
  type: "container stack"
  pyxis_product_list_identifier: "yyyyyyyyyyyyyyyyy" #7GC UDM

pyxis_apikey_path: "/var/lib/dci-openshift-app-agent/pyxis-apikey.txt"
dci_gits_to_components: []
...
```