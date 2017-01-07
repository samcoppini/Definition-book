import codecs
import os
import random
import sys

from wordnik import *

def get_word(speech):
	return words_api.getRandomWord(includePartOfSpeech=speech).word

def make_sentence():
	sentence_words = [
		"The", get_word("adjective"), get_word("noun"),
		get_word("verb-intransitive"), get_word("preposition"),
		"the", get_word("adjective"), get_word("noun")]
	return " ".join(sentence_words)

apiUrl = 'http://api.wordnik.com/v4'
apiKey = os.getenv("API_KEY")
client = swagger.ApiClient(apiKey, apiUrl)

words_api = WordsApi.WordsApi(client)
word_api = WordApi.WordApi(client)
title = make_sentence()
novel = title.split()

defined_words = [
	"you", "are", "unfamiliar", "with", "the",
	"word", "its", "definition", "is"
]

if len(sys.argv) > 1:
	words_to_write = int(sys.argv[1])
else:
	words_to_write = 50000

while len(novel) < words_to_write:
	random_index = random.randint(0,len(novel)-1)
	random_word = novel[random_index]
	if random_word not in defined_words:
		defined_words.append(random_word)
		if random_word[-1] == ".":
			random_word = random_word[:-1]
		word_definition = word_api.getDefinitions(random_word, limit=1)
		if word_definition is not None:
			word_definition = word_definition[0].text
			to_add = "(If you are unfamiliar with the word '" + random_word + "', its definition is \"" + word_definition +"\")"
			novel = novel[:random_index+1] + to_add.split() + novel[random_index+1:]
			print(str(len(novel)) + " words written")
novel = " ".join(novel) + "."
file = codecs.open(title.capitalize() + ".txt", "w", encoding='utf-8')
file.write(novel)
file.close()

print("Novel written successfully!")
