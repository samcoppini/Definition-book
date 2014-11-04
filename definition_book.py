from wordnik import *
import codecs
import random

def make_sentence():
	rand_sent  = "The "
	rand_sent += get_sentence.getRandomWord(includePartOfSpeech="adjective").word
	rand_sent += " "+get_sentence.getRandomWord(includePartOfSpeech="noun").word
	rand_sent += " "+get_sentence.getRandomWord(includePartOfSpeech="verb-intransitive").word
	rand_sent += " "+get_sentence.getRandomWord(includePartOfSpeech="preposition").word
	rand_sent += " the "
	rand_sent += get_sentence.getRandomWord(includePartOfSpeech="adjective").word
	rand_sent += " "+get_sentence.getRandomWord(includePartOfSpeech="noun").word
	return rand_sent

apiUrl = 'http://api.wordnik.com/v4'
apiKey = '5a5dc229807e6f9ac7100019db5059207afa044bc21023efa'
client = swagger.ApiClient(apiKey, apiUrl)

get_sentence = WordsApi.WordsApi(client)
wordApi = WordApi.WordApi(client)
title = make_sentence()
novel = title.split()

defined_words = ["you","are","unfamiliar","with","the","word","its","definition","is"]

words_to_write = 50000

while len(novel) < words_to_write:
	random_index = random.randint(0,len(novel)-1)
	random_word = novel[random_index]
	if random_word not in defined_words:
		defined_words.append(random_word)
		if random_word[-1] == ".":
			random_word = random_word[:-1]
		try:
			word_definition = wordApi.getDefinitions(random_word, limit=1)
			if word_definition is not None:
				word_definition = word_definition[0].text
				to_add = "(If you are unfamiliar with the word '" + random_word + "', its definition is \"" + word_definition +"\")"
				novel = novel[:random_index+1] + to_add.split() + novel[random_index+1:]
				print str(len(novel)) + " words written"
		except:
			print "Took too long to respond"
novel = " ".join(novel)+"."
file = codecs.open(title.capitalize()+".txt","w",encoding='utf-8')
file.write(novel)
file.close()

end_program = raw_input("Novel written successfully!")
