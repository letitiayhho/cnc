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
import json
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

def load_cmu_dict(path):
    with open(path) as json_fp:
        cmu_dict = json.load(json_fp)
    return(cmu_dict)

def open_log(SUB_NUM, LIST_NUM):
    log = "data/sub-" + SUB_NUM + "_list-" + LIST_NUM + ".csv"

    if not os.path.isfile(log): # create log file if it doesn't exist
        print(f"Creating {log}")
        d = {
            'sub_num': [],
            'list_num': [],
            'trial_num': [],
            'word': [],
            'response': [],
            }
        print(d)
        df = pd.DataFrame(data = d)
        df.to_csv(log, mode='w', index = False)
    return(log)

def get_trial_num(LOG):
    log = pd.read_csv(LOG)
    trial_nums = log['trial_num']
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
    event.waitKeys()
    WIN.flip()
    print(text)

def start(WIN):
    display_instructions(WIN, "Welcome to the Consonant-Nucleus-Consonant task. \n \n  Press any key to begin.")
    display_instructions(WIN, "For this task you will hear a series of words. After every word that you hear you will be asked to type in the word that you thought you heard. You must enter a word that recognized by the Carnegie Mellon Pronouncing Dictionary. \n\n Press any key to continue.")
    display_instructions(WIN, "You will now complete three practice trials. Please let you experimenter know if you have any questions or are experiencing any difficulties with the display or audio. \n \n Press any key to continue to the practice trials.")

def start_trials(WIN):
    display_instructions(WIN, "This is the end of the practice trials. Press any key to proceed to the remaining trials.")

def read_wordlist(LIST_NUM):
    wordlist = pd.read_csv(f'stim/wordlist/list-{LIST_NUM}.csv')
    return(wordlist)

def get_word(wordlist, trial_num, practice = False):
    row = wordlist[(wordlist['practice'] == practice) & (wordlist['num'] == trial_num)]
    word_fp = row['fp'].iat[0]
    word = row['word'].iat[0]
    dur = row['duration'].iat[0]
    print(f'trial_num: {trial_num}')
    print(f'word: {word}')
    print(f'dur: {dur}')
    return(word, word_fp, dur)

def play_word(WIN, word_fp, dur):
    target_text = visual.TextStim(WIN, text = "Press 'space' to hear the target word.")
    target_text.draw()
    WIN.flip()
    snd = Sound(word_fp)

    while True:
        keys = event.getKeys(keyList = ['space'])
        if 'space' in keys:
            snd.play()
            WaitSecs(dur + 0.2) # longest word is 1.12 secs
            print('Word played')
            WIN.flip()
            break

def turn_response_into_string(response):
    flattened = [item for sublist in response for item in sublist]
    response = ''.join(flattened)
    return(response)

def get_response(WIN, cmu_dict, text = "What word did you hear? Press any key to start."):
    # Prompt response
    display_instructions(WIN, text)

    # Fetch response
    response = []
    response_text = ''
    keylist = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'return', 'backspace']

    while True:
        keys = event.getKeys(keyList = keylist)
        if response_text and 'return' in keys: # empty response not accepted
            WIN.flip()
            break
        elif keys:
            if 'return' in keys:
                None
            elif 'backspace' in keys:
                response = response[:-1]
            else:
                response.append(keys)
            response_text = ''.join([item for sublist in response for item in sublist])
            WIN.flip()
            show_response = visual.TextStim(WIN,
                                           text = response_text,
                                           pos=(0.0, 0.0),
                                           color=(1, 1, 1),
                                           colorSpace='rgb')
            show_response.draw()
            WIN.flip()

    response = response_text
    if response not in cmu_dict:
        response = get_response(WIN, cmu_dict, text = "Please enter a viable word!")

    print(response)


#    while True:
#        keys = event.getKeys(keyList = keylist)
#        if 'return' in keys:
#            break
#        #if response in cmu_dict and 'return' in keys:
#        #    break
#        #elif response not in cmu_dict and 'return' in keys:
#        #    display_instructions(WIN, "Please enter a viable word!")
#        elif keys:
#            if 'return' in keys:
#                None
#            elif 'backspace' in keys:
#                response = response[:-1]
#            else:
#                response.append(keys)
#            response_text = ''.join([item for sublist in response for item in sublist])
#            #WIN.flip()
#            display_instructions(WIN, response_text)
#            #WIN.flip()
#    print(response)

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
    display_instructions(WIN, f"End of block! You may now take a break if you wish. \n \n Press any key to complete this block.")
