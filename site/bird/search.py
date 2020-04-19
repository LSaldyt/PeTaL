from modules.libraries.natural_language.cleaner import Cleaner
from pprint import pprint

import pickle
import time

def search(query):
    cleaner = Cleaner()
    start = time.time()
    with open('../pipeline/data/index', 'rb') as infile:
        index = pickle.load(infile)
    load = time.time()
    print('Loading index took ', round(load - start, 6), 'seconds')
    results = []
    for term in cleaner.clean(query):
        term_results = index[term]
        result = term_results[-1][-1]
        print('Result for "' + term + '": document ', result, ' is the best match, with ', result[1], ' hits')
        for subresult in term_results:
            print('    {} w/ {},{} hits'.format(subresult[2], subresult[0], subresult[1]))
        results.append(term_results)
    done = time.time()
    print('Searching index took ', round(done - load, 6), 'seconds')
    return done - load, results

def main():
    search('megaptera')

if __name__ == '__main__':
    main()