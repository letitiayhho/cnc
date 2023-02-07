from psychopy import prefs
prefs.hardware['audioLib'] = ['ptb']
from psychopy.sound.backend_ptb import SoundPTB as Sound
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors
from psychtoolbox import GetSecs, WaitSecs, hid
from psychopy.hardware.keyboard import Keyboard
import random
import numpy as np
from scipy.stats import beta
import os
import git
import pandas as pd

def set_cwd():
    repo = git.Repo('.', search_parent_directories=True)
    os.chdir(repo.working_tree_dir)
    print(repo.working_tree_dir)

def get_window():
    #WIN = visual.Window(size = (1920, 1080),
    WIN = visual.Window(size = (800, 600),
    screen = -1,
    units = "norm",
    fullscr = False,
    pos = (0, 0),
    allowGUI = False)
    return(WIN)

def open_log(SUB_NUM, LIST_NUM):
    log = "data/sub-" + SUB_NUM + "_list-" + LIST_NUM + ".csv"

    if not os.path.isfile(log): # create log file if it doesn't exist
        print(f"Creating {log}")
        d = {
            'sub_num': [],
            'list_num': [],
            'trial_num': [],
            'word_fp': [],
            'response': [],
            }
        print(d)
        df = pd.DataFrame(data = d)
        df.to_csv(log, mode='w', index = False)
    return(log)

def get_trial_num(LOG):
    log = pd.read_csv(LOG)
    trial_nums = log['num']
    if len(trial_nums) == 0:
        trial_num = 1
    else:
        trial_num = trial_nums.iloc[-1] + 1
    trial_num = int(trial_num)
    return(trial_num)

def start(WIN, block):
    if block == 0:
        instructions(WIN)
    else:
        block_welcome(WIN, block)

def display_instructions(WIN, text):
    instructions = visual.TextStim(WIN, text = text)
    instructions.draw()
    WIN.flip()
    event.waitKeys(keyList = ['return'])
    WIN.flip()
    print(text)

def instructions(WIN):
    display_instructions(WIN, "Welcome to the experiment. \n \n  Press 'enter' to begin.")
    display_instructions(WIN, "At each trial you will be presented with a target tone. After the target you will hear a short burst of white noise followed by a pitch-adjusted version of the target tone. Please use the 'up' and 'down' arrow keys to adjust the pitch of the displaced tone until it matches the target tone then press 'enter' to submit your answer. \n \n  Press 'enter' to continue.")
    display_instructions(WIN, "You will now complete three practice trials. Please let you experimenter know if you have any questions or are experiencing any difficulties with the display or audio. \n \n Press 'enter' to continue to the practice trials.")

def block_welcome(WIN, block):
    display_instructions(WIN, f"Welcome to block number {block}/5. \n \n Press 'enter' to begin the block.")

def ready(WIN):
    block_begin = visual.TextStim(WIN, text = "Press 'enter' to begin!")
    block_begin.draw()
    WIN.flip()
    event.waitKeys(keyList = ['return'])
    WIN.flip()

def read_wordlist(LIST_NUM):
    wordlist = pd.read_csv(f'stim/wordlist/list-{LIST_NUM}.csv')
    return(wordlist)

def get_word(wordlist, trial_num, practice = False):
    row = df[(df['practice'] == 1) & (df['num'] == 1)]
    word_fp = row['fp'].iat[0]
    word = row['word'].iat[0]
    print(f'trial_num: {trial_num}')
    print(f'word: {word}')
    return(word, word_fp

def play_word(WIN, word_fp):
    target_text = visual.TextStim(WIN, text = "Press 'space' to hear the target word.")
    target_text.draw()
    WIN.flip()
    snd = Sound(word_fp)

    while True:
        keys = event.getKeys(keyList = ['space'])
        if 'space' in keys:
            snd.play()
            WaitSecs(1.2) # longest word is 1.12 secs
            print('Word played')
            WIN.flip()
            break

def get_response(WIN, cmu_dict):
    # Prompt response
    display_instructions(WIN, "What word did you hear?")

    # Fetch response
    response = []
    response_text = ''

    while True:
        keys = event.getKeys()
        if response in cmu_dict and 'return' in keys:
            break
        elif response not in cmu_dict and 'return' in keys:
            display_instructions(WIN, "Please enter a viable word!")
        elif keys:
            if 'return' in keys:
                None
            elif 'backspace' in keys:
                response = response[:-1]
            else:
                response.append(keys)
            response_text = ''.join([item for sublist in response for item in sublist])
            #WIN.flip()
            display_instructions(WIN, response_text)
            #WIN.flip()

    return(response)

def broadcast(n_tones, var):
    if not isinstance(var, list):
        broadcasted_array = [var]*n_tones
    return(broadcasted_array)

def write_log(LOG, SUB_NUM, LIST_NUM, trial_num, word, response):
    print("Writing to log file")
    d = {
        'sub_num': SUB_NUM,
        'list_num': LIST_NUM,
        'trial_num': trial_num,
        'word': word,
        'response': response,
        }
    df = pd.DataFrame(data = d,
            index = [trial_num])
    df.to_csv(LOG, mode='a', header = False, index = False)

def end(WIN, block):
    display_instructions(WIN, f"End of block! You may now take a break if you wish. \n \n Press 'enter' to complete this block.")
