"""
JournaldConf - File /etc/systemd/journald.conf, journald.conf.d directories
===========================================================================

The journald.conf file is a key=value file with hash comments. Everything is in the [Journal]
section, so sections are ignored.

Only active settings lines are processed, commented out settings are not processed.

Active settings are provided using the `get_active_settings_value` method or
by using the dictionary `contains` functionality.

Options that are commented out are not returned - a rule using this mapper has to be aware of which
default value is assumed by systemd if the particular option is not specified.

Note: Precedence logic is implemented in JournaldConfAll reducer, the mapper is called for every
file separately.

Example:

    >>> conf = shared[EtcJournaldConf]
    >>> conf.get_active_setting_value('Storage')
    'auto'
    >>> 'Storage' in conf.active_settings
    True
"""

from .. import Mapper, mapper, get_active_lines
from ..mappers import split_kv_pairs


class JournaldConf(Mapper):
    """
    A mapper for accessing journald conf files.
    """

    def __init__(self, *args, **kwargs):
        self.active_lines_unparsed = []
        self.active_settings = {}
        super(JournaldConf, self).__init__(*args, **kwargs)

    def parse_content(self, content):
        """
        Main parsing class method which stores all interesting data from the content.

        Args:
            content (context.content): Mapper context content
        """
        # note, the Mapper class sets:
        # * self.file_path = context.path and
        # * self.file_name = os.path.basename(context.path)
        self.active_lines_unparsed = get_active_lines(content) if content is not None else []
        #  (man page shows all options with "=")
        self.active_settings = split_kv_pairs(content, use_partition=False) if content is not None else []

    def get_active_setting_value(self, setting_name):
        """
        Access active setting value by setting name.

        Args:
            setting_name (string): Setting name
        """
        return self.active_settings[setting_name]


@mapper("etc_journald.conf")
class EtcJournaldConf(JournaldConf):
    """
    Mapper for accessing etc_journald.conf file.
    """
    pass


@mapper("etc_journald.conf.d")
class EtcJournaldConfD(JournaldConf):
    """
    Mapper for accessing etc_journald.conf.d files.
    """
    pass


@mapper("usr_journald.conf.d")
class UsrJournaldConfD(JournaldConf):
    """
    Mapper for accessing usr_journald.conf.d files.
    """
    pass