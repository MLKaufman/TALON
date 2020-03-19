import pytest
from talon import talon, init_refs
from .helper_fns import fetch_correct_ID, get_db_cursor
@pytest.mark.integration

class TestIdentifyISM(object):

    def test_ISM_suffix(self):
        """ Example where the transcript is an ISM with suffix
        """
        conn, cursor = get_db_cursor()
        build = "toy_build"
        database = "scratch/toy.db"
        run_info = talon.init_run_info(database, build)
        talon.get_counters(database)

        edge_dict = init_refs.make_edge_dict(cursor)
        location_dict = init_refs.make_location_dict(build, cursor)
        transcript_dict = init_refs.make_transcript_dict(cursor, build)
        gene_starts = init_refs.make_gene_start_or_end_dict(cursor, build, "start")
        gene_ends = init_refs.make_gene_start_or_end_dict(cursor, build, "end")

        chrom = "chr1"
        strand = "+"
        positions = [ 500, 600, 900, 1000 ]
        edge_IDs = [4]
        vertex_IDs = [4, 5]
        v_novelty = [0, 0]

        all_matches = talon.search_for_ISM(edge_IDs, transcript_dict)
        gene_ID, transcript_ID, novelty, start_end_info = talon.process_ISM(chrom, 
                                                            positions, 
                                                            strand, edge_IDs,
                                                            vertex_IDs, 
                                                            all_matches, 
                                                            transcript_dict,
                                                            gene_starts, gene_ends, 
                                                            edge_dict, location_dict, 
                                                            run_info)

        correct_gene_ID = fetch_correct_ID("TG1", "gene", cursor) 

        assert gene_ID == correct_gene_ID
        assert start_end_info["vertex_IDs"] == [3, 4, 5, 6]
        assert start_end_info["edge_IDs"] == [3, 4, 5]
        assert start_end_info["start_novelty"] == 0 # because the exon is known
        assert start_end_info["end_novelty"] == 0
        assert transcript_dict[frozenset(start_end_info["edge_IDs"])] != None
        conn.close()

    def test_ISM_prefix(self):
        """ Example where the transcript is a prefix ISM with a novel start
        """
        conn, cursor = get_db_cursor()
        build = "toy_build"
        database = "scratch/toy.db"
        run_info = talon.init_run_info(database, build)
        talon.get_counters(database)

        edge_dict = init_refs.make_edge_dict(cursor)
        location_dict = init_refs.make_location_dict(build, cursor)
        transcript_dict = init_refs.make_transcript_dict(cursor, build)
        gene_starts = init_refs.make_gene_start_or_end_dict(cursor, build, "start")
        gene_ends = init_refs.make_gene_start_or_end_dict(cursor, build, "end")

        chrom = "chr1"
        strand = "+"
        positions = [ 1, 100, 500, 600 ]
        edge_IDs = [2]
        vertex_IDs = [2, 3]
        v_novelty = [0, 0]

        all_matches = talon.search_for_ISM(edge_IDs, transcript_dict)
        gene_ID, transcript_ID, novelty, start_end_info = talon.process_ISM(chrom,
                                                            positions,
                                                            strand, edge_IDs,
                                                            vertex_IDs,
                                                            all_matches,
                                                            transcript_dict,
                                                            gene_starts, gene_ends,
                                                            edge_dict, location_dict,
                                                            run_info)

        correct_gene_ID = fetch_correct_ID("TG1", "gene", cursor)
        assert gene_ID == correct_gene_ID
        assert start_end_info["vertex_IDs"] == [1, 2, 3, 4]
        assert start_end_info["edge_IDs"] == [1, 2, 3] 
        conn.close()


    def test_no_match(self):
        """ Example with no ISM match """

        conn, cursor = get_db_cursor()
        build = "toy_build"
        database = "scratch/toy.db"
        run_info = talon.init_run_info(database, build)
        talon.get_counters(database)

        edge_dict = init_refs.make_edge_dict(cursor)
        location_dict = init_refs.make_location_dict(build, cursor)
        transcript_dict = init_refs.make_transcript_dict(cursor, build)
        gene_starts = init_refs.make_gene_start_or_end_dict(cursor, build, "start")
        gene_ends = init_refs.make_gene_start_or_end_dict(cursor, build, "end")

        chrom = "chr1"
        strand = "+"
        positions = [ 1, 100, 900, 1000 ]
        edge_IDs = [200]
        vertex_IDs = [2, 5]
        v_novelty = [0, 0]

        all_matches = talon.search_for_ISM(edge_IDs, transcript_dict)
        assert all_matches == None
        conn.close()       

