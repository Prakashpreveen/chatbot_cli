import random
import json
import pickle
import numpy as np
import tensorflow as tf

import nltk
from nltk.stem import WordNetLemmatizer


nltk.download('punkt')
lemmatizer = WordNetLemmatizer()

intents = json.loads(open('intents.json').read())

print(intents)

words = []
classes = []
documents = []
ignoreletters = ['!','?',',','.']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        wordlist = nltk.word_tokenize(pattern) # Tokenize the pattern
        words.extend(wordlist) # extend in words=[]
        documents.append((wordlist,intent['tag'])) # Append the wordlist and tag in the documents=[]
        if intent['tag'] not in classes: 
            classes.append(intent('tag')) # If tag is not present append the new tags in classes=[]

words = [lemmatizer.lemmatize(word) for word in words if word not in ignoreletters]
word = sorted(set(words))
classes = sorted(set(classes))

pickle.dump(words,open('words.pkl','wb'))
pickle.dump(classes,open('classes.pkl','wb'))

training = []
outputempty = [0] * len(classes)

for document in documents:
    bag = []
    wordpatterns = document[0]
    wordpatterns = [lemmatizer.lemmatize(word.lower() for word in wordpatterns)] # make all words into lower and lemmatize it eg:running-->run
    for word in words: # checking all words in the words
        bag.append(1) if word in wordpatterns else bag.append(0) # append 1 in the bag=[] if the 'yes' else 0 as 'no'

outputrow = list(outputempty)
outputrow[classes.index(document[1])] = 1
training.append(bag + outputrow)

random.shuffle(training)
training = np.array(training)

trainX = training[:,:len(words)]
trainY = training[:,len(words):]

model = tf.keras.Sequential()
model.add(tf.keras.layer.Dense(128,input_shape=(len(trainX[0]),),activation = 'relu'))
model.add(tf.keras.layer.Dropout(0.5))
model.add(tf.keras.layer.Dense(64,activation = 'relu'))
model.add(tf.keras.layer.Dense(len(trainY[0]),activation='softmax'))

smg = tf.keras.optimizers.SGD(learning_rate=0.01,momentum=0.9,nesterov=True)
model.compile(loss='categorical_crossentropy',optimizer=sgd,metrics=['accuracy'])

hist = model.fit(np.array(trainX), np.array(trainY), epochs=200, batch_size=5, verbose=1)
model.save('chatbot_model.h5', hist)
print('Done')


