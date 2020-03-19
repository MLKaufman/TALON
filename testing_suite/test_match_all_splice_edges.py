import pytest
from talon import talon, init_refs
from .helper_fns import get_db_cursor
@pytest.mark.dbunit

class TestMatchAllEdges(object):

    def test_all_known_edges(self):
        """ Example where the toy transcript database contains matches for all
            vertices.
        """
        conn, cursor = get_db_cursor()
        build = "toy_build"
        database = "scratch/toy.db"
        talon.get_counters(database)
        edge_dict = init_refs.make_edge_dict(cursor)
        print(len(edge_dict))
        run_info = talon.init_run_info(database, build)
        conn.close()

        chrom = "chr1"
        vertex_IDs = [ 2, 3, 4, 5 ]
        strand = "+"
        edge_IDs, novelty = talon.match_all_splice_edges(vertex_IDs, strand,
                                                        edge_dict, run_info)

        assert edge_IDs == [ 2, 3, 4 ]
        assert novelty == [ 0, 0, 0 ]

    def test_antisense(self):
        """ Example where all of the vertices are in the database, but the edges
            are not, because they are antisense to the original transcript """
        
        conn, cursor = get_db_cursor()
        build = "toy_build"
        database = "scratch/toy.db"
        talon.get_counters(database)
        edge_dict = init_refs.make_edge_dict(cursor)
        run_info = talon.init_run_info(database, build)
        orig_n_edges = len(edge_dict)
        conn.close()

        chrom = "chr2"
        vertex_IDs = [ 13, 12, 11, 10 ]
        strand = "-"

        edge_IDs, novelty = talon.match_all_splice_edges(vertex_IDs, strand,
                                                        edge_dict, run_info)
        expected_edges = []
        for i in range(1,4):
            num = orig_n_edges + i
            edge_id = num
            expected_edges.append(edge_id)

        assert edge_IDs == expected_edges
        assert novelty == [ 1, 1, 1 ]

