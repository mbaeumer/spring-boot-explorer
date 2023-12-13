from enum import Enum

class BeanType(Enum):
  CONTROLLER = 1
  SERVICE = 2
  COMPONENT = 3
  CONFIGURATION = 4
  NONE = 5