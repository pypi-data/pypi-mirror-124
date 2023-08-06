# Copyright (c) Qotto, 2021

"""
Eventy messaging API

The messaging API itself is backend-agnostic, there is currently only a Kafka backend implemented.
"""
from eventy.messaging.agent import Handler, Agent, handler, Guarantee
from eventy.messaging.app import App
from eventy.messaging.errors import MessagingError
from eventy.messaging.service import Service
from eventy.messaging.store import Store, Appender, Cursor

__all__ = [
    # base
    'Service',
    # store
    'Store',
    'Appender',
    'Cursor',
    # agent
    'Agent',
    'Handler',
    'handler',
    'Guarantee',
    # app
    'App',
    # errors
    'MessagingError',
]
