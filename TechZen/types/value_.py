from TechZen.runtime_ import RTResult
from TechZen.errors_ import RTError


class Value:
    def __init__(self):
        """
        This is the value base class. All other types use this class as a parent.
        """
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        """
        Set position of the class.
        :param pos_start: Start position
        :param pos_end: End position
        :return: Class (self)
        """
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        """
        Set context of the class.
        :param context: Context
        :return: Class (self)
        """
        self.context = context
        return self

    def added_to(self, other):
        """
        Function for when there is an addition sign after the class.
        :param other: Class / value after the sign
        :return: Illegal operation error
        """
        return None, self.illegal_operation(other)

    def subbed_by(self, other):
        """
        Function for when there is a subtraction sign after the class.
        :param other: Class / value after the sign
        :return: Illegal operation error
        """
        return None, self.illegal_operation(other)

    def multed_by(self, other):
        """
        Function for when there is a multiplication sign after the class.
        :param other: Class / value after the sign
        :return: Illegal operation error
        """
        return None, self.illegal_operation(other)

    def dived_by(self, other):
        """
        Function for when there is a division sign after the class.
        :param other: Class / value after the sign
        :return: Illegal operation error
        """
        return None, self.illegal_operation(other)

    def pow_of(self, other):
        """
        Function for when there is a power sign after the class.
        :param other: Class / value after the sign
        :return: Illegal operation error
        """
        return None, self.illegal_operation(other)

    def floor_of(self, other):
        """
        Function for when there is a floor sign after the class.
        :param other: Class / value after the sign
        :return: Illegal operation error
        """
        return None, self.illegal_operation(other)

    def mod_by(self, other):
        """
        Function for when there is a modulo sign after the class.
        :param other: Class / value after the sign
        :return: Illegal operation error
        """
        return None, self.illegal_operation(other)

    def get_comparison_eq(self, other):
        """
        Function for when there is an equal to sign after the class.
        :param other: Class / value after the sign
        :return: Illegal operation error
        """
        return None, self.illegal_operation(other)

    def get_comparison_ne(self, other):
        """
        Function for when there is a not equal to sign after the class.
        :param other: Class / value after the sign
        :return: Illegal operation error
        """
        return None, self.illegal_operation(other)

    def get_comparison_lt(self, other):
        """
        Function for when there is a less than sign after the class.
        :param other: Class / value after the sign
        :return: Illegal operation error
        """
        return None, self.illegal_operation(other)

    def get_comparison_gt(self, other):
        """
        Function for when there is a greater than sign after the class.
        :param other: Class / value after the sign
        :return: Illegal operation error
        """
        return None, self.illegal_operation(other)

    def get_comparison_lte(self, other):
        """
        Function for when there is a less than or equal to sign after the class.
        :param other: Class / value after the sign
        :return: Illegal operation error
        """
        return None, self.illegal_operation(other)

    def get_comparison_gte(self, other):
        """
        Function for when there is a greater than or equal to sign after the class.
        :param other: Class / value after the sign
        :return: Illegal operation error
        """
        return None, self.illegal_operation(other)

    def anded_by(self, other):
        """
        Function for when there is an and keyword after the class.
        :param other: Class / value after the keyword
        :return: Illegal operation error
        """
        return None, self.illegal_operation(other)

    def ored_by(self, other):
        """
        Function for when there is an or keyword after the class.
        :param other: Class / value after the keyword
        :return: Illegal operation error
        """
        return None, self.illegal_operation(other)

    def notted(self):
        """
        Function for when there is a not sign in front of it
        :return: Illegal operation error
        """
        return None, self.illegal_operation()

    def execute(self, args):
        """
        Execute a function, for most classes this doesn't exist, so as a base it returns an error.
        :param args: Arguments in the function
        :return: Error
        """
        return RTResult().failure(self.illegal_operation())

    def copy(self):
        """
        Copy the class
        :return: Error
        """
        raise Exception("No copy method defined")

    @staticmethod
    def is_true():
        """
        Find if self is true or not.
        :return: False
        """
        return False

    def illegal_operation(self, other=None):
        """
        The illegal operation error.
        :param other: The value after the sign / keyword.
        :return: Illegal operation error
        """
        if not other:
            other = self
        return RTError(self.pos_start, other.pos_end, "Illegal operation", self.context)
