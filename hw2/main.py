import torch
import torchtext
from torchtext.vocab import Vectors, GloVe

import math
import numpy as np
import tqdm  # track that progress  

# Batching
from torchtext.data.iterator import BPTTIterator
from torchtext.data import Batch, Dataset

# NamedTensor  
from namedtensor import ntorch
from namedtensor.text import NamedField

# Model Imports  
# from ngram import NGram  
from nnlm import NNLM  
from lstm import LSTM  

def train(model, train_iter, criterion, optimizer, lr=0.0001, weight_decay=0): 
    """Method to train model. Define optimizer = ADAM, Adagrad, etc (e.g. optim.Adam); criterion = torch.nn.NLLLoss()""" 
    x_train, y_train, n_train = model.get_data(train_iter)

    model.train()
    optimizer = optimizer(model.parameters(), lr=lr, weight_decay=weight_decay)

    for ix in range(len(x_train)):
        optimizer.zero_grad()
        x_batch = x_train[ix]; y_batch = y_train[ix]

        probs = model.forward(x_batch)
        loss = criterion(props.log(), y_batch)

        loss.backward()
        optimizer.step()

    return validate(model, x_train, y_train, n_train)


def validate(model, x, y, n_words):
    """Method to evaluate model"""
    model.eval()

    with torch.no_grad():
        criterion = torch.nn.NLLLoss(reduction='sum')
        epoch_loss = 0
        n_correct = 0

        for i in range(len(x)):
            probs = model.forward(x[i])
            epoch_loss += criterion(probs.log(), y[i])
            n_correct += (probs.argmax(dim=1) == y[i]).sum().float()
        loss = epoch_loss / n_words
        return 100. * n_correct / n_words, loss, math.exp(loss)  # perplexity  


def train_val_model(model, n_epochs, criterion, optimizer):  
    """Wrapper to call training and evaluation"""  
    for epoch in range(n_epochs):
        train_acc, train_loss, train_ppl = train(model, train_iter, criterion, optimizer, 0.0001, 0)
        x_val, y_val, n_val = model.get_data(val_iter)
        val_acc, val_loss, val_ppl = validate(model, x_val, y_val, n_val)
        print(f'| Epoch: {epoch+1:02} | Train Acc: {train_acc*100:.2f}% | \
            Train Loss: {train_loss:.3f} | Train Ppl: {train_ppl:.3f} | \
            Val. Acc: {val_acc*100:.2f}% | Val. Loss: {val_loss:.3f} | Val. Ppl: {val_ppl:.3f}')







    