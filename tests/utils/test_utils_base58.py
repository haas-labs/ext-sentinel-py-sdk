import pytest

from itertools import product
from random import getrandbits

from sentinel.utils.base58 import (
    b58encode,
    b58decode,
    b58encode_check,
    b58decode_check,
    b58encode_int,
    b58decode_int,
    BITCOIN_ALPHABET,
    XRP_ALPHABET,
)


BASE45_ALPHABET = b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"


@pytest.fixture(params=[BITCOIN_ALPHABET, XRP_ALPHABET, BASE45_ALPHABET])
def alphabet(request) -> str:
    return request.param


def test_simple_encode():
    data = b58encode(b"hello world")
    assert data == b"StV1DL6CwTryKyV", "Incorrect encoded data"


def test_leadingz_encode():
    data = b58encode(b"\0\0hello world")
    assert data == b"11StV1DL6CwTryKyV", "Incorrect encoded data"


def test_encode_empty():
    data = b58encode(b"")
    assert data == b"", "Incorrect encoded data"


def test_simple_decode():
    data = b58decode("StV1DL6CwTryKyV")
    assert data == b"hello world", "Incorrect decoded data"


def test_simple_decode_bytes():
    data = b58decode(b"StV1DL6CwTryKyV")
    assert data == b"hello world", "Incorrect decoded data"


def test_autofix_decode_bytes():
    data = b58decode(b"StVlDL6CwTryKyV", autofix=True)
    assert data == b"hello world", "Incorrect decoded data"


def test_leadingz_decode():
    data = b58decode("11StV1DL6CwTryKyV")
    assert data == b"\0\0hello world", "Incorrect decoded data"


def test_leadingz_decode_bytes():
    data = b58decode(b"11StV1DL6CwTryKyV")
    assert data == b"\0\0hello world", "Incorrect decoded data"


def test_empty_decode():
    data = b58decode("1")
    assert data == b"\0", "Incorrect decoded data"


def test_empty_decode_bytes():
    data = b58decode(b"1")
    assert data == b"\0", "Incorrect decoded data"


def test_check_str():
    data = "hello world"
    out = b58encode_check(data)
    assert out == b"3vQB7B6MrGQZaxCuFg4oh", "Encode check failed"

    back = b58decode_check(out)
    assert back == b"hello world", "Decode check failed"


def test_autofix_check_str():
    data = "3vQB7B6MrGQZaxCuFg4Oh"
    back = b58decode_check(data, autofix=True)
    assert back == b"hello world", "Decode check failed"


def test_autofix_not_applicable_check_str():
    charset = BITCOIN_ALPHABET.replace(b"x", b"l")
    msg = b"hello world"
    enc = b58encode_check(msg).replace(b"x", b"l").replace(b"o", b"0")
    back = b58decode_check(enc, alphabet=charset, autofix=True)
    assert back == msg, "Encode/decode check failed"


def test_check_failure():
    data = "3vQB7B6MrGQZaxCuFg4oH"
    with pytest.raises(ValueError):
        b58decode_check(data)


def test_check_identity(alphabet):
    data = b"hello world"
    out = b58decode_check(b58encode_check(data, alphabet=alphabet), alphabet=alphabet)
    assert out == data, "Decode/Incode check failed"


def test_round_trips(alphabet):
    possible_bytes = [b"\x00", b"\x01", b"\x10", b"\xff"]
    for length in range(0, 5):
        for bytes_to_test in product(possible_bytes, repeat=length):
            bytes_in = b"".join(bytes_to_test)
            bytes_out = b58decode(b58encode(bytes_in, alphabet=alphabet), alphabet=alphabet)
            assert bytes_in == bytes_out, "Incorrect bytes in/out"


def test_simple_integers(alphabet):
    for idx, char in enumerate(alphabet):
        charbytes = bytes([char])
        assert b58decode_int(charbytes, alphabet=alphabet) == idx, "Incorrect decode int result"
        assert b58encode_int(idx, alphabet=alphabet) == charbytes, "Incorrect encode int result"


def test_large_integer():
    number = 0x111D38E5FC9071FFCD20B4A763CC9AE4F252BB4E48FD66A835E252ADA93FF480D6DD43DC62A641155A5  # noqa
    assert b58decode_int(BITCOIN_ALPHABET) == number, "Incorrect decode int result"
    assert b58encode_int(number) == BITCOIN_ALPHABET[1:], "Incorrect encode int result"


def test_invalid_input():
    data = "xyz\b"  # backspace is not part of the bitcoin base58 alphabet
    with pytest.raises(ValueError) as err:
        b58decode(data)
    assert str(err.value) == "Invalid character '\\x08'", "Incorrect error message"


# @pytest.mark.parametrize("length", [8, 32, 256, 1024])
# def test_encode_random(benchmark, length) -> None:
#     data = getrandbits(length * 8).to_bytes(length, byteorder="big")
#     encoded = benchmark(lambda: b58encode(data))
#     assert b58decode(encoded) == data, "Incorrect decode data"


# @pytest.mark.parametrize("length", [8, 32, 256, 1024])
# def test_decode_random(benchmark, length) -> None:
#     origdata = getrandbits(length * 8).to_bytes(length, byteorder="big")
#     encoded = b58encode(origdata)
#     data = benchmark(lambda: b58decode(encoded))
#     assert data == origdata, "Incorrect data"
