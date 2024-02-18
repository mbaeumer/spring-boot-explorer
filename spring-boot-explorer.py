import glob
from bean_type import BeanType
from endpoint import Endpoint
import sys
import os
from cli_handler import CliHandler
from cli_validation_result import ValidationResult
from line_extractor import extract_url
from line_extractor import extract_class_name
from csv_writer import write_csv_file


# find all Java files
# find all RestControllers, Service, Component
# find all endpoints


def handle_cli_args(argv):
    cli = CliHandler(argv)
    if cli.isValidArgs() == ValidationResult.NOT_ENOUGH_ARGS:
        print("ERROR: Please provide a valid argument")
        raise RuntimeError
    elif cli.isValidArgs() == ValidationResult.NO_DIRECTORY:
        print("ERROR: Please provide a path to a directory")
        raise RuntimeError
    elif cli.isValidArgs() == ValidationResult.NOT_ROOT_FOLDER:
        print("ERROR: The provided path is not the root of the project")
        raise RuntimeError


def show_menu(root_path):
    source_root = root_path + "/src/main/java"
    if has_modules(root_path):
        source_root = root_path
    menu_options = {
        1: 'List all beans',
        2: 'List all endpoints',
        3: 'Show bean count',
        4: 'Find all @PreAuthorize annotations',
        5: 'Exit'
    }

    while (True):
        print("Main menu")
        print("---------")
        for k in menu_options.keys():
            print(k, "-", menu_options[k])
        try:
            userinput = int(input("Enter your choice: "))
        except ValueError:
            print("Please enter a number")
            continue

        if userinput == 1:
            all_java_files = find_all_java_files(source_root)
            bean_mapping = find_beans(all_java_files)
            print_beans(bean_mapping)
        elif userinput == 2:
            all_java_files = find_all_java_files(source_root)
            bean_mapping = find_beans(all_java_files)
            endpoints = find_endpoints_per_controller(bean_mapping)
            print_endpoints(endpoints)
            export = ask_for_csv_export()
            if export == 'y':
                write_csv_file(endpoints)
        elif userinput == 3:
            all_java_files = find_all_java_files(source_root)
            bean_mapping = find_beans(all_java_files)
            get_bean_counts(bean_mapping)
        elif userinput == 4:
            all_java_files = find_all_java_files(source_root)
            bean_mapping = find_beans(all_java_files)
            print_preauthorize_annotations(bean_mapping)
        elif userinput == 5:
            exit(0)
        else:
            print("Please choose a valid number!")


def has_modules(root_path):
    return os.path.isdir(root_path + "/application") and os.path.isdir(root_path + "/business")


def find_all_java_files(base_dir):
    java_files = []
    files = glob.glob(base_dir + '/**/*.java', recursive=True)
    for file in files:
        java_files.append(file)
    return java_files


def get_bean_type(filename):
    bean_type = BeanType.NONE
    try:
        with open(filename, 'r') as file:
            for line in file:
                if "@RestController" in line:
                    bean_type = BeanType.CONTROLLER
                elif "@Service" in line:
                    bean_type = BeanType.SERVICE
                elif "@Component" in line:
                    bean_type = BeanType.COMPONENT
                elif "@Configuration" in line:
                    bean_type = BeanType.CONFIGURATION
    except FileNotFoundError as e:
        print("File could not be found")
    return bean_type


def find_beans(java_files):
    bean_type_dict = {}
    for file in java_files:
        bean_type_dict[file] = get_bean_type(file)
    return bean_type_dict


def print_beans(bean_mapping):
    for k, v in bean_mapping.items():
        print(k + "-" + str(v))


def get_file_content(filename):
    lines = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                lines.append(line)
    except FileNotFoundError as e:
        print("File could not be found")
    return lines


def find_endpoints_per_controller(bean_mapping):
    endpoints = []
    rest_controllers = find_beans_by_type(bean_mapping, BeanType.CONTROLLER)

    for rest_controller in rest_controllers:
        lines = get_file_content(rest_controller)
        base_url = find_base_url(lines)
        endpoints.extend(find_endpoints(lines, base_url, rest_controller))

    return endpoints


def print_preauthorize_annotations(bean_mapping):
    preauthorizes = find_all_preauthorize(bean_mapping)
    for pre in preauthorizes:
        print(pre)


def find_all_preauthorize(bean_mapping):
    preauthorizes = []
    rest_controllers = find_beans_by_type(bean_mapping, BeanType.CONTROLLER)

    for rest_controller in rest_controllers:
        lines = get_file_content(rest_controller)
        preauthorizes.extend(find_preauthorize_in_controller(lines, rest_controller))

    return preauthorizes


def find_preauthorize_in_controller(lines, restcontroller):
    preauthorize = []
    for line in lines:
        if line.find("@PreAuthorize") > 0:
            preauthorize.append(line)
    return preauthorize


def find_base_url(lines):
    base_url = ""
    line_with_requestmapping = ""
    for line in lines:
        if "@RequestMapping" in line:
            line_with_requestmapping = line
            break
    if len(line_with_requestmapping) > 0:
        start_index = int(line_with_requestmapping.find("(") + 2)
        end_index = int(line_with_requestmapping.find(")") - 1)
        base_url = line_with_requestmapping[start_index:end_index]
    return base_url


def find_endpoints(lines, base_url, rest_controller):
    endpoints = []
    for line in lines:
        if contains_mapping(line):
            http_method = extract_http_method(line)
            url = base_url + extract_url(line)
            endpoints.append(Endpoint(http_method, url, extract_class_name(rest_controller)))
    return endpoints


def contains_mapping(line):
    return "@GetMapping" in line or "@PostMapping" in line or "@PutMapping" in line or "@DeleteMapping" in line


def extract_http_method(line):
    http_method = ""
    if "@GetMapping" in line:
        http_method = "GET"
    elif "@PostMapping" in line:
        http_method = "POST"
    elif "@PutMapping" in line:
        http_method = "PUT"
    elif "@DeleteMapping" in line:
        http_method = "DELETE"

    return http_method


def find_beans_by_type(bean_mapping, bean_type):
    filenames = []
    for k, v in bean_mapping.items():
        if v == bean_type:
            filenames.append(k)
    return filenames


def print_endpoints(mapping):
    for e in mapping:
        e.display_endpoint()

def ask_for_csv_export():
    user_input = ''
    choices = ['y', 'n']
    print("")
    while user_input not in choices:
        user_input = input("Want to export? (y/n)")

    return user_input


def get_bean_counts(bean_mapping):
    controller_counter = 0
    service_counter = 0
    component_counter = 0
    configuration_counter = 0
    for k, v in bean_mapping.items():
        if bean_mapping[k] == BeanType.CONTROLLER:
            controller_counter = controller_counter + 1
        elif bean_mapping[k] == BeanType.SERVICE:
            service_counter = service_counter + 1
        elif bean_mapping[k] == BeanType.COMPONENT:
            component_counter = component_counter + 1
        elif bean_mapping[k] == BeanType.CONFIGURATION:
            configuration_counter = configuration_counter + 1

    print("Bean counts")
    print("Number of controllers: \t %d" % (controller_counter))
    print("Number of services: \t %d" % (service_counter))
    print("Number of components: \t %d" % (component_counter))
    print("Number of configuration: \t %d" % (configuration_counter))


if __name__ == '__main__':
    try:
        handle_cli_args(sys.argv)
        root_path = sys.argv[1]
        print("parameter: " + root_path)
        show_menu(root_path)
    except RuntimeError:
        print("End of story")
