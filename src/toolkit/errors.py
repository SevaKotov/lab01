class ToolkitError(Exception):
    pass

class MissingOperandError(ToolkitError):
    pass


class UnbalancedParenthesesError(ToolkitError):
    pass

class EmptyExpressionError(ToolkitError):
    pass


class InvalidCharacterError(ToolkitError):
    pass

class ConsecutiveOperatorsError(ToolkitError):
    pass


class DivisionByZeroError(ToolkitError):
    pass


class UnknownUnitError(ToolkitError):
    pass


class IncompatibleUnitsError(ToolkitError):
    pass


class InvalidNumberError(ToolkitError):
    pass

class TemperatureBelongZero(ToolkitError):
    pass