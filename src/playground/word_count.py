from map_reduce import Mapper, Reducer, Shuffler
from collections import defaultdict


def group_by_word(words):
    result = defaultdict(list)

    for (word, c) in words:
        result[word].append(c)

    return result


def map_word(word):
    return word, 1


def reduce_count(word, sequence):
    return word, sum(sequence)


def word_count(document):
    mapper = Mapper(map_word, document)
    shuffler = Shuffler(group_by_word, mapper.run())
    reducer = Reducer(reduce_count, shuffler.run().iteritems())

    return reducer.run()


def main():
    test = "it it it it ti ti ti ti"
    print(word_count(test.strip().split(" ")))


if __name__ == '__main__':
    main()
