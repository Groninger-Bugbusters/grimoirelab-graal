from graal.backends.core.analyzers.scancode import ScanCode
from graal.backends.core.composer import Composer


SCANCODE = 'scancode'
CATEGORY_COLIC_SCANCODE = 'code_license_' + SCANCODE


class CompositionScancode(Composer):
    """Analyzer Composition for Scancode security vulnerabilities."""

    version = '0.1.0'

    def get_composition(self):
        return [ScanCode()]

    def get_category(self):
        return CATEGORY_COLIC_SCANCODE

    def get_kind(self):
        return SCANCODE

    def merge_results(self, results):
        return results[0]
