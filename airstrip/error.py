# -*- coding: utf8 -*-

class Generic(Exception):
  """Base class for exceptions in airstrip."""

  def __init__(self, etype, message):
    if not etype in globals():
      etype = UNSPECIFIED
    self.type = etype
    self.message = message

UNSPECIFIED = "UNSPECIFIED"
UNIMPLEMENTED = "UNIMPLEMENTED"
WRONG_ARGUMENT = "WRONG_ARGUMENT"
MISSING = "MISSING"
BROKEN = "BROKEN"


class Http(Generic):
  """Exception raised for errors in the http submodule.

  Attributes:
      type -- error type
      msg  -- explanation of the error
  """
  def __init__(self, etype, message):
    super(Generic, self).__init__(etype, message)

class License(Generic):
  """Exception raised for errors in license handling.

  Attributes:
      type -- error type
      msg  -- explanation of the error
  """
  def __init__(self, etype, message):
    super(Generic, self).__init__(etype, message)

class AirRC(Generic):
  """Exception raised for errors in the rc submodule.

  Attributes:
      type -- error type
      msg  -- explanation of the error
  """
  def __init__(self, etype, message):
    super(Generic, self).__init__(etype, message)


class GitHub(Generic):
  """Exception raised for errors in the GitHub connector.

  Attributes:
      type -- error type
      msg  -- explanation of the error
  """
  def __init__(self, etype, message):
    super(Generic, self).__init__(etype, message)


TERRIBLE = "TERRIBLE"
GIT_ERROR = "GIT_ERROR"

class Git(Generic):
  """Exception raised for errors in the git submodule.

  Attributes:
      type -- error type
      msg  -- explanation of the error
  """
  def __init__(self, etype, message):
    super(Generic, self).__init__(etype, message)


