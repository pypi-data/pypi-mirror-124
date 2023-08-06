__all__ = [
    'Service',
]

from typing import Optional


class Service:
    def __init__(
        self,
        service_name: str,
        service_domain: str,
        service_namespace: str,
        event_topic: str,
        request_topic: str,
        response_topic: str,
    ):
        self._service_name = service_name
        self._service_domain = service_domain
        self._service_namespace = service_namespace
        self._event_topic = event_topic
        self._request_topic = request_topic
        self._response_topic = response_topic

    def get_qualified_name(self, record_name: str) -> str:
        return f'{self.namespace}:{record_name}'

    @property
    def event_topic(self) -> str:
        return self._event_topic

    @property
    def request_topic(self) -> str:
        return self._request_topic

    @property
    def response_topic(self) -> str:
        return self._response_topic

    @property
    def namespace(self) -> str:
        return self._service_namespace

    @property
    def name(self) -> str:
        return self._service_name

    @property
    def domain(self) -> str:
        return self._service_domain

    def __hash__(self):
        return hash((self.domain, self.name))

    def __eq__(self, other) -> bool:
        return (
            other is not None
            and isinstance(other, Service)
            and self.domain == other.domain
            and self.name == other.name
            and self.namespace == other.namespace
            and self.request_topic == other.request_topic
            and self.response_topic == other.response_topic
            and self.event_topic == other.event_topic
        )

    def __str__(self) -> str:
        return f'Service {self.domain}:{self.name}'

    @classmethod
    def standard(cls, name: Optional[str] = None, domain: Optional[str] = None) -> 'Service':
        from eventy.config import SERVICE_NAME, SERVICE_DOMAIN
        name = name or SERVICE_NAME
        domain = domain or SERVICE_DOMAIN
        return Service(
            service_name=name,
            service_domain=domain,
            service_namespace=f'urn:{domain}:{name}',
            event_topic=f'{name}-events',
            request_topic=f'{name}-requests',
            response_topic=f'{name}-responses',

        )
