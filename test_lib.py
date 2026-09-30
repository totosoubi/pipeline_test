from lib import add, average


def test_verage() -> None:
    assert average([1, 2, 3]) == 2.0
    assert average([1, 2]) == 1.5
    assert average([-2, 0, 2]) == 0.0


def test_add() -> None:
    assert add(2, 2) == 4
    assert add(-2, 2) == 0
    assert add(0, 0) == 0
