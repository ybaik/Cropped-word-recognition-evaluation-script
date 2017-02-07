 #-*- coding: utf-8 -*-
__author__ = 'Youngki Baik'
 
import sys
import glob
import difflib

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def load_data(f, data):
    lines = f.readlines()
    for line in lines:
        key, val = line.split(' ', 1)
        data[key] = val
    return data

def main(argv=sys.argv[1:]):

    if len(argv) != 2:
        print ('Please enter "wordRecEval.py [groundtruth.txt] [result.txt]"')
        return

    # loading groundtruth data
    gtruth_path = argv[0]
    gtruth = dict()
    f = open(gtruth_path, 'r')
    gtruth = load_data(f, gtruth)
    f.close()

    # loading result data
    result_path = argv[1]
    result = dict()
    f = open(result_path, 'r')
    result = load_data(f, result)
    f.close()

    # compare: key (image name) value (result)
    word_count = 0;
    word_hit_count = 0;
    word_hit_count_nocase = 0;

    edit_distance = 0;
    edit_distance_nocase = 0;

    edit_distance_norm = 0;
    edit_distance_nocase_norm = 0;

    total_letters = 0;

    for key, gresult in gtruth.iteritems():
        total_letters = total_letters + len(gresult)
        word_count = word_count + 1
        if key in result:
            rresult = result[key]
            # lower
            if rresult == gresult:
                word_hit_count = word_hit_count + 1

            if rresult.lower() == gresult.lower():
                word_hit_count_nocase = word_hit_count_nocase + 1

            # case sensitive
            curr_ed = levenshtein(gresult, rresult)
            edit_distance = edit_distance + curr_ed
            edit_distance_norm = edit_distance_norm + float(curr_ed)/len(gresult)

            # case insensitive
            curr_ed = levenshtein(gresult.lower(), rresult.lower())
            edit_distance_nocase = edit_distance_nocase + curr_ed
            edit_distance_nocase_norm = edit_distance_nocase_norm + float(curr_ed)/len(gresult)

        else :
            edit_distance = edit_distance + len(gresult)
            edit_distance_nocase = edit_distance_nocase + len(gresult)
            edit_distance_norm = edit_distance + 1
            edit_distance_nocase_norm = edit_distance_nocase + 1

    # result print
    print 'Total letters', total_letters
    print 'Total words', word_count
    print ''
    print '# case insensitive (no case) result'
    print ' Word: hit', word_hit_count_nocase
    print ' Word: accuracy', float(word_hit_count_nocase)/word_count
    print ' Edit distance =', edit_distance_nocase
    print ' Normed edit distance =', edit_distance_nocase_norm
    print ''
    print '# case sensitive (case consideration) result'
    print ' Word: hit ', word_hit_count
    print ' Word:accuracy', float(word_hit_count)/word_count
    print ' Edit distance =', edit_distance
    print ' Normed edit distance =', edit_distance_norm

if __name__ == '__main__':
    main()