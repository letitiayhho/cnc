import pandas as pd

def get_correct_phon_counts(scores):
    counts = df['n_hit_phons'].value_counts()
    if len(counts) < 3:
        missing_count_val = {1, 2, 3}.difference(set(counts.index))
        missing_count_val = list(missing_count_val)
        add_counts = pd.Series([0] * len(missing_count_val), index = missing_count_val)
    counts = counts.append(add_counts)

    out = pd.DataFrame()
    # Add col 1_phons_correct, 2_phons_correct, 3_phons_correct
    for i in range(len(counts)):
        counts.values[i]
        out[f"{counts.index[i]}_phons_correct"] = [counts.values[i]]
        out[f"{counts.index[i]}_phons_score"] = [counts.values[i]*counts.index[i]]

    return(out)

def get_correct_percentages(df, out):
    # Add col percent_words_fully_correct, percent_phonemes_correct
    out['percent_words_fully_correct'] = out['3_phons_correct']/50
    out['percent_phonemes_correct'] = sum(df['n_hit_phons'])/150
    return(out)

def add_info(df, out):
    # Add col sub, list
    out.insert(0, 'list', df['list_num'][0])
    out.insert(0, 'sub', df['sub_num'][0])
    return(out)

def aggregate_score(log):
    df = pd.read_csv(log)
    out = get_correct_phon_counts(df)
    out = get_correct_percentages(df, out)
    out = add_info(df, out)
    out.to_csv('../data/aggregate.csv', mode='a')