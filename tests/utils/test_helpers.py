from letterman.utils.helpers import flatten_dict

case_1 = {"InstanceId": "i-1234567890", "State": {"Code": 1, "Name": "running"}}
result_1 = {"InstanceId": "i-1234567890", "State.Code": 1, "State.Name": "running"}
case_2 = {"InstanceId": "i-1234567890", "ImageId": "ami-1234567890"}
result_2 = {"InstanceId": "i-1234567890", "ImageId": "ami-1234567890"}


def test_flatten_dict_basic_nested_structure():
    assert flatten_dict(case_1, ".") == result_1


def test_flatten_dict_non_nested_structure():
    assert flatten_dict(case_2, ".") == result_2
