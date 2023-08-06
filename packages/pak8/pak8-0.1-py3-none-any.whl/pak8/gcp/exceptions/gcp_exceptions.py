# Exceptions currently being used
class GCPAuthException(Exception):
    pass


class GCPEnableApiException(Exception):
    pass


class Pak8GCPConfInvalidException(Exception):
    pass


class Pak8GCPCredentialsInvalidException(Exception):
    pass


class GKEClusterCreateException(Exception):
    pass


class GKEClusterNotFoundException(Exception):
    pass


class Pak8GKEClientException(Exception):
    pass


# Exceptions to fix
class Pak8GCSClientException(Exception):
    pass


class Pak8CloudSQLClientException(Exception):
    pass


class GKEOperationNotFoundException(Exception):
    pass


class GKEQuotaExceededException(Exception):
    pass


class CloudSQLInstanceNotFoundException(Exception):
    pass
