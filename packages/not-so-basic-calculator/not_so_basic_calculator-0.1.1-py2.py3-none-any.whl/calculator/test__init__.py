from calculator import Calculator

calculator = Calculator()


def test_add():
    assert calculator.reset_memory() == 0
    assert calculator.add(4) == 4
    assert calculator.add(3.12) == 7.12


def test_subtract():
    assert calculator.reset_memory() == 0
    assert calculator.subtract(5) == -5
    assert calculator.subtract(2.35) == -7.35


def test_multiply():
    assert calculator.reset_memory() == 0
    assert calculator.add(2) == 2
    assert calculator.multiply(16) == 32
    assert calculator.multiply(0.5) == 16
    assert calculator.multiply(-1) == -16


def test_divide():
    assert calculator.reset_memory() == 0
    assert calculator.add(2) == 2
    assert calculator.divide(2) == 1
    assert calculator.divide(0.5) == 2
    assert calculator.divide(-1) == -2


def test_take_root():
    assert calculator.reset_memory() == 0
    assert calculator.add(64) == 64
    assert calculator.take_root(2) == 8
    assert calculator.take_root(3) == 2
    assert calculator.add(64) == 66
    assert calculator.take_root(-1) == 0.0152
