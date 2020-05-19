from abc import ABC
import abc


class BaseRouter(ABC):
    def __init__(self, user, command, args=[]):
        self.user = user
        self.command = command
        self.args = args

    @abc.abstractmethod
    def route(self):
        """Take a Command and route to appropriate code"""