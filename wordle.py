import random
import numpy as np

class Wordle:

    MAX_ROUND = 6

    def __init__(self, solution_path='solution.txt', valid_word_path='valid_word.txt'):
        with open(solution_path) as f:
            self._vocab = [l.strip() for l in f.readlines()]
        with open(valid_word_path) as f:
            self._valid = [l.strip() for l in f.readlines()]
        self._valid += self._vocab
        
        self._target_word = random.choice(self._vocab)
        self._round = 0
        # [char, pos], last pos is judge the alphabet is appear.
        # value: 0: not appear, 1: maybe, 2: is appear
        self._state = np.ones([26, 6])
        self._guess_path = []
        # 0: wrong alphabet, 1: right alphabet but wrong place, 2: right alphabet and right place
        self._guess_result = []

    def _update_state(self, guess_word, guess_result):
        for idx, c in enumerate(guess_word):
            asc_c = ord(c) - ord('a')
            if asc_c >= 26:
                print(asc_c, c, self._target_word, guess_word)
            if guess_result[idx] == '0':
                self._state[asc_c, :] = 0
            elif guess_result[idx] == '1':
                self._state[asc_c, idx] = 0
                self._state[asc_c, 5] = 2
            else:
                self._state[asc_c, idx] = 2
                self._state[asc_c, 5] = 2


    def _get_guess_result(self, guess_word):
        return get_guess_result(guess_word, self._target_word)

    def get_round(self):
        return self._round

    # state, is_termiate, is_win, history
    def guess(self, guess_word):
        self._guess_path.append(guess_word)
        guess_result = self._get_guess_result(guess_word)
        self._guess_result.append(guess_result)
        self._update_state(guess_word, guess_result)
        self._round += 1

        if guess_word == self._target_word:   # Guess right.
            return self._state, True, True, (self._guess_path, self._guess_result)
        elif self._round == self.MAX_ROUND:    # Round Limit Exceed.
            return self._state, True, False, (self._guess_path, self._guess_result)
        else:
            return self._state, False, False, (self._guess_path, self._guess_result)
    


# This function is use for external guess result counting.
def get_guess_result(guess_word, target_word):
    guess_result = ''
    for idx, c in enumerate(guess_word):
        if not c in target_word:
            guess_result += '0'
        elif target_word[idx] != c:
            guess_result += '1'
        else:
            guess_result += '2'
    return guess_result
