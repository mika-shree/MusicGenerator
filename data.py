import os
from io import open
import torch
import regex as re

class Dictionary(object):
    def __init__(self):
        self.word2idx = {}
        self.idx2word = []

    def createWordToIndex(self):
        self.word2idx = {u: i for i, u in enumerate(self.idx2word)}

    def __len__(self):
        return len(self.idx2word)


class Corpus(object):
    def __init__(self, path):
        self.dictionary = Dictionary()
        self.train = self.tokenize(os.path.join(path, 'train.abc'))
        self.valid = self.tokenize(os.path.join(path, 'valid.abc'))
        self.test = self.tokenize(os.path.join(path, 'test.abc'))

    def extract_song_snippet(self, text):
        pattern = '(^|\n\n)(.*?)\n\n'
        search_results = re.findall(pattern, text, overlapped=True, flags=re.DOTALL)
        songs = [song[1] for song in search_results]
        return songs

    def tokenize(self, path):
        """Tokenizes a text file."""
        assert os.path.exists(path)

        songs = []
        with open(path, 'r', encoding="utf8") as f:
            text = f.read()
            songs = self.extract_song_snippet(text)
        songs_joined = "\n\n".join(songs)
        # Find all unique characters in the joined string
        self.dictionary.idx2word = sorted(set(songs_joined))
        # Add words to the dictionary
        self.dictionary.createWordToIndex()

        # Tokenize file content
        idss = []
        for s in songs:
            ids = []
            for note in s:
                ids.append(self.dictionary.word2idx[note])
            idss.append(torch.tensor(ids, dtype=torch.int64))
        ids = torch.cat(idss)
        return ids