from main_twisted import *

def test_setUnset_Control():
    sets['control'] = False
    setUnset('control')
    assert sets['control'] == True