# tests/test_app.py
def add(a, b):
    return a - b  # BUG: should be a + b

def test_addition():
    assert add(2, 3) == 5, "Expected 5 but got something else"

def test_always_passes():
    assert 1 + 1 == 2
