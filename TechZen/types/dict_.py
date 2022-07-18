from TechZen.types.value_ import Value
from TechZen.errors_ import RTError


class Dict(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements

    def added_to(self, other):
        new_dict = self.copy()
        new_dict.elements.update(other.elements)
        return new_dict, None

    def subbed_by(self, other):
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
