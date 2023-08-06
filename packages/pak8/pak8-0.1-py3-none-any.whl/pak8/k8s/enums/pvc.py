from pak8.utils.enums import ExtendedEnum


class PVCAccessMode(ExtendedEnum):
    READWRITEONCE = "ReadWriteOnce"
    READONLYMANY = "ReadOnlyMany"
    READWRITEMANY = "ReadWriteMany"
