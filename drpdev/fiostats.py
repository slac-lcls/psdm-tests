

import glob
import json
import jmespath


def read_test_sequence(globpatt, debug=False):
    """ Read fio jason files and return them as a list of dicts """
    data = []
    for fn in glob.glob("/reg/neh/home/wilko/projects/drp_tst/fiotst/logs/{}*json".format(globpatt)):
        with open(fn) as fp:
            data.append(json.load(fp))
            if debug:
                dir_setting = jmespath.search('jobs[*]."job options".directory', data[-1])
                print(fn, len(dir_setting), set(dir_setting))

    print("Found for", globpatt, len(data), "tests")
    return data
