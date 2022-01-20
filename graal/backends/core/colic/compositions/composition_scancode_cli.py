from graal.backends.core.analyzers.scancode import ScanCode
from graal.backends.core.composer import Composer


SCANCODE_CLI = 'scancode_cli'
CATEGORY_COLIC_SCANCODE_CLI = 'code_license_' + SCANCODE_CLI


class CompositionScancodeCli(Composer):
    """Analyzer Composition for Scancode cli security vulnerabilities."""

    version = '0.1.0'

    def get_composition(self):
        return [ScanCode(cli=True)]

    def get_category(self):
        return CATEGORY_COLIC_SCANCODE_CLI

    def get_kind(self):
        return SCANCODE_CLI

    def merge_results(self, results):
        return results[0]
