import unittest
from line_identifier import is_convenience_mapping_with_attributes
from line_identifier import is_convenience_mapping_without_attributes
from line_identifier import is_request_mapping


class LineIdentifierTestCase(unittest.TestCase):
    def test_is_convenience_mapping_with_attributes_true(self):
        line = '@PostMapping(value = "/item/select", produces = "application/json")'
        self.assertTrue(is_convenience_mapping_with_attributes(line))

    def test_is_convenience_mapping_with_attributes_false(self):
        line = '@PostMapping("/item/select")'
        self.assertFalse(is_convenience_mapping_with_attributes(line))

    def test_is_convenience_mapping_without_attributes_true(self):
        line = '@PostMapping("/item/select")'
        self.assertTrue(is_convenience_mapping_without_attributes(line))

    def test_is_request_mapping_true(self):
        line = '@RequestMapping("/api/dosomestuff")'
        self.assertTrue(is_request_mapping(line))

    def test_is_request_mapping_false(self):
        line = '"/api/dosomestuff"'
        self.assertFalse(is_request_mapping(line))


if __name__ == '__main__':
    unittest.main()
