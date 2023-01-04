class FilterModule(object):
    def filters(self):
        return {
            'junit2dict': self.junit2dict,
        }

    def junit2dict(self, junit_filepath):
        from junitparser import JUnitXml
        xml = JUnitXml.fromfile(junit_filepath)
        tests = []
        for suite in xml:
            for case in suite:
                tests.append({'testcase': case.name, 'passed': case.is_passed})
        return tests
