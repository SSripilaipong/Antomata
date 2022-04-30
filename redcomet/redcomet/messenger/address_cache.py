from typing import Dict, Optional

from redcomet.base.messaging.address import Address


class AddressCache:
    def __init__(self):
        self._cache: Dict[str, Address] = {}

    def get_address(self, target: str) -> Optional[Address]:
        return self._cache.get(target)

    def update_cache(self, address: Address):
        self._cache[address.target] = address
