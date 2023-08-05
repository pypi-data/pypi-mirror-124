from typing import List
from dataclasses import dataclass
from datetime import datetime, timezone

from energytt_platform.serialize import Serializable


@dataclass
class InternalToken(Serializable):
    """
    TODO
    """
    issued: datetime
    expires: datetime

    # The user performing action(s)
    actor: str

    # The subject we're working with data on behalf of
    subject: str

    # Scopes granted on subject's data
    # meteringpoints.read, measurements.read, emissions.read, meteringpoint.onboard
    scope: List[str]

    @property
    def is_expired(self) -> bool:
        return self.expires < datetime.now(tz=timezone.utc)
