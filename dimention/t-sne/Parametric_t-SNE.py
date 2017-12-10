# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 05:15:48 2017

@author: Terada
"""

import os
from matplotlib import pyplot as plt
import numpy as np
import keras
from keras import backend as K
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD
from keras.utils import np_utils
from keras.objectives import categorical_crossentropy
from keras.datasets import mnist

batch_size = 5000

(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train = X_train.reshape(-1, 784)
X_test = X_test.reshape(-1, 784)
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')

def Hbeta(D, beta):
    P = np.exp(-D * beta)
    sumP = np.sum(P)
    H = np.log(sumP) + beta * np.sum(np.multiply(D, P)) / sumP
    P = P / sumP
    return H, P


def x2p(X, u=15, tol=1e-4, print_iter=500, max_tries=50, verbose=0):
    # Initialize some variables
    n = X.shape[0]                     # number of instances
    P = np.zeros((n, n))               # empty probability matrix
    beta = np.ones(n)                  # empty precision vector
    logU = np.log(u)                   # log of perplexity (= entropy)
    
    # Compute pairwise distances
    if verbose > 0: print('Computing pairwise distances...')
    sum_X = np.sum(np.square(X), axis=1)
    # note: translating sum_X' from matlab to numpy means using reshape to add a dimension
    D = sum_X + sum_X[:,None] + -2 * X.dot(X.T)

    # Run over all datapoints
    if verbose > 0: print('Computing P-values...')
    for i in range(n):
        
        if verbose > 1 and print_iter and i % print_iter == 0:
            print('Computed P-values {} of {} datapoints...'.format(i, n))
        
        # Set minimum and maximum values for precision
        betamin = float('-inf')
        betamax = float('+inf')
        
        # Compute the Gaussian kernel and entropy for the current precision
        indices = np.concatenate((np.arange(0, i), np.arange(i + 1, n)))
        Di = D[i, indices]
        H, thisP = Hbeta(Di, beta[i])
        
        # Evaluate whether the perplexity is within tolerance
        Hdiff = H - logU
        tries = 0
        while abs(Hdiff) > tol and tries < max_tries:
            
            # If not, increase or decrease precision
            if Hdiff > 0:
                betamin = beta[i]
                if np.isinf(betamax):
                    beta[i] *= 2
                else:
                    beta[i] = (beta[i] + betamax) / 2
            else:
                betamax = beta[i]
                if np.isinf(betamin):
                    beta[i] /= 2
                else:
                    beta[i] = (beta[i] + betamin) / 2
            
            # Recompute the values
            H, thisP = Hbeta(Di, beta[i])
            Hdiff = H - logU
            tries += 1
        
        # Set the final row of P
        P[i, indices] = thisP
        
    if verbose > 0: 
        print('Mean value of sigma: {}'.format(np.mean(np.sqrt(1 / beta))))
        print('Minimum value of sigma: {}'.format(np.min(np.sqrt(1 / beta))))
        print('Maximum value of sigma: {}'.format(np.max(np.sqrt(1 / beta))))
    
    return P, beta

def compute_joint_probabilities(samples, batch_size=5000, d=2, perplexity=30, tol=1e-5, verbose=0):
    v = d - 1
    
    # Initialize some variables
    n = samples.shape[0]
    batch_size = min(batch_size, n)
    
    # Precompute joint probabilities for all batches
    if verbose > 0: print('Precomputing P-values...')
    batch_count = int(n / batch_size)
    P = np.zeros((batch_count, batch_size, batch_size))
    for i, start in enumerate(range(0, n - batch_size + 1, batch_size)):   
        curX = samples[start:start+batch_size]                   # select batch
        P[i], beta = x2p(curX, perplexity, tol, verbose=verbose) # compute affinities using fixed perplexity
        P[i][np.isnan(P[i])] = 0                                 # make sure we don't have NaN's
        P[i] = (P[i] + P[i].T) # / 2                             # make symmetric
        P[i] = P[i] / P[i].sum()                                 # obtain estimation of joint probabilities
        P[i] = np.maximum(P[i], np.finfo(P[i].dtype).eps)

    return P

P = compute_joint_probabilities(X_train, batch_size=batch_size, verbose=2)
np.save('P.npy', P)

# P is the joint probabilities for this batch (Keras loss functions call this y_true)
# activations is the low-dimensional output (Keras loss functions call this y_pred)
def tsne(P, activations):
#     d = K.shape(activations)[1]
    d = 2 # TODO: should set this automatically, but the above is very slow for some reason
    n = batch_size # TODO: should set this automatically
    v = d - 1.
    eps = K.variable(10e-15) # needs to be at least 10e-8 to get anything after Q /= K.sum(Q)
    sum_act = K.sum(K.square(activations), axis=1)
    Q = K.reshape(sum_act, [-1, 1]) + -2 * K.dot(activations, K.transpose(activations))
    Q = (sum_act + Q) / v
    Q = K.pow(1 + Q, -(v + 1) / 2)
    Q *= K.variable(1 - np.eye(n))
    Q /= K.sum(Q)
    Q = K.maximum(Q, eps)
    C = K.log((P + eps) / (Q + eps))
    C = K.sum(P * C)
    return C

model = Sequential()
model.add(Dense(500, activation='relu', input_shape=(X_train.shape[1],)))
model.add(Dense(500, activation='relu'))
model.add(Dense(2000, activation='relu'))
model.add(Dense(2))
sgd = SGD(lr=0.1)
model.compile(loss=tsne, optimizer=sgd)

Y_train = P.reshape(X_train.shape[0], -1)
print(X_train.shape)
print(Y_train.shape)

model.fit(X_train, Y_train, batch_size=batch_size, shuffle=False, nb_epoch=100)


def plot_model(embedding, labels):
    fig = plt.figure(figsize=(8,8))
    plt.scatter(embedding[:,0], embedding[:,1], marker='o', s=1, edgecolor='', c=labels)
    fig.tight_layout()
    
from matplotlib.lines import Line2D
def plot_differences(embedding, actual, lim=1000):
    fig = plt.figure(figsize=(8,8))
    ax = fig.gca()
    for a, b in zip(embedding, actual)[:lim]:
        ax.add_line(Line2D((a[0], b[0]), (a[1], b[1]), linewidth=1))
    ax.autoscale_view()
    plt.show()

from tsne import bh_sne
X_2d = bh_sne(X_train.astype(np.float64))
print(X_2d.shape)

encoder = Sequential()
encoder.add(Dense(500, activation='relu', input_shape=(X_train.shape[1],)))
encoder.add(Dense(500, activation='relu'))
encoder.add(Dense(2000, activation='relu'))
encoder.add(Dense(2))
encoder.compile(loss='mse', optimizer='rmsprop')

encoder.fit(X_train, X_2d, nb_epoch=100, verbose=2)
plot_model(encoder.predict(X_train), y_train)
plot_differences(encoder.predict(X_train), X_2d)



# around 600K parameters
nb_filters = 32
nb_pool = 2
nb_conv = 3
conv = Sequential()
conv.add(Convolution2D(nb_filters, nb_conv, nb_conv, input_shape=(1, 28, 28)))
conv.add(Activation('relu'))
conv.add(Convolution2D(nb_filters, nb_conv, nb_conv))
conv.add(Activation('relu'))
conv.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
conv.add(Dropout(0.25))
conv.add(Flatten())
conv.add(Dense(128))
conv.add(Activation('relu'))
conv.add(Dense(2))
conv.compile(loss='mean_squared_error', optimizer='rmsprop')


X_train_conv = X_train.reshape(-1, 1, 28, 28)
conv.fit(X_train_conv, X_2d, nb_epoch=100)
plot_model(conv, X_train_conv, y_train)

plot_differences(conv, X_train_conv, X_2d)


# around 1.2M parameters
decoder = Sequential()
decoder.add(Dense(2000, activation='relu', input_shape=(2,)))
decoder.add(Dense(500, activation='relu'))
decoder.add(Dense(500, activation='relu'))
decoder.add(Dense(X_train.shape[1]))
decoder.compile(loss='mse', optimizer='rmsprop')

decoder.fit(X_2d, X_train, nb_epoch=100, verbose=2)


def make_mosaic(images_flat, n):
    nx = ny = n
    w = h = int(np.sqrt(len(images_flat[0])))
    images = images_flat.reshape(-1, h, w)
    image_gen = iter(images)
    mosaic = np.empty((h*ny, w*nx))
    for i in range(ny):
        for j in range(nx):
            mosaic[(nx-i-1)*w:(nx-i)*w, j*h:(j+1)*h] = next(image_gen)
    return mosaic

from cStringIO import StringIO
import PIL.Image
import IPython.display
import shutil
def showarray(a, fmt='png', filename=None):
    a = np.uint8(np.clip(a, 0, 255))
    image_data = StringIO()
    PIL.Image.fromarray(a).save(image_data, fmt)
    IPython.display.display(IPython.display.Image(data=image_data.getvalue()))
    if filename is not None:
        with open(filename, 'w') as f:
            image_data.seek(0)
            shutil.copyfileobj(image_data, f)

showarray(255 * make_mosaic(X_train, 12))
showarray(255 * make_mosaic(decoder.predict(X_2d), 12))

n = X_train.shape[1]
ae = Sequential()
ae.add(Dense(500, activation='relu', weights=encoder.layers[0].get_weights(), input_shape=(n,)))
ae.add(Dense(500, activation='relu', weights=encoder.layers[1].get_weights()))
ae.add(Dense(2000, activation='relu', weights=encoder.layers[2].get_weights()))
ae.add(Dense(2, weights=encoder.layers[3].get_weights()))
ae.add(Dense(2000, activation='relu', weights=decoder.layers[0].get_weights()))
ae.add(Dense(500, activation='relu', weights=decoder.layers[1].get_weights()))
ae.add(Dense(500, activation='relu', weights=decoder.layers[2].get_weights()))
ae.add(Dense(n, weights=decoder.layers[3].get_weights()))
ae.compile(loss='mse', optimizer='rmsprop')
ae.fit(X_train, X_train, nb_epoch=100, verbose=2, batch_size=32)

decoded = ae.predict(X_train)
showarray(255 * make_mosaic(decoded, 12))

import theano
def get_submodel(model, start, end):
    return theano.function([model.layers[start].input],
                          model.layers[end].get_output(train=False),
                          allow_input_downcast=True)
def get_encoder(ae):
    return get_submodel(ae, 0, (len(ae.layers) / 2) - 1)
def get_decoder(ae):
    return get_submodel(ae, len(ae.layers) / 2, (len(ae.layers) / 2) - 1) # this doesn't work


ae_encoder = get_encoder(ae)

encoded = encoder.predict(X_train)
ae_encoded = ae_encoder(X_train)


plot_differences(encoded, ae_encoded, lim=1000)
plot_model(encoded, y_train)
plot_model(ae_encoded, y_train)


ae_decoder = Sequential()
ae_decoder.add(Dense(2000, activation='relu', weights=ae.layers[4].get_weights(), input_shape=(2,)))
ae_decoder.add(Dense(500, activation='relu', weights=ae.layers[5].get_weights()))
ae_decoder.add(Dense(500, activation='relu', weights=ae.layers[6].get_weights()))
ae_decoder.add(Dense(X_train.shape[1], weights=ae.layers[7].get_weights()))
ae_decoder.compile(loss='mse', optimizer='rmsprop')


def sample_grid(model, example_data, filename=None, n=128):
    x = np.linspace(example_data[:,0].min(), example_data[:,0].max(), n)
    y = np.linspace(example_data[:,1].min(), example_data[:,1].max(), n)
    xv, yv = np.meshgrid(x, y)
    samples_encoded = np.array(zip(xv.flatten(), yv.flatten()))
    samples_decoded = model.predict(samples_encoded)
    showarray(255 * make_mosaic(samples_decoded, n), filename=filename)


sample_grid(decoder, encoded, filename='output-orig.png')
sample_grid(ae_decoder, ae_encoded, filename='output-finer.png')

n = X_train.shape[1]
ae_scratch = Sequential()
ae_scratch.add(Dense(500, activation='relu', input_shape=(n,)))
ae_scratch.add(Dense(500, activation='relu'))
ae_scratch.add(Dense(2000, activation='relu'))
ae_scratch.add(Dense(2))
ae_scratch.add(Dense(2000, activation='relu'))
ae_scratch.add(Dense(500, activation='relu'))
ae_scratch.add(Dense(500, activation='relu'))
ae_scratch.add(Dense(n))
ae_scratch.compile(loss='mse', optimizer='rmsprop')

ae_scratch.fit(X_train, X_train, nb_epoch=300, verbose=2)

plt.figure(figsize=(10,6))
plt1, = plt.plot(ae_scratch.history.history['loss'][:200], label='Vanilla AE')
plt2, = plt.plot(decoder.history.history['loss'], label='t-SNE Generator')
plt3, = plt.plot(range(100, 200), ae.history.history['loss'], label='t-SNE AE')
plt.legend(handles=[plt1, plt2, plt3])
plt.xlabel('Epochs')
plt.ylabel('Reconstruction Loss (MSE)')
plt.plot(encoder.history.history['loss'])

ae_scratch_encoder = get_encoder(ae_scratch)
ae_scratch_encoded = ae_scratch_encoder(X_train)

ae_scratch_decoder = Sequential()
ae_scratch_decoder.add(Dense(2000, activation='relu', weights=ae_scratch.layers[4].get_weights(), input_shape=(2,)))
ae_scratch_decoder.add(Dense(500, activation='relu', weights=ae_scratch.layers[5].get_weights()))
ae_scratch_decoder.add(Dense(500, activation='relu', weights=ae_scratch.layers[6].get_weights()))
ae_scratch_decoder.add(Dense(X_train.shape[1], weights=ae_scratch.layers[7].get_weights()))
ae_scratch_decoder.compile(loss='mse', optimizer='rmsprop')

sample_grid(ae_scratch_decoder, ae_scratch_encoded, filename='output-scratch.png')

if __name__ == "__main__":
    


    plt.show()
