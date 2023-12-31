def is_convenience_mapping_with_attributes(line):
    return (
                       "@GetMapping" in line or "@PostMapping" in line or "@PutMapping" in line or "@DeleteMapping") and "value" in line


def is_convenience_mapping_without_attributes(line):
    return (
                       "@GetMapping" in line or "@PostMapping" in line or "@PutMapping" in line or "@DeleteMapping") and "value" not in line and "produces" not in line


def is_request_mapping(line):
    return "@RequestMapping(" in line
