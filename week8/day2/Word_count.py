from mrjob.job import MRJob

class WordCount(MRJob):

    def mapper(self, _, line):
        words = line.split()
        for word in words:
            if word.isalpha() and len(word) > 0:
                yield word[0].lower(), 1

    def reducer(self, letter, counts):
        yield letter, sum(counts)

if __name__ == '__main__':
    WordCount.run()
