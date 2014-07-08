import main_twisted
from main_twisted import *
from mock import Mock

def test_setUnset_Control():
    sets['control'] = False
    setUnset('control')
    assert sets['control'] == True

def test_class_Set():
    sets['control'] = False
    c = Set()
    request = Mock()
    request.args = {'var': ['control']}
    main_twisted.setUnset = Mock()
    c.render_POST(request)
    assert main_twisted.setUnset.called
