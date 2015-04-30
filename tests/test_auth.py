from application.auth import decode_token, encode_token


def test_token_encoding_and_decoding():
    payload = dict(hello='world')
    token = encode_token(payload)
    result = decode_token(token)
    assert result.get('hello') == 'world'
