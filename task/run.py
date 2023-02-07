import json
from psychtoolbox import WaitSec
from functions import *
from score_list import *

# --- Task ---

SUB_NUM = input('Input subject number: ')
LIST_NUM = input('Input list number [1-10]: ')

set_cwd()
WIN = get_window()
wordlist = read_wordlist(LIST_NUM)
cmu_dict = json.load('stim/CMU_dict.json')
LOG = open_log(SUB_NUM, LIST_NUM)
trial_num = get_trial_num(LOG)

start_practice(WIN, LIST_NUM)
ready(WIN)
while trial_num <= 3:
    word, word_fp = get_word(wordlist, trial_num, practice = True)
    play_word(WIN, word_fp)
    WaitSecs(0.5)
    get_response(WIN)
    WaitSecs(2)

start(WIN, LIST_NUM)
ready(WIN)
trial_num = 1
while trial_num <= 50:
    word, word_fp = get_word(LIST_NUM, trial_num, practice = False)
    play_word(WIN, word_fp)
    WaitSecs(0.5)
    response = get_response(WIN, cmu_dict)
    write_log(LOG, SUB_NUM, LIST_NUM, trial_num, word, response)
    trial_num += 1
    WaitSecs(2)

end(WIN, LIST_NUM)

print("Block over :-)")
core.quit()

print("Scoring...")
score(LOG)

