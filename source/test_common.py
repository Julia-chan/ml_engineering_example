from .common import invert_dict

def test_invert_dict():
    func_res = invert_dict({'key': 'value'})
    assert {'value': 'key'} == func_res
    