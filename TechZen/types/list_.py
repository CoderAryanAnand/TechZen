from TechZen.types.value_ import Value
from TechZen.types.number_ import Number
from TechZen.errors_ import RTError


class List(Value):
    def __init__(self, elements):
        """
        List type. Inherits from Value class.
        :param elements:
        """
        super().__init__()
        self.elements = elements

    def added_to(self, other):
        """
        Add element to list.
        :param other: Element
        :return: Updated list
        """
        new_list = self.copy()
        new_list.elements.append(other)
        return new_list, None

    def multed_by(self, other):
        """
        Merge two lists.
        :param other: Other list
        :return: Updated list
        """
        if not isinstance(other, List):
            return None, Value.illegal_operation(self, other)
        new_list = self.copy()
        new_list.elements.extend(other.elements)
        return new_list, None

    def subbed_by(self, other):
        """
        Remove element from list.
        :param other: Element index
        :return: Updated list
        """
        if not isinstance(other, Number):
            return None, Value.illegal_operation(self, other)
        new_list = self.copy()
        try:
            new_list.elements.pop(other.value)
            return new_list, None
        except IndexError:
            return (
                None,
                RTError(
                    other.pos_start,
                    other.pos_end,
                    "Element at this index could not be removed from"
                    "list, because index is out of bounds",
                    self.context,
                ),
            )

    def dived_by(self, other):
        """
        Get element from list
        :param other: Index
        :return: Element
        """
        if not isinstance(other, Number):
            return None, Value.illegal_operation(self, other)
        try:
            return self.elements[other.value], None
        except IndexError:
            return (
                None,
                RTError(
                    other.pos_start,
                    other.pos_end,
                    "Element at this index could not be retrieved from"
                    "list, because index is out of bounds",
                    self.context,
                ),
            )

    def copy(self):
        """
        Make a copy of the list.
        :return: Copy
        """
        copy = List(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return ", ".join([str(x) for x in self.elements])

    def __repr__(self):
        return f'[{", ".join([str(x) for x in self.elements])}]'
