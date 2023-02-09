import pandas as pd

def read_df(fp):
    df = read_csv(fp)
    return(df)

def get_correct_phon_counts(scores):
    counts = scores.value_counts()
    if len(counts) < 3:
        missing_count_val = {1, 2, 3}.difference(set(counts.index))
        missing_count_val = list(missing_count_val)
        add_counts = pd.Series([0] * len(missing_count_val), index = missing_count_val)
    counts.append(add_counts)

    out = pd.DataFrame()
    for i in range(1, 4):
        out[f"{i}_phons_correct"] = [counts.values[i]]

    return(out)

def get_correct_percentages(out):
    None

# sub, list, 1_phonemes_correct, 2_phonemes_correct, 3_phonemes_correct, percentage_fully_correct, percentage_phons_correct
