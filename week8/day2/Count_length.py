from mrjob.job import MRJob

class WordCountLength(MRJob):

    def mapper(self, _, line):
        words = line.split()
        for word in words:
            if len(word) == 5:
                yield word, 1

    def reducer(self, word, counts):
        yield word, sum(counts)

if __name__ == '__main__':
    WordCountLength.run()
