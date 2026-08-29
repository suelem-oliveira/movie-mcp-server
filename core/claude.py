import os
from anthropic import Anthropic
from anthropic.types import Message


class _FakeTextBlock:
    def __init__(self, text: str):
        self.type = "text"
        self.text = text


class _FakeMessage:
    def __init__(self, text: str):
        self.content = [_FakeTextBlock(text)]
        self.stop_reason = "end_turn"
        self.role = "assistant"


class Claude:
    def __init__(self, model: str):
        self.mock_mode = os.getenv("MOCK_MODE", "0") == "1"
        self.model = model
        if not self.mock_mode:
            self.client = Anthropic()

    def add_user_message(self, messages: list, message):
        user_message = {
            "role": "user",
            "content": message.content
            if isinstance(message, Message) or isinstance(message, _FakeMessage)
            else message,
        }
        messages.append(user_message)

    def add_assistant_message(self, messages: list, message):
        assistant_message = {
            "role": "assistant",
            "content": message.content
            if isinstance(message, Message) or isinstance(message, _FakeMessage)
            else message,
        }
        messages.append(assistant_message)

    def text_from_message(self, message) -> str:
        return "\n".join(
            [block.text for block in message.content if block.type == "text"]
        )

    def chat(
        self,
        messages,
        system=None,
        temperature=1.0,
        stop_sequences=[],
        tools=None,
        thinking=False,
        thinking_budget=1024,
    ):
        if self.mock_mode:
            return self._fake_chat(messages)

        params = {
            "model": self.model,
            "max_tokens": 8000,
            "messages": messages,
            "temperature": temperature,
            "stop_sequences": stop_sequences,
        }

        if thinking:
            params["thinking"] = {
                "type": "enabled",
                "budget_tokens": thinking_budget,
            }

        if tools:
            params["tools"] = tools

        if system:
            params["system"] = system

        message = self.client.messages.create(**params)
        return message

    def _fake_chat(self, messages) -> _FakeMessage:
        last_user_content = ""
        if messages:
            last = messages[-1].get("content", "")
            last_user_content = last if isinstance(last, str) else str(last)

        preview = last_user_content.strip()[:300]

        fake_text = (
            "[MODO SIMULADO - sem chamada real a API]\n\n"
            "Recebi sua mensagem e o contexto dos documentos mencionados, "
            "mas estou rodando em modo local sem me conectar a Anthropic.\n\n"
            f"Trecho do que voce enviou:\n---\n{preview}\n---"
        )
        return _FakeMessage(fake_text)
