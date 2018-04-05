# TALON: Techonology-Agnostic Long Read Analysis Pipeline
# Author: Dana Wyman
# -----------------------------------------------------------------------------
# This program takes transcripts from one or more samples (SAM format) and
# assigns them transcript and gene identifiers based on a GTF annotation.
# Novel transcripts are assigned new identifiers.

from genetree import GeneTree
from optparse import OptionParser

def getOptions():
    parser = OptionParser()
    parser.add_option("--f", dest = "infile_list", 
        help = "Comma-delimited list of input SAM files",
        metavar = "FILE", type = "string")
    parser.add_option("--gtf", "-g", dest = "gtf_file",
        help = "GTF annotation containing genes, transcripts, and exons.",
        metavar = "FILE", type = "string")
    (options, args) = parser.parse_args()
    return options

def read_gtf_file(gtf_file):
    """ Reads gene, transcript, and exon information from a GTF file.

        Args:
            gtf_file: Path to the GTF file

        Returns:
            genes: A GeneTree object, which consists of a  dictionary mapping 
            each chromosome to an interval tree data structure. Each interval 
            tree contains intervals corresponding to gene class objects. 
    """
    genes = GeneTree()

    with open(gtf_file) as gtf:
        for line in gtf:
            line = line.strip()
            
            # Ignore header
            if line.startswith("#"):
                continue

            # Split into constitutive fields on tab
            tab_fields = line.split("\t")
            chrom = tab_fields[0]
            entry_type = tab_fields[2]            

            # Process genes
            if entry_type == "gene":
                genes.add_gene_from_gtf(tab_fields)

    genes.print_tree()
    genes.get_genes_in_range("chr1", 30000, 40000, "+")
    return genes
                
def process_sam_file(sam_file):
    """ Reads transcripts from a SAM file

        Args:
            sam_file: Path to the SAM file

        Returns:
    """
    with open(sam_file) as sam:
        for line in sam:
            line = line.strip()
 
            # Ignore header
            if line.startswith("@"):
                continue

def main():
    options = getOptions()
    infile_list = options.infile_list
    gtf_file = options.gtf_file

    # Process the GTF annotations
    read_gtf_file(gtf_file)

    # Process the SAM files
    sam_files = infile_list.split(",")
    for sam in sam_files:
        process_sam_file(sam)

if __name__ == '__main__':
    main()