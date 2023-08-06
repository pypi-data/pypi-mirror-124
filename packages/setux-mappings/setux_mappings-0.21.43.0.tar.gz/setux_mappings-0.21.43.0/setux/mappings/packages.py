from setux.core.mapping import Packages


class Debian(Packages):
    pkg = dict(
        sqlite = 'sqlite3',
    )


class FreeBSD(Packages):
    pkg = dict(
        sqlite = 'sqlite3',
    )
