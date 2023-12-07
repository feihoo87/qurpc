import pickle

import pytest

from qurpc.bencoder import decodes, encodes, Bencached

msg = {
    'w': {
        'a': -1,
        'b': 2,
        'c': {
            'p': b'world',
            'q': 0
        }
    },
    'x': 1,
    'y': [1, 2, 3],
    'z': b'hello'
}


def test_encode():
    assert encodes(2283) == b'i2283e'
    assert encodes("hello") == b'5:hello'
    assert encodes(b"hello") == b'5:hello'
    assert encodes([1, 2, 'xyz', True, False]) == b'li1ei2e3:xyzi1ei0ee'

    assert encodes(
        msg
    ) == b'd1:wd1:ai-1e1:bi2e1:cd1:p5:world1:qi0eee1:xi1e1:yli1ei2ei3ee1:z5:helloe'


def test_decode():
    assert decodes(b'i2283e') == 2283
    assert decodes('i2283e') == 2283
    assert decodes(b'5:hello') == b"hello"
    assert decodes(b'0:') == b""
    assert decodes(b'li1ei2e3:xyzi1ei0ee') == [1, 2, b'xyz', 1, 0]
    assert pickle.dumps(
        decodes(
            b'd1:wd1:ai-1e1:bi2e1:cd1:p5:world1:qi0eee1:xi1e1:yli1ei2ei3ee1:z5:helloe'
        )) == pickle.dumps(msg)


def test_Bencached():
    assert encodes(Bencached(b"xyz")) == b"xyz"


def test_error():
    with pytest.raises(ValueError):
        decodes(b'6:hello')

    with pytest.raises(ValueError):
        decodes(b'x122e')

    with pytest.raises(ValueError):
        decodes(b'0 :')

    with pytest.raises(ValueError):
        decodes(b'i-0e')

    with pytest.raises(ValueError):
        decodes(b'i0123e')
