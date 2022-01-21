from graal.backends.core.analyzers.nomos import Nomos
from graal.backends.core.composer import Composer


NOMOS = 'nomos'
CATEGORY_COLIC_NOMOS = 'code_license_' + NOMOS


class CompositionNomos(Composer):
    """Analyzer Composition for Nomos security vulnerabilities."""

    version = '0.1.0'

    def get_composition(self):
        return [Nomos()]

    def get_category(self):
        return CATEGORY_COLIC_NOMOS

    def get_kind(self):
        return NOMOS

    def merge_results(self, results):
        return results[0]
