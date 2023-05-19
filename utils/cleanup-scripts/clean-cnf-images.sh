#!/bin/bash
#
# Copyright (C) 2023 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# A shell script to remove lingering images generated during the cnf-cert executions
# The Remore CI is used to confirm the Job status

# Params: The path to a valid remote CI

function help(){
    echo "$(basename "$0") <remote_ci_path>"
    echo "Absolute path to remote CI is missing"
}

# if [[ $# != 1 ]]; then
#     echo "Error: Missing remote CI" >&2
#     help
#     exit 1
# fi

# Source the remote CI file
# remote_ci="${1}"
# if [[ ! -f $remote_ci ]]; then
#     echo "Remote CI: ${remote_ci} does not exist, skipping" >&2
#     exit 1
# fi
# source "${remote_ci}"

# Get the container names
containers=$(podman images --format "{{.Repository}}:{{.Tag}}");

# Loop over the containers and check their job status
while IFS=, read -r name
do
  job_id=$(echo "$name" | grep -E '\w{8}(-\w{4}){3}-\w{12}' | cut -d':' -f2 | cut -d'-' -f2-)
  echo "$job_id"
  echo "$name"
  # Check if the job is in a failure state
  # fail_states=( failure error killed )
  # job_status=$(dcictl --format json job-show "${job_id}" | jq -er .job.jobstates[-1].status)
  # if [[ " ${fail_states[*]} " =~ ${job_status} ]]; then
  #   podman rmi -f "${name}"
  # fi
done <<< "${containers}"
