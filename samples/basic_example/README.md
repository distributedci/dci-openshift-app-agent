# Basic example

This example creates a deployment with a pod from a web server image, and validates if the pods are running.
The deployment uses anti-affinity and replicas, also a service and route are created to access the web service.

The table below shows the available variables and their default values.

Name                               | Default                                              | Description
---------------------------------- | ---------------------------------------------------- | -------------------------------------------------------------
dci\_openshift\_app\_ns            | myns                                                 | Name of the NS to use
dci\_openshift\_app\_replicas      | 1                                                    | Number of pod replicas to deploy with anti-affinity rule
dci\_openshift\_app\_image         | docker.io/kennethreitz/httpbin:latest                | Name of the image to use for the web server pod
dci\_local\_registry               | defined in disconnected envs                         | Name of the registry to use to pull web server image
