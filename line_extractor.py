from line_identifier import is_convenience_mapping_with_attributes
from line_identifier import is_convenience_mapping_without_attributes


def extract_url(line):
    if is_convenience_mapping_without_attributes(line):
        url = ""
        if line.find("(") > 0:
            start_index = int(line.find("(") + 2)
            end_index = int(line.find(")") - 1)
            url = line[start_index:end_index]
        return url
    elif is_convenience_mapping_with_attributes(line):
        value_index = line.find("value = ")
        if value_index == 0:
            return ""
        produces_index = line.find("produces = ")
        end_index = line.find("\")")
        if produces_index > value_index:
            end_index = line.find("\",")
        url = line[value_index + 9:end_index]
        return url

    return ""

def extract_class_name(full_name):
    splitted = full_name.split("/")
    file_name = splitted[len(splitted) - 1]
    class_name = file_name[0:file_name.find(".java")]
    return class_name



