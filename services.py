from clients import CrewAiClient
from models import Conversation, Message


class MessageSubmissionService:
    def __init__(self, conversation: Conversation):
        self._conversation = conversation
        self._client = CrewAiClient()

    def send_message(self, message: Message):
        kickoff_id = self._client.kickoff(
            self._conversation.id,
            message.model_dump(),
        )

        result_json = self._client.status(kickoff_id)

        if not self._conversation.id and result_json["id"]:
            self._conversation.id = result_json["id"]

        return Message(**result_json["history"][-1])
