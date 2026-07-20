from dataclasses import dataclass

from mnemograph_domain.enums import ActorKind
from mnemograph_domain.identifiers import ActorId


@dataclass(frozen=True)
class ActorRef:
    kind: ActorKind
    actor_id: ActorId
