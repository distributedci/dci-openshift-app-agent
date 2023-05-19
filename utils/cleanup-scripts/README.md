# DCI cleanup scripts

DCI jobs execution may lead to generate some lingering resources that need to be cleaned up to avoid resources starvation on the servers used to execute the jobs. Those resources could be:

- Dangling images, volumes, containers.

The following scripts will allow to perform the removal of those resources. It is recommended to schedule its execution in crontab.

Please review the scripts before running them on your environment, this to detect tasks that may not be suitable for your environment.

`clean-cnf-images.sh` The following is a list of actions performed by this script:
1. Remove lingering containers images generated during the cnf-cert execution using DCI.

This script requires as parameter the dci-credentials in order to verify the status of the DCI job that generated the containers.

```ShellSession
./clean-cnf-images.sh /etc/dci-openshift-agent/<your>_dci_credentials.sh
```
