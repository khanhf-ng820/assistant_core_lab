from ui.streaming import should_stream_message, stream_text


def test_stream_text_chunks_and_reassembles():
    assert list(stream_text("hello world", chunk_size=4)) == ["hell", "o wo", "rld"]
    assert "".join(stream_text("hello world")) == "hello world"
    assert list(stream_text("")) == []


def test_should_stream_only_unstreamed_newest_assistant_message():
    assert should_stream_message(2, "assistant", total_messages=3, streamed_up_to=0) is True
    assert should_stream_message(2, "assistant", total_messages=3, streamed_up_to=2) is False
    assert should_stream_message(0, "assistant", total_messages=3, streamed_up_to=0) is False
    assert should_stream_message(2, "user", total_messages=3, streamed_up_to=0) is False
