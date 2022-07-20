#######################################
# RUNTIME RESULT
#######################################


class RTResult:
    def __init__(self):
        """
        This is the runtime result. This class checks if there are any errors, or successes.
        """
        self.reset()

    def reset(self):
        """
        Reset all variables
        :return: nothing
        """
        self.value = None
        self.error = None
        self.func_return_value = None
        self.loop_should_continue = False
        self.loop_should_break = False
        self.should_exit = False

    def register(self, res):
        """
        Register the result
        :param res: Result
        :return: Result value
        """
        self.error = res.error
        self.func_return_value = res.func_return_value
        self.loop_should_continue = res.loop_should_continue
        self.loop_should_break = res.loop_should_break
        self.should_exit = res.should_exit
        return res.value

    def success(self, value):
        """
        Register the success
        :param value: Value
        :return: Runtime result
        """
        self.reset()
        self.value = value
        return self

    def success_return(self, value):
        """
        Register the success and save return
        :param value: Value
        :return: Runtime result
        """
        self.reset()
        self.func_return_value = value
        return self

    def success_continue(self):
        """
        Register the success and save continue
        :return: Runtime result
        """
        self.reset()
        self.loop_should_continue = True
        return self

    def success_break(self):
        """
        Register the success and save break
        :return: Runtime result
        """
        self.reset()
        self.loop_should_break = True
        return self

    def success_exit(self, exit_value):
        """
        Register the success and save exit
        :return: Runtime result
        """
        self.reset()
        self.should_exit = True
        self.value = exit_value
        return self

    def failure(self, error):
        """
        Register the failure and save the error
        :param error: Error
        :return: Runtime result
        """
        self.reset()
        self.error = error
        return self

    def should_return(self):
        """
        Returns whether the function from which this method was called should return.
        :return: True or False
        """
        return (
            self.error
            or self.func_return_value
            or self.loop_should_continue
            or self.loop_should_break
            or self.should_exit
        )
