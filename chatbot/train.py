import json
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from nltk_utils import tokenize, stem, bag_of_words
from model import NeuralNet

class ChatDataset(Dataset):
    def __init__(self, x_train, y_train):
        self.n_samples = len(x_train)
        self.x_data = x_train
        self.y_data = y_train
    
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples

def load_data(file_path):
    with open(file_path, 'r') as f:
        intents = json.load(f)
    return intents

def preprocess_data(intents):
    all_words = []
    tags = []
    xy = []
    ignore_words = ['?', '!', '.', ',']

    for intent in intents['intents']:
        tag = intent['tag']
        if tag not in tags:
            tags.append(tag)
        for pattern in intent['patterns']:
            w = tokenize(pattern)
            all_words.extend(w)
            xy.append((w, tag))

    all_words = [stem(w) for w in all_words if w not in ignore_words]
    all_words = sorted(set(all_words))
    tags = sorted(set(tags))

    x_train = []
    y_train = []
    for (pattern_sentence, tag) in xy:
        bag = bag_of_words(pattern_sentence, all_words)
        x_train.append(bag)
        label = tags.index(tag)
        y_train.append(label)

    x_train = np.array(x_train)
    y_train = np.array(y_train)
    return x_train, y_train, all_words, tags

def train_model(x_train, y_train, all_words, tags):
    input_size = len(x_train[0])
    output_size = len(tags)
    hidden_size = 8
    learning_rate = 0.001
    num_epochs = 1000

    dataset = ChatDataset(x_train, y_train)
    train_loader = DataLoader(dataset=dataset, batch_size=8, shuffle=True, num_workers=0)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in range(num_epochs):
        for (words, labels) in train_loader:
            words = words.to(device)
            labels = labels.to(device).long()

            optimizer.zero_grad()
            outputs = model(words)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

        if (epoch+1) % 100 == 0:
            print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

    print(f'Training complete. Final loss: {loss.item():.4f}')

    # Save the model and metadata
    data = {
        'model_state': model.state_dict(),
        'input_size': input_size,
        'output_size': output_size,
        'hidden_size': hidden_size,
        'all_words': all_words,
        'tags': tags
    }

    FILE = 'data.pth'
    torch.save(data, FILE)
    print(f'Model saved to {FILE}')

if __name__ == '__main__':
    file_path = 'C:/Users/manya/OneDrive/Desktop/chatbot/intents.json'  # Update with your actual file path
    intents = load_data(file_path)
    x_train, y_train, all_words, tags = preprocess_data(intents)
    train_model(x_train, y_train, all_words, tags)
