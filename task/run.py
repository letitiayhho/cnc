from psychtoolbox import WaitSecs
from functions import *

# --- Task ---

SUB_NUM = input('Input subject number: ')
LIST_NUM = input('Input list number [1-10]: ')

set_cwd()
WIN = get_window()
practice, num, word = read_wordlist(SUB_NUM, LIST_NUM)
LOG = open_log(SUB_NUM, LIST_NUM)
trial_num = get_trial_num(LOG)

start_practice(WIN, LIST_NUM)
ready(WIN)
while trial_num <= 3:
    word_fp, ipa = get_word(LIST_NUM, trial_num, practice = True)
    play_word(WIN, word_fp)
    WaitSecs(2)

start(WIN, LIST_NUM)
ready(WIN)
while trial_num <= 50:
    print(f'trial_num: {trial_num}')
    word_fp, ipa = get_word(LIST_NUM, trial_num, practice = False)
    print(f'word_fp: {word_fp}')
    play_word(WIN, word_fp)
    WaitSecs(1)
    response = get_response(WIN)
    write_log(LOG, SUB_NUM, LIST_NUM, trial_num, response)
    trial_num += 1
    WaitSecs(2)

score(SUB_NUM, LIST_NUM, log)
end(WIN, LIST_NUM)

print("Block over :-)")
core.quit()
