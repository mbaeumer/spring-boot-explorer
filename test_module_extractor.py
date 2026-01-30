import unittest
from module_extractor import extract_unique_module_names

class ModuleExtractorTestCase(unittest.TestCase):
    def test_extract_unique_module_names(self):
        paths = [
            "/data/projects/app1/src/main.py",
            "/data/projects/app1/README.md",
            "/data/projects/app2/config.yaml",
            "/data/projects/app3/docs/index.md",
        ]
        root_path = "/data/projects"
        result = extract_unique_module_names(paths, root_path)
        self.assertEqual(len(result), 3)
        
if __name__ == '__main__':
    unittest.main()