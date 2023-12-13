#!/usr/bin/python
from enum import Enum

class ValidationResult(Enum):
  OK = 1
  NOT_ENOUGH_ARGS = 2
  NOT_ROOT_FOLDER = 3
  NO_DIRECTORY = 4

