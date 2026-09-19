import json
from dataclasses import asdict, dataclass
from datetime import datetime, UTC

from blog.core.actor import current_actor
from blog.core.messages import Event
from blog.runtime.db.session import Database


@dataclass(frozen=True)
class OutboxRecord:
    event_name: str
    payload: str
    actor_id: int | None
    created_at: datetime


async def record(event: Event) -> None:
    session = Database.session()
    actor = current_actor()
    session.add(
        OutboxRecord(
            event_name=event.event_name,
            payload=json.dumps(asdict(event), default=str),
            actor_id=actor.customer_id,
            created_at=datetime.now(UTC),
        )
    )
