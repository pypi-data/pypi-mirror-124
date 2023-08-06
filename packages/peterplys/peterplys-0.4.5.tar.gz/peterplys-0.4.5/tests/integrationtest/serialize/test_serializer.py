import pytest
from dataclasses import dataclass

from energytt_platform.bus import Message
from energytt_platform.serialize import \
    Serializer, simple_serializer, json_serializer


@dataclass
class Nested:
    something: str


@dataclass
class Message1(Message):
    something: str
    nested: Nested


class TestSerializer:

    @pytest.mark.parametrize('uut', [
        simple_serializer,
        json_serializer,
    ])
    def test__should_serialize_and_deserialize_correctly(self, uut: Serializer):

        # -- Arrange ---------------------------------------------------------

        obj = Message1(
            something='something',
            nested=Nested(something='something nested'),
        )

        # -- Act -------------------------------------------------------------

        serialized = uut.serialize(obj=obj)
        deserialized = uut.deserialize(data=serialized, schema=Message1)

        # -- Assert ----------------------------------------------------------

        assert isinstance(deserialized, Message1)
        assert deserialized == obj
