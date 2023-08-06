# -*- coding: utf-8 -*-
from typing import Mapping

from eventsourcing.persistence import (
    AggregateRecorder,
    ApplicationRecorder,
    InfrastructureFactory,
    ProcessRecorder,
)
from eventsourcing.utils import strtobool

from eventsourcing_sqlalchemy.datastore import SQLAlchemyDatastore
from eventsourcing_sqlalchemy.recorders import (
    SQLAlchemyAggregateRecorder,
    SQLAlchemyApplicationRecorder,
    SQLAlchemyProcessRecorder,
)


class Factory(InfrastructureFactory):
    SQLALCHEMY_URL = "SQLALCHEMY_URL"
    CREATE_TABLE = "CREATE_TABLE"

    def __init__(self, application_name: str, env: Mapping[str, str]):
        super().__init__(application_name, env)
        db_url = self.getenv(self.SQLALCHEMY_URL)
        if db_url is None:
            raise EnvironmentError(
                "SQLAlchemy URL not found "
                "in environment with key "
                f"'{self.SQLALCHEMY_URL}'"
            )
        self.datastore = SQLAlchemyDatastore(url=db_url)

    def aggregate_recorder(self, purpose: str = "events") -> AggregateRecorder:
        prefix = self.application_name.lower() or "stored"
        events_table_name = prefix + "_" + purpose
        for_snapshots = purpose == "snapshots"
        recorder = SQLAlchemyAggregateRecorder(
            datastore=self.datastore,
            events_table_name=events_table_name,
            for_snapshots=for_snapshots,
        )
        if self.env_create_table():
            recorder.create_table()
        return recorder

    def application_recorder(self) -> ApplicationRecorder:
        prefix = self.application_name.lower() or "stored"
        events_table_name = prefix + "_events"
        recorder = SQLAlchemyApplicationRecorder(
            datastore=self.datastore, events_table_name=events_table_name
        )
        if self.env_create_table():
            recorder.create_table()
        return recorder

    def process_recorder(self) -> ProcessRecorder:
        prefix = self.application_name.lower() or "stored"
        events_table_name = prefix + "_events"
        prefix = self.application_name.lower() or "notification"
        tracking_table_name = prefix + "_tracking"
        recorder = SQLAlchemyProcessRecorder(
            datastore=self.datastore,
            events_table_name=events_table_name,
            tracking_table_name=tracking_table_name,
        )
        if self.env_create_table():
            recorder.create_table()
        return recorder

    def env_create_table(self) -> bool:
        default = "yes"
        return bool(strtobool(self.getenv(self.CREATE_TABLE) or default))
