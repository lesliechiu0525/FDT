import torch
#tensor版计算AUC
def auc(y_pred,y_true):
    sorted_y, sorted_indices = torch.sort(y_pred, descending=True)
    sorted_labels = y_true[sorted_indices]
    tp = sorted_labels.float().cumsum(dim=0)
    fp = (1 - sorted_labels).float().cumsum(dim=0)
    tn = fp[-1] - fp
    fn = tp[-1] - tp
    tpr = tp / (tp + fn)
    fpr = fp / (fp + tn)
    tpr = torch.cat((torch.tensor([0.0]), tpr))
    fpr = torch.cat((torch.tensor([0.0]), fpr))
    tpr_diff = torch.diff(tpr, dim=0)
    fpr_diff = torch.diff(fpr, dim=0)
    auc_value = (tpr_diff * (fpr[1:] + fpr[:-1]) / 2).sum()
    return auc_value.item()