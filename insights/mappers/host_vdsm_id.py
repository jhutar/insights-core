"""
vdsm.id- File /etc/vdsm/vdsm.id
===============================

Module for parsing the content of file ``vdsm.id``, which is a simple file.

Typical content of "vdsm.id" is::

    # VDSM UUID info
    #
    F7D9D983-6233-45C2-A387-9B0C33CB1306

Examples:
    >>> vd = shared[VDSMId]
    >>> vd.uuid
    "F7D9D983-6233-45C2-A387-9B0C33CB1306"

"""
from .. import Mapper, mapper
from ..mappers import get_active_lines


@mapper("vdsm_id")
class VDSMId(Mapper):
    """Class for parsing `vdsm.id` file."""

    def parse_content(self, content):
        """
        Returns the UUID of this Host
        - E.g.: F7D9D983-6233-45C2-A387-9B0C33CB1306
        """
        lines = get_active_lines(content)
        self.data = lines[0].strip() if len(lines) > 0 else None

    @property
    def uuid(self):
        """Return the UUID in `vdsm.id` file."""
        return self.data