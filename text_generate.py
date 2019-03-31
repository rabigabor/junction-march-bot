import numpy as np


def make_pairs(corpus):
	for i in range(len(corpus)-1):
		yield (corpus[i], corpus[i+1])

def prepare_model(corpus_path):
	quotes = open(corpus_path, encoding='utf8').read()
	corpus = quotes.split()

	pairs = make_pairs(corpus)

	word_dict = {}

	for word_1, word_2 in pairs:
		if word_1 in word_dict.keys():
			word_dict[word_1].append(word_2)
		else:
			word_dict[word_1] = [word_2]

	return quotes, word_dict

def generate_quote(min_length = 30):

	words = list(word_dict.keys())

	first_word = "[START]" #np.random.choice(words)

	while first_word.islower() or first_word == "[END]":
		first_word = np.random.choice(words)

	generated_words = [np.random.choice(word_dict["[START]"])]

	while True:
		next_word = np.random.choice(word_dict[generated_words[-1]])
		if next_word == "[END]":
			break
		else:
			generated_words.append(next_word)

	generated_quote = " ".join(generated_words)

	if len(generated_quote) < min_length:
		return generate_quote(word_dict, min_length-1)
	else:
		return generated_quote

def pick_random_quote(min_length = 30):

	random_quote = np.random.choice(quotes.split("\n"))
	return random_quote[8:-5]


quotes, word_dict = prepare_model('unique_quotes.txt')