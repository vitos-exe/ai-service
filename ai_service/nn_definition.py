from torch import nn
from torch.nn.functional import softmax


class SentimentDNN(nn.Module):
    name = "sentiment-dnn"

    def __init__(
        self, input_size=300, hidden_sizes=(64, 32), dropout_rates=(0, 0), output_size=4
    ):
        super(SentimentDNN, self).__init__()

        layers = []
        for i, hidden_size in enumerate(hidden_sizes):
            layers.append(
                nn.Linear(input_size if i == 0 else hidden_sizes[i - 1], hidden_size)
            )
            layers.append(nn.ReLU())
            if dropout_rates[i] > 0:
                layers.append(nn.Dropout(dropout_rates[i]))

        layers.append(nn.Linear(hidden_sizes[-1], output_size))
        self.model = nn.Sequential(*layers)

    def forward(self, x):
        y = self.model(x)
        return softmax(y, dim=1)
