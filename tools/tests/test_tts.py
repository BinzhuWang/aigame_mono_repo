from tools.mcp_server.asset.tts import MsConfig, MsText


def test_tts():
    ms_config = MsConfig()
    text = MsText(content="hello, how are you?")
    print(text.ssml())
    audio_bytes = ms_config.ssml_tts(text.ssml())
    with open("test.wav", "wb") as f:
        res = f.write(audio_bytes)
    assert res > 0
