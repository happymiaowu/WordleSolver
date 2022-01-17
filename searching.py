
from wordle import get_guess_result, Wordle
import json, os

class SearchAgent():

    SEARCH_TREE_FILE_NAME = 'search_tree.txt'

    def __init__(self, solution_path='solution.txt', valid_word_path='valid_word.txt'):
        with open(solution_path) as f:
            self._vocab = [l.strip() for l in f.readlines()]
        with open(valid_word_path) as f:
            self._valid = [l.strip() for l in f.readlines()]

        if not os.path.exists(self.SEARCH_TREE_FILE_NAME):
            self._search_tree = self._search_tree_creator(self._vocab)
            with open(self.SEARCH_TREE_FILE_NAME, 'w') as f:
                f.write(json.dumps(self._search_tree))
        else:
            with open(self.SEARCH_TREE_FILE_NAME) as f:
                self._search_tree = json.loads(''.join([l.strip() for l in f.readlines()]))


    def _search_tree_creator(self, vocab):
        if len(vocab) == 0:
            return {}
        if len(vocab) == 1:
            return {list(vocab)[0]: {}}

        opt_guess_word = None
        opt_min_max_depth = None
        opt_candidate_tree = None
        opt_breadth = None
        for guess_word in self._valid:
            candidate_tree = {}
            for target_word in vocab:
                guess_result = get_guess_result(guess_word, target_word)
                if guess_result not in candidate_tree:
                    candidate_tree[guess_result] = set()
                candidate_tree[guess_result].add(target_word)
            
            min_max_depth = None
            for guess_result in candidate_tree:
                min_max_depth = len(candidate_tree[guess_result]) if min_max_depth is None else max(min_max_depth, len(candidate_tree[guess_result]))
            
            if opt_min_max_depth is None or opt_min_max_depth > min_max_depth:
                opt_min_max_depth = min_max_depth
                opt_candidate_tree = candidate_tree
                opt_guess_word = guess_word
        
        search_tree = {opt_guess_word: {}}
        for guess_result in opt_candidate_tree:
            search_tree[opt_guess_word][guess_result] = self._search_tree_creator(opt_candidate_tree[guess_result])
        return search_tree

    def play(self):
        subtree = self._search_tree
        wordle = Wordle()
        while True:
            guess_word = list(subtree.keys())[0]
            _, is_terminate, is_win, history = wordle.guess(guess_word)
            guess_result = history[1][-1]
            print('round: %d, guess word: %s, guess result: %s' % (wordle.get_round(), guess_word, guess_result))
            if is_terminate:
                break
            subtree = subtree[guess_word][guess_result]
        return is_win, wordle.get_round()
        
