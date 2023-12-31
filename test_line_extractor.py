import unittest
from line_extractor import extract_url
from line_extractor import extract_class_name


class LineExtractorTestCase(unittest.TestCase):
    def test_extract_url_without_attributes(self):
        line = '@PostMapping("/item/select")'
        self.assertEqual(extract_url(line), "/item/select")

    def test_extract_url_with_one_attribute(self):
        line = '@PostMapping(value = "/item/select")'
        self.assertEqual(extract_url(line), "/item/select")

    def test_extract_url_with_two_attributes(self):
        line = '@PostMapping(value = "/item/select", produces = "application/text")'
        self.assertEqual(extract_url(line), "/item/select")

    def test_extract_url_without_value_attribute(self):
        line = '@GetMapping(produces = "application/json")'
        self.assertEqual(extract_url(line), "")

    def test_extract_class_name(self):
        line = 'src/jada/TestController.java'
        self.assertEqual(extract_class_name(line), "TestController")

