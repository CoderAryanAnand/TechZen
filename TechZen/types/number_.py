from TechZen.types.value_ import Value
from TechZen.errors_ import RTError


class Number(Value):
    def __init__(self, value):
        """
        Number type. Inherits from Value class.
        :param value: Value
        """
        super().__init__()
        self.value = value

    def added_to(self, other):
        """
        Add two numbers.
        :param other: Number
        :return: Sum
        """
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def subbed_by(self, other):
        """
        Subtract two numbers.
        :param other: Number
        :return: Difference
        """
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        """
        Multiply two numbers.
        :param other: Number
        :return: Product
        """
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def dived_by(self, other):
        """
        Divide two numbers.
        :param other: Number
        :return: Quotient
        """
        if not isinstance(other, Number):
            return None, Value.illegal_operation(self, other)
        if other.value == 0:
            return (
                None,
                RTError(
                    other.pos_start, other.pos_end, "Division by zero", self.context
                ),
            )

        return Number(self.value / other.value).set_context(self.context), None

    def floor_of(self, other):
        """
        Floor divide two numbers.
        :param other: Number
        :return: Quotient
        """
        if not isinstance(other, Number):
            return None, Value.illegal_operation(self, other)
        if other.value == 0:
            return (
                None,
                RTError(
                    other.pos_start, other.pos_end, "Division by zero", self.context
                ),
            )

        return Number(self.value // other.value).set_context(self.context), None

    def pow_of(self, other):
        """
        Exponent two numbers.
        :param other: Number
        :return: Product
        """
        if isinstance(other, Number):
            return Number(self.value**other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def mod_by(self, other):
        """
        Modulo two numbers.
        :param other: Number
        :return: Number
        """
        if isinstance(other, Number):
            return Number(self.value % other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_eq(self, other):
        """
        Decide whether two numbers are equal.
        :param other: Number
        :return: Boolean
        """
        if isinstance(other, Number):
            return (
                Number(int(self.value == other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_ne(self, other):
        """
        Decide whether two numbers are not equal.
        :param other: Number
        :return: Boolean
        """
        if isinstance(other, Number):
            return (
                Number(int(self.value != other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lt(self, other):
        """
        Decide whether two numbers are less than to each other.
        :param other: Number
        :return: Boolean
        """
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gt(self, other):
        """
        Decide whether two numbers are greater than to each other.
        :param other: Number
        :return: Boolean
        """
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lte(self, other):
        """
        Decide whether two numbers are less than or equal to each other.
        :param other: Number
        :return: Boolean
        """
        if isinstance(other, Number):
            return (
                Number(int(self.value <= other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gte(self, other):
        """
        Decide whether two numbers are greater than or equal to each other.
        :param other: Number
        :return: Boolean
        """
        if isinstance(other, Number):
            return (
                Number(int(self.value >= other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def anded_by(self, other):
        """
        Decide whether two numbers are true.
        :param other: Number
        :return: Boolean
        """
        if isinstance(other, Number):
            return (
                Number(int(self.value and other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def ored_by(self, other):
        """
        Decide whether one of the two numbers are true.
        :param other: Number
        :return: Boolean
        """
        if isinstance(other, Number):
            return (
                Number(int(self.value or other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def notted(self):
        """
        Return the opposite of the number
        :return: Boolean
        """
        return Number(1 if self.value == 0 else 0).set_context(self.context), None

    def copy(self):
        """
        Make a copy of the number.
        :return: Copy
        """
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        """
        Is the number true?
        :return: Boolean
        """
        return self.value != 0

    def __repr__(self):
        return str(self.value)


Number.null = Number(0)
Number.false = Number(0)
Number.true = Number(1)
