import pytest
from dataclasses import dataclass

from energytt_platform.bus import Message
from energytt_platform.bus.registry import MessageRegistry


@dataclass
class Message1(Message):
    something: str


@dataclass
class Message2(Message):
    something: str


class TestMessageRegistry:

    def test__from_message_types__items_added_to_registry(self):

        # -- Act -------------------------------------------------------------

        uut = MessageRegistry.from_message_types(Message1, Message2)

        # -- Assert ----------------------------------------------------------

        assert len(uut) == 2
        assert uut['Message1'] == Message1
        assert uut['Message2'] == Message2

    def test__add__items_added_to_registry(self):

        # -- Arrange ---------------------------------------------------------

        uut = MessageRegistry()

        # -- Act -------------------------------------------------------------

        uut.add(Message1, Message2)

        # -- Assert ----------------------------------------------------------

        assert len(uut) == 2
        assert uut['Message1'] == Message1
        assert uut['Message2'] == Message2

    @pytest.mark.parametrize('item', [
        Message1,
        Message1(something='test'),
        'Message1',
    ])
    def test__contains__item_exists__returns_true(self, item):

        # -- Arrange ---------------------------------------------------------

        uut = MessageRegistry()

        # -- Act -------------------------------------------------------------

        uut.add(Message1, Message2)

        # -- Assert ----------------------------------------------------------

        assert item in uut

    @pytest.mark.parametrize('item', [
        Message2,
        Message2(something='test'),
        'Message2',
    ])
    def test__contains__item_does_not_exist__returns_false(self, item):

        # -- Arrange ---------------------------------------------------------

        uut = MessageRegistry()

        # -- Act -------------------------------------------------------------

        uut.add(Message1)

        # -- Assert ----------------------------------------------------------

        assert item not in uut

    @pytest.mark.parametrize('item', [
        Message1,
        Message1(something='test'),
        'Message1',
    ])
    def test__get__item_exists__returns_true(self, item):

        # -- Arrange ---------------------------------------------------------

        uut = MessageRegistry()

        # -- Act -------------------------------------------------------------

        uut.add(Message1, Message2)

        # -- Assert ----------------------------------------------------------

        assert uut.get(item) is Message1

    @pytest.mark.parametrize('item', [
        Message2,
        Message2(something='test'),
        'Message2',
    ])
    def test__get__item_does_not_exist__returns_none(self, item):

        # -- Arrange ---------------------------------------------------------

        uut = MessageRegistry()

        # -- Act -------------------------------------------------------------

        uut.add(Message1)

        # -- Assert ----------------------------------------------------------

        assert uut.get(item) is None
