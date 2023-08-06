# Copyright (c) Qotto, 2021

"""
Eventy configuration
"""

from eventy.messaging import Service

__all__ = [
    'SERVICE_DOMAIN',
    'SERVICE_NAME',
    'SERVICE',
]

SERVICE_NAME: str = '-'
"""
Do not update with:
>>> from eventy.config import SERVICE_NAME
>>> SERVICE_NAME = 'my_service'

If you want to update the value you need to do:
>>> from eventy import config
>>> config.SERVICE_NAME = 'my_service'
"""

SERVICE_DOMAIN: str = '-'
"""
Do not update with:
>>> from eventy.config import SERVICE_DOMAIN
>>> SERVICE_DOMAIN = 'my_domain'

If you want to update the value you need to do:
>>> from eventy import config
>>> config.SERVICE_DOMAIN = 'my_domain'
"""

SERVICE: Service
"""
Do not update with:
>>> from eventy.config import SERVICE
>>> SERVICE = my_service

If you want to update the value you need to do:
>>> from eventy import config
>>> config.SERVICE = my_service
"""
