#!/usr/bin/env python
# coding: utf-8

# In[23]:


# All general imports
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import LabelBinarizer 

import tensorflow.keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Input, Embedding, Reshape, Conv2D, MaxPool2D, Concatenate, Flatten, Dropout, Dense, Bidirectional, GlobalAveragePooling1D, GRU, GlobalMaxPooling1D, concatenate
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import LSTM, GRU, Conv1D, MaxPool1D, Activation

from tensorflow.keras.models import Model, Sequential

from tensorflow.keras.layers import Dense, Input, Embedding, Dropout, Activation, Conv1D, Softmax
from tensorflow.keras import initializers, regularizers, constraints, optimizers, layers

from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

from sklearn.model_selection import KFold, cross_val_predict, cross_val_score
from sklearn.metrics import classification_report, accuracy_score
from sklearn import linear_model

import io, os, gc

path = "E:/4thSem/inno_lab"

# In[30]:


# Declaring Global Variable
def get_parameters(embedding_matrix):
    MAX_SEQUENCE_LENGTH = 15
    NUM_CLASSES = 2
    MAX_NUM_WORDS = embedding_matrix.shape[0]
    NUM_EMBEDDING_DIM = embedding_matrix.shape[1]
    return MAX_SEQUENCE_LENGTH, NUM_CLASSES, MAX_NUM_WORDS, NUM_EMBEDDING_DIM


# In[22]:


def import_dataset():
    # Import the dataset
    question_df = pd.read_csv(path + '/question_data.csv')
    print(question_df.head())
    question_test = pd.read_csv(path + '/question_test.csv')
    x_train = question_df.question
    y_train = question_df.label
    x_test = question_test.question
    y_test = question_test.label
    return x_train, y_train, x_test, y_test


# In[3]:


def get_tokenizer(vocabulary_size, x_train, x_test):
    train_lst = x_train.tolist()
    test_lst = x_test.tolist()
    uq_tr = list(set(train_lst))
    uq_ts = list(set(test_lst))
    total_dataset = uq_tr + uq_ts
    print('Dataset length is', len(total_dataset))
    # Training the Tokenizer now
    print('Training tokenizer...')
    tokenizer = Tokenizer(num_words= vocabulary_size)
    tweet_text = []
    print('Read {} Sentences'.format(len(total_dataset)))
    tokenizer.fit_on_texts(total_dataset)
    return tokenizer


# In[4]:


# For getting the embedding matrix
def get_embeddings(x_train, x_test):
  print('Generating embeddings matrix...')
  embeddings_file = path + '/glove.6B.50d.txt'
  embeddings_index = dict()
  with open(embeddings_file, 'r', encoding="utf-8") as infile:
    for line in infile:
      values = line.split()
      word = values[0]
      vector = np.asarray(values[1:], "float32")
      embeddings_index[word] = vector
	# create a weight matrix for words in training docs
  vocabulary_size = len(embeddings_index)
  embeddinds_size = list(embeddings_index.values())[0].shape[0]
  print('Vocabulary = {}, embeddings = {}'.format(vocabulary_size, embeddinds_size))
  tokenizer = get_tokenizer(vocabulary_size, x_train, x_test)
  embedding_matrix = np.zeros((vocabulary_size, embeddinds_size))
  considered = 0
  total = len(tokenizer.word_index.items())
  for word, index in tokenizer.word_index.items():
    if index > vocabulary_size - 1:
      print(word, index)
      continue
    else:
      embedding_vector = embeddings_index.get(word)
      if embedding_vector is not None:
        embedding_matrix[index] = embedding_vector
        considered += 1
  print('Considered ', considered, 'Left ', total - considered)			
  return embedding_matrix, tokenizer


# In[5]:


def get_data(tokenizer, MAX_LENGTH, input_texts, input_labels):
    print('Loading data')
    X, Y = [], []
    X = input_texts.tolist()
    Y = input_labels.tolist()
    assert len(X) == len(Y)
    sequences_1 = tokenizer.texts_to_sequences(X)
    X = pad_sequences(sequences_1, maxlen=MAX_LENGTH)
    Y = np.array(Y)
    return X, Y


# In[33]:


