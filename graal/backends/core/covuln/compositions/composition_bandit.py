from graal.backends.core.analyzers.bandit import Bandit
from graal.backends.core.composer import Composer


BANDIT = 'bandit'
CATEGORY_COVULN = "code_vulnerabilities"


class CompositionBandit(Composer):
    """Analyzer Composition for Bandit security vulnerabilities."""

    version = '0.1.0'

    def get_composition(self):
        return [Bandit()]

    def get_category(self):
        return CATEGORY_COVULN

    def get_kind(self):
        return BANDIT

    def merge_results(self, results):
        return results[0]
