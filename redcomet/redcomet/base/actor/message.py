from typing import Optional

from redcomet.base.messaging.content import PacketContentAbstract


class MessageAbstract(PacketContentAbstract):

    @property
    def ref_id(self) -> Optional[str]:
        return None
