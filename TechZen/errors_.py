from TechZen.strings_with_arrows import string_with_arrows


class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        """
        Parent class for an error.
        :param pos_start: Where the error in the code starts
        :param pos_end: Where the error in the code ends
        :param error_name: What type of error it is
        :param details: Details of the error
        """
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        """
        Printing the error as a string
        :return: The type of error, the details of the error, in which file and line it occurred
        """
        result = f"{self.error_name}: {self.details}\n"
        result += f"File {self.pos_start.fn}, line {self.pos_start.ln + 1}"
        result += "\n\n" + string_with_arrows(
            self.pos_start.ftxt, self.pos_start, self.pos_end
        )
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        """
        An illegal character error.
        :param pos_start: Where the error in the code starts
        :param pos_end: Where the error in the code ends
        :param details: Details of the error
        """
        super().__init__(pos_start, pos_end, "Illegal Character", details)


class ExpectedCharError(Error):
    """
    An expected character error. When a character is not the expected one.
    :param pos_start: Where the error in the code starts
    :param pos_end: Where the error in the code ends
    :param details: Details of the error
    """
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Expected Character", details)


class InvalidSyntaxError(Error):
    """
    An invalid syntax error.
    :param pos_start: Where the error in the code starts
    :param pos_end: Where the error in the code ends
    :param details: Details of the error
    """
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Invalid Syntax", details)


class RTError(Error):
    """
    A runtime error.
    :param pos_start: Where the error in the code starts
    :param pos_end: Where the error in the code ends
    :param details: Details of the error
    """
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, "Runtime Error", details)
        self.context = context

    def as_string(self):
        """
        Printing the error as a string
        :return: The type of error, the details of the error, in which file and line it occurred
        """
        result = self.generate_traceback()
        result += f"{self.error_name}: {self.details}"
        result += "\n\n" + string_with_arrows(
            self.pos_start.ftxt, self.pos_start, self.pos_end
        )
        return result

    def generate_traceback(self):
        """
        This function generates a traceback for the error.
        :return: Traceback for the error, all parent files and functions
        """
        result = ""
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result = (
                f"  File {pos.fn}, line {pos.ln + 1}, in {ctx.display_name}\n" + result
            )

            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return "Traceback (most recent call last):\n" + result
