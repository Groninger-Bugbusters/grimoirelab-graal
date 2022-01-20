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


# class BanditAnalyzer:

#     def __init__(self, details=False):
#         self.details = details
#         self.bandit = Bandit()

#     def analyze(self, folder_path):
#         """Analyze the content of a folder using Bandit

#         :param folder_path: folder path

#         :returns a dict containing the results of the analysis, like the one below
#         {
#           'code_quality': ..,
#           'modules': [..]
#         }
#         """
#         kwargs = {
#             'folder_path': folder_path,
#             'details': self.details
#         }
#         analysis = self.bandit.analyze(**kwargs)

#         return analysis
