import pandas as pd

def add_ipa(df, col, ipa_col):
    # Convert words to IPA
    words = df[col]
    ipa = []
    for word in words:
        ipa.append(eng_to_ipa.convert(word))

    # Add to file and overwrite
    df[ipa_col] = ipa

    return(df)

def score_word(word_ipa, response_ipa):
    # Compare ipa symbols in response with word
    word_ipa = set(word_ipa)
    response_ipa = set(response_ipa)

    hit_phons = word_ipa.intersection(response_ipa)
    n_hit_phons = len(hit_phons)
    missed_phons = word_ipa.difference(response_ipa)
    return(n_hit_phons, hit_phons, missed_phons)

def score_all_words(df, word_ipa, response_ipa):
    n_hit_phons_list = []
    hit_phons_list = []
    missed_phons_list = []

    for i in range(len(word_ipa)):
        n_hit_phons, hit_phons, missed_phons = score_word(word_ipa[i], response_ipa[i])

        n_hit_phons_list.append(n_hit_phons)
        hit_phons_list.append(hit_phons)
        missed_phons_list.append(missed_phons)

    df['n_hit_phons'] = n_hit_phons_list
    df['hit_phons'] = hit_phons_list
    df['missed_phons'] = missed_phons_list

    return(df)

def score(LOG):
    # Add ipa for words and responses
    df = pd.read_csv(LOG)
    df = add_ipa(df, col = 'word', ipa_col = 'word_ipa')
    df = add_ipa(df, col = 'response', ipa_col = 'response_ipa')

    # Score each word
    df = score_all_words(df, df['word_ipa'], df['response_ipa'])

    # Save to log
    df.to_csv(LOG)

