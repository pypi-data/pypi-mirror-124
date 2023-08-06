from energytt_platform.bus import MessageBroker, Message


class TestMessageBroker:
    """
    TODO
    """

    # -- poll() --------------------------------------------------------------

    def test__poll__publish_messages_and_subscribe_to_all_topics__should_receive_messages_from_all_topics(
            self,
            broker: MessageBroker,
            msg1: Message,
            msg2: Message,
            msg3: Message,
    ):
        """
        TODO
        """

        # -- Act -------------------------------------------------------------

        broker.publish(topic='TOPIC1', msg=msg1)
        broker.publish(topic='TOPIC2', msg=msg2)
        broker.publish(topic='TOPIC2', msg=msg3)

        broker.subscribe(['TOPIC1', 'TOPIC2'])

        received_messages = broker.poll(timeout=5)

        # -- Assert ----------------------------------------------------------

        assert received_messages == {
            'TOPIC1': [msg1],
            'TOPIC2': [msg2, msg3],
        }

    def test__poll__publish_messages_and_subscribe_to_some_topics__should_receive_messages_from_subscribed_topics(
            self,
            broker: MessageBroker,
            msg1: Message,
            msg2: Message,
            msg3: Message,
    ):
        """
        TODO
        """

        # -- Act -------------------------------------------------------------

        broker.publish(topic='TOPIC1', msg=msg1)
        broker.publish(topic='TOPIC2', msg=msg2)
        broker.publish(topic='TOPIC3', msg=msg3)

        broker.subscribe(['TOPIC1'])

        received_messages = broker.poll(timeout=5)

        # -- Assert ----------------------------------------------------------

        assert received_messages == {
            'TOPIC1': [msg1],
        }

    # -- poll_list() ---------------------------------------------------------

    def test__poll_list__publish_messages_and_subscribe_to_all_topics__should_receive_messages_from_all_topics(
            self,
            broker: MessageBroker,
            msg1: Message,
            msg2: Message,
            msg3: Message,
    ):
        """
        TODO
        """

        # -- Act -------------------------------------------------------------

        broker.publish(topic='TOPIC1', msg=msg1)
        broker.publish(topic='TOPIC2', msg=msg2)
        broker.publish(topic='TOPIC3', msg=msg3)

        broker.subscribe(['TOPIC1', 'TOPIC2', 'TOPIC3'])

        received_messages = broker.poll_list(timeout=5)

        # -- Assert ----------------------------------------------------------

        assert len(received_messages) == 3
        assert all(msg in received_messages for msg in [msg1, msg2, msg3])

    def test__poll_list__publish_messages_and_subscribe_to_some_topics__should_receive_messages_from_all_topics(
            self,
            broker: MessageBroker,
            msg1: Message,
            msg2: Message,
            msg3: Message,
    ):
        """
        TODO
        """

        # -- Act -------------------------------------------------------------

        broker.publish(topic='TOPIC1', msg=msg1)
        broker.publish(topic='TOPIC2', msg=msg2)
        broker.publish(topic='TOPIC3', msg=msg3)

        broker.subscribe(['TOPIC1'])

        received_messages = broker.poll_list(timeout=5)

        # -- Assert ----------------------------------------------------------

        assert received_messages == [msg1]
