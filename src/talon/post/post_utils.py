# Utilities for the post-TALON scripts
import sqlite3

from .. import query_utils as qutils


def handle_filtering(database, annot, observed, whitelist_file, dataset_file):
    """Determines which transcripts to allow in the analysis. This can be done
    in two different ways. If no whitelist is included, then all of the
    transcripts in the database are included (modified by 'observed'
    option). If a whitelist is provided, then transcripts on that list
    will be included (modified by 'observed' option). This can be
    tuned further by providing a dataset file, but this is optional."""

    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get list of datasets to use in run
    if dataset_file != None:
        datasets = qutils.parse_datasets(dataset_file, cursor)
    elif observed == True:
        datasets = qutils.fetch_all_datasets(cursor)
    else:
        datasets = None

    # Get initial transcript whitelist
    if whitelist_file != None:
        whitelist = qutils.parse_whitelist(whitelist_file)
    else:
        whitelist = qutils.fetch_all_transcript_gene_pairs(cursor)

    if datasets != None:
        # Limit the whitelist to transcripts detected in the datasets
        transcripts = [x[1] for x in whitelist]
        transcript_str = qutils.format_for_IN(transcripts)
        dataset_str = qutils.format_for_IN(datasets)

        query = """ SELECT DISTINCT gene_ID, transcript_ID
                    FROM observed
                    WHERE transcript_ID IN %s
                    AND dataset in %s """ % (
            transcript_str,
            dataset_str,
        )
        cursor.execute(query)
        whitelist = cursor.fetchall()

    conn.close()

    # check if the pass list has any transcripts
    if len(whitelist) == 0:
        raise ValueError("No transcripts found with the given filtering settings")

    return whitelist
