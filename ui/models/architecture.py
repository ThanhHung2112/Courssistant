import numpy as np 
import torch.nn as nn

class IntentClassifier(nn.Module):
    def __init__(self, bert_model, num_classes):
        super(IntentClassifier, self).__init__()
        self.bert = bert_model
        self.relu1 = nn.ReLU()
        self.relu2 = nn.ReLU()
        self.fc = nn.Linear(self.bert.config.hidden_size, num_classes)

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids, attention_mask=attention_mask)
        pooled_output = outputs.last_hidden_state[:, 0, :]
        x = self.relu1(pooled_output)
        x = self.relu2(x)
        logits = self.fc(x)
        return logits
    
