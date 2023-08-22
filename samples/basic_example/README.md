# Basic example

This example creates a deployment and a service with a pod from an image, and validates if the web server is running.

The table below shows the available variables and their default values.

Name                               | Default                                              | Description
---------------------------------- | ---------------------------------------------------- | -------------------------------------------------------------
dci\_openshift\_app\_ns            | myns                                                 | Name of the NS to use
dci\_openshift\_app\_replicas      | 1                                                    | Number of pod replicas to deploy with anti-affinity rule
dci\_openshift\_app\_image         | mirror.gcr.io/library/nginx:latest                   | Name of the image to use for the web server pod
dci\_local\_registry               | defined in disconnected envs                         | Name of the registry to use to pull web server image
