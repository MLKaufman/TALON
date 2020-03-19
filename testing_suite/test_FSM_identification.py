import pytest
from talon import talon, init_refs
from .helper_fns import fetch_correct_ID, get_db_cursor, fetch_counter
@pytest.mark.integration

class TestIdentifyFSM(object):

    def test_FSM_perfect(self):
        """ Example where the transcript is a perfect full splice match.
        """
        conn, cursor = get_db_cursor()
        build = "toy_build"
        db = "scratch/toy.db"
        talon.get_counters(db)
        edge_dict = init_refs.make_edge_dict(cursor)
        location_dict = init_refs.make_location_dict(build, cursor)
        run_info = talon.init_run_info(db, build)        
        transcript_dict = init_refs.make_transcript_dict(cursor, build)
        gene_starts = init_refs.make_gene_start_or_end_dict(cursor, build, "start")
        gene_ends = init_refs.make_gene_start_or_end_dict(cursor, build, "end")

        chrom = "chr1"
        positions = [1, 100, 500, 600, 900, 1010]
        strand = "+"
        edge_IDs = [2, 3, 4]
        vertex_IDs = [2, 3, 4, 5]
        v_novelty = [0, 0, 0, 0]

        all_matches = talon.search_for_ISM(edge_IDs, transcript_dict)

        gene_ID, transcript_ID, novelty, start_end_info = talon.process_FSM(chrom, 
                                                            positions, strand, edge_IDs,
                                                            vertex_IDs, all_matches,
                                                            gene_starts, gene_ends,
                                                            edge_dict,
                                                            location_dict, run_info)

        correct_gene_ID = fetch_correct_ID("TG1", "gene", cursor) 
        correct_transcript_ID = fetch_correct_ID("TG1-001", "transcript", cursor)
        assert gene_ID == correct_gene_ID
        assert transcript_ID == correct_transcript_ID
        assert novelty == []
        assert start_end_info["start_vertex"] == 1
        assert start_end_info["end_vertex"] == 6
        assert start_end_info["diff_3p"] == 10
        conn.close()

    def test_FSM_end_diff(self):
        """ Example where the transcript is an FSM but has a difference on
            the ends large enough to be novel.
        """
        conn, cursor = get_db_cursor()
        build = "toy_build"
        db = "scratch/toy.db"
        talon.get_counters(db)

        orig_vertices = talon.vertex_counter.value()
        edge_dict = init_refs.make_edge_dict(cursor)
        location_dict = init_refs.make_location_dict(build, cursor)
        run_info = talon.init_run_info(db, build)
        transcript_dict = init_refs.make_transcript_dict(cursor, build)
        gene_starts = init_refs.make_gene_start_or_end_dict(cursor, build, "start")
        gene_ends = init_refs.make_gene_start_or_end_dict(cursor, build, "end")

        chrom = "chr2"
        positions = [1, 100, 500, 600, 900, 1301] #Last position is > 300bp away
        strand = "+"
        edge_IDs = [13, 14, 15]
        vertex_IDs = [14, 15, 16, 17] 
        v_novelty = [0, 0, 0, 0]
  
        all_matches = talon.search_for_ISM(edge_IDs, transcript_dict)

        gene_ID, transcript_ID, novelty, start_end_info = talon.process_FSM(chrom,
                                                            positions, strand, edge_IDs,
                                                            vertex_IDs, all_matches,
                                                            gene_starts, gene_ends,
                                                            edge_dict,
                                                            location_dict, run_info) 

        correct_gene_ID = fetch_correct_ID("TG2", "gene", cursor)
        correct_transcript_ID = fetch_correct_ID("TG2-001", "transcript", cursor)
        assert gene_ID == correct_gene_ID
        assert transcript_ID == correct_transcript_ID
        assert start_end_info["end_vertex"] == orig_vertices + 1
        conn.close()

    def test_FSM_start_diff(self):
        """ Example where the transcript is an FSM but has a difference on
            the start large enough to be novel.
        """
        conn, cursor = get_db_cursor()
        build = "toy_build"
        db = "scratch/toy.db"
        talon.get_counters(db)

        edge_dict = init_refs.make_edge_dict(cursor)
        location_dict = init_refs.make_location_dict(build, cursor)
        run_info = talon.init_run_info(db, build)
        transcript_dict = init_refs.make_transcript_dict(cursor, build)
        orig_vertices = talon.vertex_counter.value()
        gene_starts = init_refs.make_gene_start_or_end_dict(cursor, build, "start")
        gene_ends = init_refs.make_gene_start_or_end_dict(cursor, build, "end")

        chrom = "chr1"
        positions = [2501, 1500, 1000, 900] #First postion is > 500bp away
        strand = "-"
        edge_IDs = [7]
        vertex_IDs = [7, 6]
        v_novelty = [0, 0]

        all_matches = talon.search_for_ISM(edge_IDs, transcript_dict)

        gene_ID, transcript_ID, novelty, start_end_info = talon.process_FSM(chrom,
                                                            positions, strand, edge_IDs,
                                                            vertex_IDs, all_matches,
                                                            gene_starts, gene_ends,
                                                            edge_dict,
                                                            location_dict, run_info)

        correct_gene_ID = fetch_correct_ID("TG3", "gene", cursor)
        correct_transcript_ID = fetch_correct_ID("TG3-001", "transcript", cursor)
        assert gene_ID == correct_gene_ID
        assert transcript_ID == correct_transcript_ID
        assert start_end_info["start_vertex"] == orig_vertices + 1
        assert start_end_info["end_vertex"] == 5
        conn.close() 

    def test_no_match(self):
        """ Example with no FSM match """

        conn, cursor = get_db_cursor()
        build = "toy_build"
        db = "scratch/toy.db"
        talon.get_counters(db)

        edge_dict = init_refs.make_edge_dict(cursor)
        location_dict = init_refs.make_location_dict(build, cursor)
        run_info = talon.init_run_info(db, build)
        transcript_dict = init_refs.make_transcript_dict(cursor, build)
        gene_starts = init_refs.make_gene_start_or_end_dict(cursor, build, "start")
        gene_ends = init_refs.make_gene_start_or_end_dict(cursor, build, "end")

        chrom = "chr1"
        positions = [1, 100, 500, 600] 
        strand = "+"
        edge_IDs = [2]
        vertex_IDs = [2,3,4,5]
        v_novelty = [0, 0, 0, 0]

        all_matches = talon.search_for_ISM(edge_IDs, transcript_dict)

        gene_ID, transcript_ID, novelty, start_end_info = talon.process_FSM(chrom,
                                                            positions, strand, edge_IDs,
                                                            vertex_IDs, all_matches,
                                                            gene_starts, gene_ends,
                                                            edge_dict,
                                                            location_dict, run_info)

        assert gene_ID == transcript_ID == None 
        conn.close()       

