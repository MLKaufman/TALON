import pytest
from talon import talon
@pytest.mark.unit

class TestGetOverlap(object):
    def test_1(self):
        """ Example where intervals of size 11 match exactly. So the answer
            should be 11.
        """
        a = [ 10, 20 ]
        b = [ 10, 20 ]
        assert talon.get_overlap(a, b)[0] == 11

    def test_2(self):
        """ Example where interval a is contained within interval b. The answer
            should be 7 (the size of interval a).
        """
        a = [ 12, 18 ]
        b = [ 10, 20 ]
        assert talon.get_overlap(a, b)[0] == 7

    def test_3(self):
        """ Example where interval a starts and ends earlier than b.
        """
        a = [ 10, 20 ]
        b = [ 15, 25 ]
        assert talon.get_overlap(a, b)[0] == 6

    def test_4(self):
        """ Example with no overlap.
        """
        a = [ 10, 20 ]
        b = [ 30, 40 ]
        assert talon.get_overlap(a, b)[0] == 0
