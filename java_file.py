from bean_type import BeanType

def _extract_class_name(file_name):
    last_slash_index = file_name.rfind("/")
    file_with_extension = file_name[last_slash_index + 1:len(file_name)]
    last_dot_index = file_with_extension.rfind(".")
    class_name = file_with_extension[0:last_dot_index]
    return class_name

    
def _extract_module_name(root_path, file_name):
    length = len(root_path)
    index_source_path = file_name.find("/src/main")
    module_name = file_name[length + 1:index_source_path]
    return "src" if len(module_name) == 0 else module_name

def _extract_file_content(file_name):
    lines = []
    try:
        with open(file_name, 'r') as file:
            for line in file:
                lines.append(line)
    except FileNotFoundError as e:
        print("File could not be found")
    return lines
    
class JavaFile:
    def __init__(self, name, path, module, content):
        self.class_name = name
        self.path = path
        self.module = module
        self.content = content
        self.stripped_content = []

        self.package = None
        self.bean_type = None
        self.imports = []
        
    
    @classmethod
    def from_file_name(cls, root_path: str, file_name: str):
        # identify bean type
        # set path
        # set class name
        # set package
        class_name = _extract_class_name(file_name)
        module_name = _extract_module_name(root_path, file_name)
        content = _extract_file_content(file_name)
        java_file = cls(class_name, file_name, module_name, content)
        java_file.preprocess()
        return java_file

    def preprocess(self):
        for line in self.content:
            self.stripped_content.append(line.strip())
        self.package = self.read_package_name(self.content[0])
        self.bean_type = self.get_bean_type()
        self.imports = self.get_imports()
    
    def read_package_name(self, s) -> str:
        return s.split(maxsplit=1)[1] if " " in s else ""
    
    def get_bean_type(self):
        bean_type = BeanType.NONE
        for line in self.stripped_content:
            if "@RestController" in line:
                bean_type = BeanType.CONTROLLER
            elif "@Service" in line:
                bean_type = BeanType.SERVICE
            elif "@Component" in line:
                bean_type = BeanType.COMPONENT
            elif "@Configuration" in line:
                bean_type = BeanType.CONFIGURATION
            elif "@Repository" in line:
                bean_type = BeanType.REPOSITORY
        return bean_type
    
    def get_imports(self):
        imports = []
        for line in self.stripped_content:
            if "import " in line:
                imports.append(line)
            
        return imports
        


