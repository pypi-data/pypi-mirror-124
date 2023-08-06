from enum import Enum
from functools import wraps
from typing import Callable, Iterable

from eventy.messaging.store import Appender
from eventy.record import Record

__all__ = [
    'Guarantee',
    'Handler',
    'Agent',
    'handler',
]


class Guarantee(Enum):
    """
    Delivery guarantee for handlers
    """
    AT_LEAST_ONCE = 1
    AT_MOST_ONCE = 10
    EXACTLY_ONCE = 11


class Handler:
    """
    Record handler
    """

    def __init__(
        self,
        qualified_name: str,
        delivery_guarantee: Guarantee,
        function: Callable[[Record, Appender], None],
    ) -> None:
        self.qualified_name = qualified_name
        self.delivery_guarantee = delivery_guarantee
        self.function = function

    def __call__(self, record: Record, appender: Appender) -> None:
        self.function(record, appender)

    def __str__(self) -> str:
        return f'Handler of {self.qualified_name} with {self.delivery_guarantee} using {self.function}.'


class _AgentHandler:
    """
    Decorator for handler methods of an Agent
    """

    def __init__(
        self,
        schema: str,
        guarantee: Guarantee,
        method: Callable[['Agent', Record, Appender], None],
    ) -> None:
        self.schema = schema
        self.guarantee = guarantee
        self.method = method

    def __call__(self, agent_self, record: Record, appender: Appender):
        self.method(agent_self, record, appender)


class Agent:
    """
    An agent can define methods to handle records
    """

    def get_handlers(self) -> Iterable[Handler]:
        for attribute_name in self.__dir__():
            attribute = getattr(self, attribute_name)
            if isinstance(attribute, _AgentHandler):
                method = getattr(attribute, 'method')

                @wraps(method)
                def func(record: Record, appender: Appender):
                    method(self, record, appender)

                yield Handler(
                    qualified_name=attribute.schema,
                    delivery_guarantee=attribute.guarantee,
                    function=func,
                )


def handler(qualified_name: str, delivery_guarantee: Guarantee):
    """
    Decorator to create handlers from functions or agent methods
    """

    def decorator(func):
        if '.' in func.__qualname__:
            return _AgentHandler(
                schema=qualified_name,
                guarantee=delivery_guarantee,
                method=func,
            )
        else:
            return Handler(
                qualified_name=qualified_name,
                delivery_guarantee=delivery_guarantee,
                function=func,
            )

    return decorator
