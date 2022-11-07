import pytest
from talon import query_utils as qutils


@pytest.mark.integration
class TestPostTalonUtils(object):
    """ Make sure that the post-TALON utils are working correctly """

    def test_filtering(self):
        """ Make sure that the right transcripts and genes ended up in the
            whitelist file """

        whitelist_file = "scratch/chr11_and_Tcf3_whitelist.csv"
        whitelist = qutils.parse_whitelist(whitelist_file)

        # Gene IDs
        assert set([x[0] for x in whitelist]) == set([5, 723, 2987])
        assert set([x[1] for x in whitelist]) == set([28, 1744, 8437, 8453])
