from dataclasses import dataclass
from unittest.mock import MagicMock, patch

import pytest

from energytt_platform.bus import Message
from energytt_platform.bus.serialize import MessageSerializer


@dataclass
class Nested:
    something: str


@dataclass
class Message1(Message):
    something: str
    nested: Nested


class TestMessageSerializer:

    def test__should_serialize_and_deserialize_correctly(self):

        # -- Arrange ---------------------------------------------------------

        obj = Message1(
          something='something',
          nested=Nested(something='something nested'),
        )

        registry_mock = MagicMock()
        registry_mock.__contains__.return_value = True
        registry_mock.get.return_value = Message1

        uut = MessageSerializer(registry=registry_mock)

        # -- Act -------------------------------------------------------------

        serialized = uut.serialize(obj)
        deserialized = uut.deserialize(serialized)

        # -- Assert ----------------------------------------------------------

        assert isinstance(deserialized, Message1)
        assert deserialized == obj

    def test__serialize__message_not_in_registry__should_raise_serialize_error(self):

        # -- Arrange ---------------------------------------------------------

        obj = Message1(
          something='something',
          nested=Nested(something='something nested'),
        )

        registry_mock = MagicMock()
        registry_mock.__contains__.return_value = False

        uut = MessageSerializer(registry=registry_mock)

        # -- Act -------------------------------------------------------------

        with pytest.raises(uut.SerializeError):
            uut.serialize(obj)
  
    @patch('energytt_platform.bus.serialize.json_serializer')
    def test__deserialize__message_not_in_registry__should_raise(self, json_serializer_mock):

        # -- Arrange ---------------------------------------------------------

        registry_mock = MagicMock()
        registry_mock.__contains__.return_value = False

        wrapped_msg_mock = MagicMock(type=123)

        json_serializer_mock.deserialize.return_value = wrapped_msg_mock

        uut = MessageSerializer(registry=registry_mock)

        # -- Act -------------------------------------------------------------

        with pytest.raises(uut.DeserializeError):
            uut.deserialize(b'does not matter')
