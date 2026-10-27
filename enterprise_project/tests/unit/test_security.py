from src.core.security import create_token, decode_token, hash_password, verify_password


def test_password_roundtrip():
    h = hash_password("secret123")
    assert verify_password("secret123", h)
    assert not verify_password("wrong", h)


def test_token_roundtrip_and_invalid():
    t = create_token(7, "admin")
    assert decode_token(t)["sub"] == "7"
    assert decode_token("garbage") is None
