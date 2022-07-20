from TechZen.types.value_ import Value
from TechZen.types.number_ import Number


class String(Value):
    def __init__(self, value):
        """
        String type. Inherits from Value class.
        :param value: String
        """
        super().__init__()
        self.value = value

    def added_to(self, other):
        """
        Concatenate two strings.
        :param other: String
        :return: Updated string
        """
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        """
        Multiply a string.
        :param other: Number
        :return: Updated string
        """
        if isinstance(other, Number):
            return String(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_eq(self, other):
        """
        Compare two strings for the equal to comparison.
        :param other: String
        :return: Boolean
        """
        if isinstance(other, String):
            return (
                Number(int(self.value == other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_ne(self, other):
        """
        Compare two strings for the not equal to comparison.
        :param other: String
        :return: Boolean
        """
        if isinstance(other, String):
            return (
                Number(int(self.value != other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def is_true(self):
        """
        Decide whether the string contains any characters.
        :return: Boolean
        """
        return len(self.value) > 0

    def copy(self):
        """
        Make a copy of the string.
        :return: Copy
        """
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return self.value

    def __repr__(self):
        return f'"{self.value}"'
