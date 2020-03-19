from talon.post import filter_talon_transcripts as filt
import pandas as pd

def test_filter_on_min_count():
    """ If we start with this df and apply a min_count threshold of 2:
        read_name  gene_ID  transcript_ID           dataset
          read_1      1          1             dataset_1
          read_2      1          1             dataset_1  
          read_3      2          3             dataset_1
          read_4      2          3             dataset_2  
          read_5      2          3             dataset_3
 
        Then the final df should look like this:

        gene_ID     transcript_ID    dataset   count
           1               1        dataset_1    2
    """

    reads = pd.DataFrame([['read_1', 1, 1, 'dataset_1'], ['read_2', 1, 1, 'dataset_1'], 
                          ['read_3', 2, 3, 'dataset_1'], ['read_4', 2, 3, 'dataset_2'], 
                          ['read_5', 2, 3, 'dataset_3']],
                          columns = ["read_name", "gene_ID", "transcript_ID", 'dataset'])
  
    filtered = filt.filter_on_min_count(reads, 2)

    assert len(filtered) == 1
    assert list(filtered.iloc[0]) == [ 1, 1, "dataset_1", 2 ]

def test_filter_on_n_datasets():
    """ If we start with this df and apply a min_dataset threshold of 2:
        gene_ID  transcript_ID           dataset       count
            1          1                dataset_1        2
            2          3                dataset_1        1
            2          3                dataset_2        1
            2          3                dataset_3        1

        Then the final df should look like this:

        gene_ID     transcript_ID    n_datasets   
           2               3             3
    """

    counts = pd.DataFrame([[1, 1, 'dataset_1', 2], [2, 3, 'dataset_1', 1], 
                          [2, 3, 'dataset_2', 1],
                          [2, 3, 'dataset_3', 1]],
                          columns = ['gene_ID', 'transcript_ID', 'dataset', 'count'])

    filtered = filt.filter_on_n_datasets(counts, 2)

    assert len(filtered) == 1
    assert list(filtered.iloc[0]) == [ 2, 3, 3 ]
