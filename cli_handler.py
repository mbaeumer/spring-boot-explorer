#!/usr/bin/python
import os
import re
from cli_validation_result import ValidationResult


class CliHandler:
  def __init__(self, argv):
    self.cliparams = argv
    self.title = ""
    self.targetFilename = ""

  def matchesFormat(self):
    return re.match(r'^...', self.targetFilename)

  def isValidArgs(self):
    if len(self.cliparams) != 2:
      return ValidationResult.NOT_ENOUGH_ARGS
    elif str(self.cliparams[1]).endswith("/src/main/java"):
      return ValidationResult.NOT_ROOT_FOLDER
    elif not os.path.isdir(str(self.cliparams[1])):
      return ValidationResult.NO_DIRECTORY


    return ValidationResult.OK
