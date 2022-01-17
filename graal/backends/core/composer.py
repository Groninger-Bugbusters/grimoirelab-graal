class Composer:
    """Template class for composition of analyzers"""

    def get_kind(self):
        """Returns more readable name of this composition"""

        raise NotImplementedError

    def get_category(self):
        """Returns the category of this composition"""

        raise NotImplementedError

    def get_composition(self):
        """Returns the corresponding composition"""

        raise NotImplementedError

    def merge_results(self, results):
        """Merges the results of the composition's analyzers"""

        raise NotImplementedError
