from enum import StrEnum


class Currency(StrEnum):
    """Standard ISO 4217 currency codes."""

    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    CAD = "CAD"
    NGN = "NGN"


class CountryCode(StrEnum):
    """Standard ISO 3166-1 alpha-2 country codes."""

    US = "US"
    GB = "GB"
    CA = "CA"
    NG = "NG"


class NotificationChannel(StrEnum):
    """Supported application communication channels."""

    EMAIL = "EMAIL"
    SMS = "SMS"
    PUSH = "PUSH"
    WHATSAPP = "WHATSAPP"
    IN_APP = "IN_APP"


class MediaType(StrEnum):
    """Supported file system or upload asset media types."""

    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"
    DOCUMENT = "DOCUMENT"
    ARCHIVE = "ARCHIVE"
