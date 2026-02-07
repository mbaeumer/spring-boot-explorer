from enum import Enum

class BeanType(Enum):
  CONTROLLER = 1
  SERVICE = 2
  COMPONENT = 3
  CONFIGURATION = 4
  REPOSITORY = 5
  ENTITY = 6
  NONE = 7