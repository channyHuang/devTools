import torch

def save_checkpoint(state,filename):
    torch.save(state, filename)
    print('Saved training state as %s'%filename)

def load_checkpoint(path):
    checkpoint = torch.load(path)
    return checkpoint

def validate(model, criterion, validation_loader):
  total_loss = 0
  total_acc = 0
  model.train()
  for batch_idx, data in enumerate(validation_loader):
    target = data
    if torch.cuda.is_available():
      data = data.cuda()
      target = target.cuda()
    output = model(data)
    loss = criterion(output, target).item()

    total_loss+=loss
    accuracy = 0
    total_acc+=accuracy
  return total_loss, total_acc