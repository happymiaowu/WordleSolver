from searching import SearchAgent


if __name__ == '__main__':
    is_win, round = SearchAgent().play()
    print('is_win: %s, round: %d' % (is_win, round))
    