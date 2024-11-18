import unittest
from functions import research
class TestGlobalFunctionality(unittest.TestCase):

    def test_program_execution(self):
        try:
            # on appelle la fonction principale
            result = research("test", 5, source="Reddit", lang="Anglais")
            self.assertEqual(result, (True, 'success'))
        except Exception as e:
            # on capture toutes les exceptions possibles lors de l'exécution
            self.fail(f"Unexpected exception: {e}")

if __name__ == '__main__':
    unittest.main()
