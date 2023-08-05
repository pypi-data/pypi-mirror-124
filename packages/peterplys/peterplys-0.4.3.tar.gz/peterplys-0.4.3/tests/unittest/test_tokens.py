from dataclasses import dataclass

from energytt_platform.bus import Message
from energytt_platform.tokens import TokenEncoder


@dataclass
class Nested:
    something: str


@dataclass
class Message1(Message):
    something: str
    nested: Nested


class TestTokenEncoder:

    def test__should_encode_and_decode_correctly(self):

        # -- Arrange ---------------------------------------------------------

        obj = Message1(
            something='something',
            nested=Nested(something='something nested'),
        )

        uut = TokenEncoder(
            schema=Message1,
            secret='123',
        )

        # -- Act -------------------------------------------------------------

        encoded = uut.encode(obj=obj)
        decoded = uut.decode(encoded_jwt=encoded)

        # -- Assert ----------------------------------------------------------

        assert isinstance(decoded, Message1)
        assert decoded != encoded
        assert decoded == obj
