from psychtoolbox import WaitSecs
from functions import *
from score_list import *
from aggregate_score import *

SUB_NUM = input('Input subject number: ')
LIST_NUM = input('Input list number [1-10]: ')

set_cwd()
WIN = get_window()
wordlist = read_wordlist(LIST_NUM)
cmu_dict = load_cmu_dict('stim/CMU_dict.json')
LOG = open_log(SUB_NUM, LIST_NUM)
trial_num = get_trial_num(LOG)

start(WIN)
while trial_num <= 3:
    word, word_fp, dur = get_word(wordlist, trial_num, practice = True)
    play_word(WIN, word_fp, dur)
    WaitSecs(0.5)
    get_response(WIN, cmu_dict)
    WaitSecs(2)
    trial_num += 1

start_trials(WIN)
trial_num = 1
while trial_num <= 50:
    word, word_fp, dur = get_word(wordlist, trial_num, practice = False)
    play_word(WIN, word_fp, dur)
    WaitSecs(0.5)
    response = get_response(WIN, cmu_dict)
    write_log(LOG, SUB_NUM, LIST_NUM, trial_num, word, response)
    WaitSecs(2)
    trial_num += 1

end(WIN, LIST_NUM)

print("Block over :-)")
core.quit()

print("Scoring...")
score(LOG)

print("Getting aggregate score...")
aggregate_score(LOG)

