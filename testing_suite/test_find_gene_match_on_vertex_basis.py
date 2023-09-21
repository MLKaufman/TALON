import pytest
from talon import talon
from talon import init_refs
from .helper_fns import fetch_correct_ID, get_db_cursor
@pytest.mark.unit

class TestIdentifyGeneOnVertexBasis(object):

    def test_perfect_match(self):
        """ Example where the vertices perfectly match a gene.
        """
        conn, cursor = get_db_cursor()
        db = "scratch/toy.db"
        build = "toy_build"
        init_refs.make_temp_novel_gene_table(cursor, "toy_build")
        run_info = talon.init_run_info(db, build)
        vertex2gene = init_refs.make_vertex_2_gene_dict(cursor)

        vertex_IDs = (1, 2, 3, 4, 5, 6)
        strand = "+"

        gene_ID, fusion = talon.find_gene_match_on_vertex_basis(vertex_IDs, strand, vertex2gene)

        correct_gene_ID = fetch_correct_ID("TG1", "gene", cursor)
        assert gene_ID == correct_gene_ID
        assert fusion == False
        conn.close()

    def test_fusion_match(self):
        """ Example where the vertices overlap multiple genes.
        """
        conn, cursor = get_db_cursor()
        db = "scratch/toy.db"
        build = "toy_build"
        init_refs.make_temp_novel_gene_table(cursor, "toy_build")
        run_info = talon.init_run_info(db, build)
        vertex2gene = init_refs.make_vertex_2_gene_dict(cursor)

        vertex_IDs = (1, 2, 3, 4, 5, 9, 10, 11)
        strand = "+"

        gene_ID, fusion = talon.find_gene_match_on_vertex_basis(vertex_IDs, strand, vertex2gene)

        correct_gene_ID = None
        assert gene_ID == correct_gene_ID
        assert fusion == True
        conn.close()

    def test_NNC_type_match(self):
        """ Example where some vertices match a gene, while others don't.
        """
        conn, cursor = get_db_cursor()
        db = "scratch/toy.db"
        build = "toy_build"
        init_refs.make_temp_novel_gene_table(cursor, "toy_build")
        run_info = talon.init_run_info(db, build)
        vertex2gene = init_refs.make_vertex_2_gene_dict(cursor)

        vertex_IDs = (1, 200, 3, 4, 5, 6)
        strand = "+"

        gene_ID, fusion = talon.find_gene_match_on_vertex_basis(vertex_IDs, strand, vertex2gene)

        correct_gene_ID = fetch_correct_ID("TG1", "gene", cursor)
        assert gene_ID == correct_gene_ID
        assert fusion == False
        conn.close()

    def test_no_match(self):
        """ Example where no match exists """
        conn, cursor = get_db_cursor()
        db = "scratch/toy.db"
        build = "toy_build"
        init_refs.make_temp_novel_gene_table(cursor, "toy_build")
        run_info = talon.init_run_info(db, build)
        vertex2gene = init_refs.make_vertex_2_gene_dict(cursor)

        vertex_IDs = (1000, 2000, 3000, 4000)
        strand = "+"

        gene_ID, fusion = talon.find_gene_match_on_vertex_basis(vertex_IDs, strand, vertex2gene)

        assert gene_ID == None
        assert fusion == False
        conn.close()
