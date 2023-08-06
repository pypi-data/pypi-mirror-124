class UnsupportedPackageManager(Exception):
    pass


class UnsupportedAction(Exception):
    pass


class NotAuthenticated(Exception):
    pass


class FailedToLoadToken(Exception):
    pass


class FailedToRefreshToken(Exception):
    pass
