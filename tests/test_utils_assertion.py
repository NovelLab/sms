"""Test for assertion utility."""

# Official Libraries
import pytest

# My Modules
from sms.utils.assertion import is_int, is_str
from sms.utils.assertion import is_instance
from sms.utils.assertion import is_list, is_tuple, is_dict


# test "is_dict"
@pytest.mark.parametrize("x",
        [{"a":1, "b":2}, {}])
def test_assertion_is_dict(x):

    assert is_dict(x) or is_dict(x) == {}, f"Expected a dictionary type value: {x}"


@pytest.mark.parametrize("x",
        [1, "a", [1,2,3]])
def test_assertion_is_dict__failure(x):

    with pytest.raises(AssertionError):
        is_dict(x)


# test "is_int"
@pytest.mark.parametrize("x",
        [1, 0, -1,])
def test_assertion_is_int(x):

    assert is_int(x) or is_int(x) == 0, f"Expected an integer type value: {x}"


@pytest.mark.parametrize("x",
        ["a", [1,2,3], {"a":1,},])
def test_assertion_is_int__failure(x):

    with pytest.raises(AssertionError):
        is_int(x)


# test "is_list"
@pytest.mark.parametrize("x",
        [[1,2,3], []])
def test_assertion_is_list(x):

    assert is_list(x) or is_list(x) == [], f"Expected a list type value: {x}"


@pytest.mark.parametrize("x",
        [1, "a", {"a":1}, (1,2,)])
def test_assertion_is_list__failure(x):

    with pytest.raises(AssertionError):
        is_list(x)


# test "is_tuple"
@pytest.mark.parametrize("x",
        [(1,2,3), ()])
def test_assertion_is_tuple(x):

    assert is_tuple(x) or is_tuple(x) == (), f"Expected a tuple type value: {x}"


@pytest.mark.parametrize("x",
        [1, "a", {"a":1}, [1,2,]])
def test_assertion_is_tuple__failure(x):

    with pytest.raises(AssertionError):
        is_tuple(x)



# test "is_str"
@pytest.mark.parametrize("x",
        ["a", "日本語",
            """Multi
               Line
            """])
def test_assertion_is_str(x):

    assert is_str(x), f"Expected a string type value: {x}"


@pytest.mark.parametrize("x",
        [1, [], {}])
def test_assertion_is_str__failure(x):

    with pytest.raises(AssertionError):
        is_str(x)


# test "is_instance"
class Person(object):
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

class Worker(Person):
    def __init__(self, name: str, age: int, job: str):
        super().__init__(name, age)
        self.job = job

def taro():
    return Person("taro", 17)

def hanako():
    return Person("hanako", 15)

def sasaki():
    return Worker("sasaki", 25, "officeman")

@pytest.mark.parametrize(["x", "t"],
        [
            [1, int],
            ["a", str],
            [taro(), Person],
            [sasaki(), Worker],
            [sasaki(), Person],
            ])
def test_assertion_is_instance(x, t):

    assert is_instance(x, t), f"Expected a type {t} value: {x}"