# Propose a deep network architecture
def get_multicnn_model(embedding_matrix):
    # Getting all the parameters
    MAX_SEQUENCE_LENGTH, NUM_CLASSES, MAX_NUM_WORDS, NUM_EMBEDDING_DIM = get_parameters(embedding_matrix)
    #print('Getting Text CNN model...')
    filter_sizes = [2, 3, 5]
    num_filters = 128 #Hyperparameters 32,64,128; 0.2,0.3,0.4
    drop = 0.4

    top_input = Input(
        shape=(MAX_SEQUENCE_LENGTH, ), 
        dtype='int32')

    embedding_layer = Embedding(
        MAX_NUM_WORDS, NUM_EMBEDDING_DIM, weights = [embedding_matrix], trainable=True)

    top_embedded = embedding_layer(
        top_input)

    reshape = Reshape((MAX_SEQUENCE_LENGTH, NUM_EMBEDDING_DIM, 1))(top_embedded)
    conv_0 = Conv2D(num_filters, kernel_size=(filter_sizes[0], NUM_EMBEDDING_DIM),  padding='valid', kernel_initializer='normal', activation='relu')(reshape)
    conv_1 = Conv2D(num_filters, kernel_size=(filter_sizes[1], NUM_EMBEDDING_DIM),  padding='valid', kernel_initializer='normal', activation='relu')(reshape)
    conv_2 = Conv2D(num_filters, kernel_size=(filter_sizes[2], NUM_EMBEDDING_DIM),  padding='valid', kernel_initializer='normal', activation='relu')(reshape)
    maxpool_0 = MaxPool2D(pool_size=(MAX_SEQUENCE_LENGTH - filter_sizes[0] + 1, 1), strides=(1,1), padding='valid')(conv_0)
    maxpool_1 = MaxPool2D(pool_size=(MAX_SEQUENCE_LENGTH - filter_sizes[1] + 1, 1), strides=(1,1), padding='valid')(conv_1)
    maxpool_2 = MaxPool2D(pool_size=(MAX_SEQUENCE_LENGTH - filter_sizes[2] + 1, 1), strides=(1,1), padding='valid')(conv_2)
    concatenated_tensor = Concatenate(axis=1)([maxpool_0, maxpool_1, maxpool_2])
    flatten = Flatten()(concatenated_tensor)
    dropout = Dropout(drop)(flatten)
    predictions = Dense(units=NUM_CLASSES, activation='sigmoid')(dropout)

    model = Model(
        inputs=[top_input], 
        outputs=predictions)
    return model


# In[36]:


def train():
    x_train, y_train, x_test, y_test = import_dataset()
    embedding_matrix, tokenizer = get_embeddings(x_train, x_test)
    # Getting all the parameters
    MAX_SEQUENCE_LENGTH, NUM_CLASSES, MAX_NUM_WORDS, NUM_EMBEDDING_DIM = get_parameters(embedding_matrix)
    # Convert input data to tokens
    X, Y = get_data(tokenizer, MAX_LENGTH, x_train, y_train)
    x_test, y_test = get_data(tokenizer, MAX_LENGTH, x_test, y_test)
    # Converting train to categorical
    y_cat = tensorflow.keras.utils.to_categorical(Y)
    print(y_cat)
    # Preparing to train
    model = get_multicnn_model(embedding_matrix)
    print(model.summary())
    
    # Splitting the data
    from sklearn.model_selection import train_test_split
    VALIDATION_RATIO = 0.1
    RANDOM_STATE = 9527
    x_train, x_val,     y_train, y_val =         train_test_split(
            X, y_cat, 
            test_size=VALIDATION_RATIO, 
            random_state=RANDOM_STATE
    )
    # Setting the optimizer
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
    lr = 1e-3
    opt = Adam(lr=lr, decay=lr/50)
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy'])
    
    # Fitting the Model
    BATCH_SIZE = 5
    NUM_EPOCHS = 3
    stop = EarlyStopping(monitor='val_loss', patience=0.001)
    checkpointer = ModelCheckpoint (filepath=path + '/dbsentence.h5', verbose=1, save_best_only=True)
    history = model.fit(x=x_train,
                        y=y_train,
                        batch_size=BATCH_SIZE,
                        epochs=NUM_EPOCHS,
                        validation_data=(
                          x_val, 
                          y_val
                        ),
                        shuffle=True,
                        callbacks=[stop, checkpointer],
              )
    # Predicting on test set
    predictions = model.predict(x_test)
    y_pred = [idx for idx in np.argmax(predictions, axis=1)]
    print('Accuracy is')
    print(accuracy_score(y_test, y_pred)*100)


# In[37]:


#train()


# In[38]:


def get_inference(query, embedding_matrix, tokenizer, MAX_LENGTH):
    model = get_multicnn_model(embedding_matrix)
    model.load_weights(path + '/dbsentence.h5')
    # Preparing the query
    in_query = []
    in_query.append(query)
    sequences_1 = tokenizer.texts_to_sequences(in_query)
    in_query = pad_sequences(sequences_1, maxlen=MAX_LENGTH)
    # Online Inferencing
    predictions = model.predict(in_query)
    y_pred = [idx for idx in np.argmax(predictions, axis=1)]
    return y_pred[0]


# In[40]:

# getting embedding matrix
# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
# MAX_LENGTH = 15
# x_train, y_train, x_test, y_test = import_dataset()
# embedding_matrix, tokenizer = get_embeddings(x_train, x_test)
# query = input('> ')
# print(get_inference(query, embedding_matrix, tokenizer, MAX_LENGTH))

