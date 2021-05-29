from enum import Enum
from communication_parser import CommunitcationParserResult
from communication_protocol import MessageType

class MessagingTypes(Enum):
    NONE = 0
    GLOBAL = 1

class MessagingParserResult():
    def __init__(self, res: CommunitcationParserResult):
        if res.result_type != MessageType.MESSAGING:
            # additional verification
            self.msg_type = MessagingTypes.NONE
            return
        body = res.msg_body
        self.msg_type = MessagingTypes(body["type"])
        self.sender_uuid = res.uuid
        self.msg_text = body["text"]


# Module to parse Messaging from clients and process with them
class MessagingModule():

    @staticmethod
    def parse_message(res: CommunitcationParserResult)-> MessagingParserResult:
        result = MessagingParserResult(res)
        return result


