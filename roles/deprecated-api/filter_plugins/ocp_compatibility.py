class FilterModule(object):
    def filters(self):
        return {
            'ocp_compatibility': self.ocp_compatibility,
        }

    def ocp_compatibility(self, after_api, curr_version, junit_ocp_file):
        '''
        Parse the deprecated and to-be-deprecated API after the workload installation.
        '''
        from junitparser import JUnitXml, TestCase, TestSuite, Failure
        from semver import VersionInfo

        # convert k8s version to ocp version
        k8s2ocp = lambda x : str(float(x) + 2.87)
        # parse the API after the workload installation and write down incompatible OCP versions
        ocp_versions = { k8s2ocp(api['status']['removedInRelease']) : 'not_compatible' for api in after_api }

        # convert major.minor version to semvers' major.minor.patch
        ocp2semver = lambda x : VersionInfo.parse(x + ".0")
        # convert semver's major.minor.patch to OCP major.minor
        semver2ocp = lambda x : '.'.join(str(x).split('.')[:-1])
        # Find max version in the set of incompatible versions.
        # If the set is empty, bump the current version.
        if ocp_versions:
            max_version = max(ocp_versions)
        else:
            max_version = semver2ocp(ocp2semver(curr_version).bump_minor())

        # Build a continuous list from current version to max_version.
        # It only works when major versions are the same.
        version = ocp2semver(curr_version)
        max_version_semver = ocp2semver(max_version)
        all_versions = []
        while version <= max_version_semver:
            all_versions.append(semver2ocp(version))
            version = version.bump_minor()

        for version in all_versions:
            if version not in ocp_versions:
                ocp_versions[version] = 'compatible'

        # convert the dictionary to JUnit test suite
        test_suite = TestSuite('Workload compatibility with OCP versions')
        for version, status in ocp_versions.items():
            test_case = TestCase(f'OCP-{version}', classname=f'Compatibility with OCP-{version}')

            if status == 'not_compatible':
                failure_message = f'The workload is not compatible with OCP-{version}'
                test_case.result = [Failure(failure_message)]

            test_suite.add_testcase(test_case)

        junit_xml = JUnitXml()
        junit_xml.add_testsuite(test_suite)
        junit_xml.write(junit_ocp_file)

        return ocp_versions
