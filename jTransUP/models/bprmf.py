import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable as V

from jTransUP.utils.misc import to_gpu

def build_model(FLAGS, user_total, item_total):
    model_cls = BPRMF
    return model_cls(
                embedding_size = FLAGS.embedding_size,
                user_total = user_total,
                item_total = item_total
    )

class BPRMF(nn.Module):
    def __init__(self,
                embedding_size,
                user_total,
                item_total,
                ):
        super(BPRMF, self).__init__()
        self.embedding_size = embedding_size
        self.user_total = user_total
        self.item_total = item_total

        user_weight = torch.FloatTensor(self.user_total, self.embedding_size)
        item_weight = torch.FloatTensor(self.item_total, self.embedding_size)
        nn.init.xavier_uniform(user_weight)
        nn.init.xavier_uniform(item_weight)
        # init user and item embeddings
        self.user_embeddings = nn.Embedding(self.user_total, self.embedding_size)
        self.item_embeddings = nn.Embedding(self.item_total, self.embedding_size)
        self.user_embeddings.weight = nn.Parameter(user_weight)
        self.item_embeddings.weight = nn.Parameter(item_weight)
        normalize_user_emb = F.normalize(self.user_embeddings.weight.data, p=2, dim=1)
        normalize_item_emb = F.normalize(self.item_embeddings.weight.data, p=2, dim=1)
        self.user_embeddings.weight.data = normalize_user_emb
        self.item_embeddings.weight.data = normalize_item_emb

        self.user_embeddings = to_gpu(self.user_embeddings)
        self.item_embeddings = to_gpu(self.item_embeddings)

    def forward(self, u_ids, i_ids):
        u_e = self.user_embeddings(to_gpu(V(torch.LongTensor(u_ids))))
        i_e = self.item_embeddings(to_gpu(V(torch.LongTensor(i_ids))))
        return torch.bmm(u_e.unsqueeze(1), i_e.unsqueeze(2)).squeeze()