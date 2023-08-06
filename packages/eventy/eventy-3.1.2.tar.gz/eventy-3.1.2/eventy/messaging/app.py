import time
from typing import Optional, Dict

from eventy.messaging.agent import Agent, Handler, Guarantee
from eventy.messaging.errors import MessagingError
from eventy.messaging.service import Service
from eventy.messaging.store import Cursor, Store, Appender
from eventy.record import Record, Request, Event, Response
from eventy.trace_id.local import local_trace

__all__ = [
    'App',
]


class App:

    def __init__(
        self,
        service: Optional[Service] = None,
        read_batch_size: int = 1,
        read_timeout_ms: Optional[int] = None,
        write_timeout_ms: Optional[int] = None,
        ack_timeout_ms: Optional[int] = None,
        commit_timeout_ms: Optional[int] = None,
    ):
        if service is None:
            from eventy.config import SERVICE
            service = SERVICE
        self.service = service
        self.services_to_request: Dict[Service, Cursor] = dict()
        self.services_to_listen: Dict[Service, Cursor] = dict()
        self.handlers: list[Handler] = []
        self.read_batch_size = read_batch_size
        self.read_timeout_ms = read_timeout_ms
        self.write_timeout_ms = write_timeout_ms
        self.ack_timeout_ms = ack_timeout_ms
        self.commit_timeout_ms = commit_timeout_ms

    def register_agent(self, agent: Agent) -> None:
        for handler in agent.get_handlers():
            self.register_handler(handler)

    def register_handler(self, handler: Handler) -> None:
        self.handlers.append(handler)

    def register_service_to_request(self, service: Service, response_cursor: Cursor = Cursor.ACKNOWLEDGED) -> None:
        if service in self.services_to_request:
            raise MessagingError(f"Already registered service {service}.")
        self.services_to_request[service] = response_cursor

    def register_service_to_listen(self, service: Service, event_cursor=Cursor.ACKNOWLEDGED) -> None:
        if service in self.services_to_listen:
            raise MessagingError(f"Already registered service {service}.")
        self.services_to_listen[service] = event_cursor

    def run(self, store: Store) -> None:
        alo_handlers = list(
            filter(
                lambda handler: handler.delivery_guarantee == Guarantee.AT_LEAST_ONCE,
                self.handlers
            )
        )
        eos_handlers = list(
            filter(
                lambda handler: handler.delivery_guarantee == Guarantee.EXACTLY_ONCE,
                self.handlers
            )
        )
        amo_handlers = list(
            filter(
                lambda handler: handler.delivery_guarantee == Guarantee.AT_MOST_ONCE,
                self.handlers
            )
        )

        store.register_topic(self.service.request_topic)
        for service, cursor in self.services_to_listen.items():
            store.register_topic(service.event_topic, cursor)
        for service, cursor in self.services_to_request.items():
            store.register_topic(service.response_topic, cursor)

        appender = _StoreAppender(self, store)

        while True:
            records = list(
                store.read(
                    max_count=self.read_batch_size,
                    timeout_ms=self.read_timeout_ms,
                    auto_ack=False,
                )
            )
            if not records:
                time.sleep(0.05)
                continue

            # At Least Once
            for record in records:
                with local_trace(correlation_id=record.correlation_id):
                    for handler in alo_handlers:
                        handler(record, appender)

            if eos_handlers:
                store.start_transaction()
                try:
                    store.ack(self.ack_timeout_ms)
                    for record in records:
                        with local_trace(correlation_id=record.correlation_id):
                            for handler in eos_handlers:
                                handler(record, appender)
                    store.commit(self.commit_timeout_ms)
                except Exception as e:
                    store.abort()
                    raise e

            # At Most Once
            for record in records:
                with local_trace(correlation_id=record.correlation_id):
                    for handler in amo_handlers:
                        handler(record, appender)


class _StoreAppender(Appender):
    def __init__(
        self,
        app: App,
        store: Store,
    ):
        self.app = app
        self.store = store

    def append(self, record: Record) -> None:
        topics: list[str] = list()
        if isinstance(record, Event):
            if self.app.service:
                topics.append(self.app.service.event_topic)
        elif isinstance(record, Response):
            if self.app.service:
                topics.append(self.app.service.response_topic)
        elif isinstance(record, Request):
            for service in self.app.services_to_request:
                if service.namespace == record.namespace:
                    topics.append(service.request_topic)
        else:
            raise MessagingError(f"Record of unknown type: {record}.")

        for topic in topics:
            self.store.write(
                record, topic, self.app.write_timeout_ms
            )
