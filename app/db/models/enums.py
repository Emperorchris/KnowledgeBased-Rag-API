import enum

class DocumentSourceEnum(str, enum.Enum):
    UPLOADED = "uploaded"
    IMPORTED = "imported"
    GENERATED = "generated"
    SCRAPED = "scraped"


class MessageRoleEnum(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
