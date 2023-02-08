import pandas as pd
import eng_to_ipa

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
    # Compare first phon
    words_ipa, response_ipa, hit_phons, n_hit_phons, missed_phons = compare_first_phon(word_ipa, response_ipa)

    # Compare ipa symbols for remaining phons
    word_ipa = set(word_ipa)
    response_ipa = set(response_ipa)

    # Add to scores
    hit_phons.append(list(word_ipa.intersection(response_ipa)))
    n_hit_phons += len(hit_phons)
    missed_phons.append(list(word_ipa.difference(response_ipa)))

    hit_phons = flatten(hit_phons)
    missed_phons = flatten(missed_phons)
    
    print("Comparing rest phon")
    print(f"hit_phons: {hit_phons}")
    print(f"n_hit_phons: {n_hit_phons}")
    print(f"missed_phons: {missed_phons}")
    
    return(n_hit_phons, hit_phons, missed_phons)

def compare_first_phon(word_ipa, response_ipa):
    # Compare first phon
    if word_ipa[0] == response_ipa[0]:
        hit_phons = [word_ipa[0]]
        n_hit_phons = 1
        missed_phons = []
    else:
        hit_phons = []
        n_hit_phons = 0
        missed_phons = [word_ipa[0]]

    del word_ipa[0]
    del response_ipa[0]

    print("Comparing first phon")
    print(f"hit_phons: {hit_phons}")
    print(f"n_hit_phons: {n_hit_phons}")
    print(f"missed_phons: {missed_phons}")

    return(word_ipa, response_ipa, hit_phons, n_hit_phons, missed_phons)

def flatten(l):
    return [item for sublist in l for item in sublist]

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

