from framework.decorators import test, skip, parametrize

@test
def test_addition():
    assert 1 + 1 == 2

@test
def test_failure():
    assert 2 * 2 == 5

@skip("not implemented")
@test
def test_skip_case():
    assert True

@parametrize("x", [1, 2, 3])
@test
def test_param(x):
    assert x < 5