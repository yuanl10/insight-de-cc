"""
Processing the input.txt file and calculate the average error for each window defined in window.txt,
write a file into output.

@author:      Yuan Li
@lastUpdated: 08-30-2018

Below are some doctest scripts:

>>> _calc_error({}, {})
[]

>>> _calc_error({'ABCDEF': 1.0}, {})
[]

>>> _calc_error({'ABCDEF': 1.0}, {'ABCDEF': 2.0})
[1.0]

>>> _calc_error({'ABCDEF': 1.0, 'ABCDEG': 1.1}, {'ABCDEF': 2.0})
[1.0]

>>> _calc_error({'ABCDEF': 1.0, 'ABCDEG': 1.1}, {'ABCDEF': 2.0, 'ABCDEG': 0.7})
[0.40000000000000013, 1.0]

"""

import sys
from argparse import ArgumentParser

WINDOW_SIZE = 1

def main(window_file, actual_file, predicted_file, output_file):
    with open(window_file) as window:
        try:
            WINDOW_SIZE = int(window.readline())
        except Exception as e:
            print e.message

    actual = dict()
    predicted = dict()

    with open(actual_file) as act:
        for line in act.readlines():
            if not line or line.count('|') < 2:
                continue
            cur = line.rstrip().split('|')
            if int(cur[0]) not in actual:
                actual[int(cur[0])] = dict()
            actual[int(cur[0])][cur[1]] = float(cur[2])

    with open(predicted_file) as pred:
        for line in pred.readlines():
            if not line or line.count('|') < 2:
                continue
            cur = line.rstrip().split('|')
            if int(cur[0]) not in predicted:
                predicted[int(cur[0])] = dict()
            predicted[int(cur[0])][cur[1]] = float(cur[2])

    batch = list()
    ct, err_sum = 0, 0.0

    with open(output_file, 'w+') as compare:
        for hour,v in predicted.items():
            calc_res = _calc_error(actual[hour], v)
            cur_ct = len(calc_res)
            cur_sum = sum(calc_res)

            ct += cur_ct
            err_sum += cur_sum

            batch.append({int(hour): [int(cur_ct), float(cur_sum)]})

            if len(batch) == WINDOW_SIZE:
                left = batch[0].keys()[0]
                right = batch[-1].keys()[0]

                avg_err = "{:.2f}\n".format(err_sum / ct) if ct else "NA"
                compare.write('|'.join([str(left), str(right), avg_err]))

                head = batch.pop(0)[left]

                ct -= head[0]
                err_sum -= head[1]

def _calc_error(actual, predicted):
    """
    Calculate the error given two dictionaries from actual and predict at the same hour

    :param actual and predict: the dict at the same specific hour
    :return: list, of errors calculated in {:.2f} format
    """
    if not actual or not predicted:
        return []
    return [abs(predicted[k] - actual[k]) for k in predicted.keys() if k in actual]


if __name__ == "__main__":

    import doctest
    doctest.testmod()

    # window_file = '../input/window.txt'
    # actual_file = '../input/actual.txt'
    # predicted_file = '../input/predicted.txt'
    # output_file = '../output/comparison.txt'

    # parser = ArgumentParser(description='Get file locations.')
    #
    # parser.add_argument('--window_file', help = 'Enter the window_file', required = True)
    # parser.add_argument('--actual_file', help = 'Enter the actual_file', required = True)
    # parser.add_argument('--predicted_file', help = 'Enter the predicted_file', required = True)
    # parser.add_argument('--output_file', help = 'Enter the output_file', required = True)
    #
    # args = parser.parse_args()

    window_file = sys.argv[1]
    actual_file = sys.argv[2]
    predicted_file = sys.argv[3]
    output_file = sys.argv[4]

    main(window_file, actual_file, predicted_file, output_file)
