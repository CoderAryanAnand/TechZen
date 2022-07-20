from TechZen.types.value_ import Value
from TechZen.errors_ import RTError


class Dict(Value):
    def __init__(self, elements):
        """
        Dictionary type. Inherits from Value class.
        :param elements: Elements of the dictionary
        """
        super().__init__()
        self.elements = elements

    def added_to(self, other):
        """
        Add more elements to the dictionary.
        :param other: Dictionary to be added
        :return: Updated dictionary
        """
        new_dict = self.copy()
        new_dict.elements.update(other.elements)
        return new_dict, None

    def subbed_by(self, other):
        """
        Remove element from dictionary
        :param other: Key to be removed
        :return: Updated dictionary
        """
        new_dict = self.copy()
        try:
            for i in range(len(list(self.elements.keys()))):
                if list(self.elements.keys())[i].value == other.value:
                    new_dict.elements.pop(list(self.elements.keys())[i])
                    return new_dict, None
        except KeyError:
            return (
                None,
                RTError(
                    other.pos_start, other.pos_end, "Key does not exist", self.context
                ),
            )

    def dived_by(self, other):
        """
        Get value belonging to key from dictionary
        :param other: Key
        :return: Value
        """
        try:
            for i in range(len(list(self.elements.keys()))):
                if list(self.elements.keys())[i].value == other.value:
                    return self.elements.get(list(self.elements.keys())[i]), None
        except KeyError:
            return (
                None,
                RTError(
                    other.pos_start, other.pos_end, "Key does not exist", self.context
                ),
            )

    def copy(self):
        """
        Return a copy of the dictionary
        :return: Copy
        """
        copy = Dict(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        keys, values = list(self.elements.keys()), list(self.elements.values())
        try:
            list_ = [f"{key}: {value}" for key, value in zip(keys, values)]
            return_dict = ", ".join([str(x) for x in list_])
            return f"{{{return_dict}}}"
        except ValueError:
            try:
                return f"{{{keys[0]}: {values[0]}}}"
            except ValueError:
                return "{}"
