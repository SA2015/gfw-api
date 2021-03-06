"""A wrapper for strings."""



import apifunction
import computedobject
import ee_exception

# Using lowercase function naming to match the JavaScript names.
# pylint: disable=g-bad-name


class String(computedobject.ComputedObject):
  """An object to represent strings."""

  _initialized = False

  def __init__(self, string):
    """Construct a string wrapper.

    This constuctor accepts the following args:
      1) A bare string.
      2) A ComputedObject returning a string.

    Args:
      string: The string to wrap.
    """
    self.initialize()

    if isinstance(string, basestring):
      super(String, self).__init__(None, None)
    elif isinstance(string, computedobject.ComputedObject):
      super(String, self).__init__(string.func, string.args)
    else:
      raise ee_exception.EEException(
          'Invalid argument specified for ee.String(): %s' % string)
    self._string = string

  @classmethod
  def initialize(cls):
    """Imports API functions to this class."""
    if not cls._initialized:
      apifunction.ApiFunction.importApi(cls, 'String', 'String')
      cls._initialized = True

  @classmethod
  def reset(cls):
    """Removes imported API functions from this class."""
    apifunction.ApiFunction.clearApi(cls)
    cls._initialized = False

  @staticmethod
  def name():
    return 'String'

  def encode(self, opt_encoder=None):
    if isinstance(self._string, basestring):
      return self._string
    else:
      return self._string.encode(opt_encoder)
