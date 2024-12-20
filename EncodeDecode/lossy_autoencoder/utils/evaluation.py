import IPython
import model.PytorchMsssim as PytorchMsssim
import matplotlib.pyplot as plt
import torchvision.transforms.functional as TF
import torch


def display(x):
    if type(x) is tuple:
        img,out = x
        fig, axes = plt.subplots(ncols=1,nrows=2,figsize=(18,30))
        axes.ravel()[0].imshow(img)
        axes.ravel()[0].set_title('Original')
        axes.ravel()[1].imshow(out)
        axes.ravel()[1].set_title('After Compression')
        plt.show()
    else:
        plt.imshow(x)

def evaluate(model,ds,idx, showImages = False):
    
    x = ds[idx]
    iimg = TF.to_pil_image(x)
    x=x.unsqueeze(0)
    if torch.cuda.is_available():
        x = x.cuda()
    y = model(x)
    oimg = TF.to_pil_image(y.squeeze(0).cpu().detach())
    score = (PytorchMsssim.msssim(x, y).item())
#     print("MSSSIM score is {:.5f}".format(score))
    if showImages:
        display((iimg,oimg))
    return score

def visualize(history):
  plt.figure(figsize=(15,7))
  plt.plot(history['epoch_data'], history['train_losses'],label="Train Loss {:.5f}".format(history['train_losses'][-1]))
  plt.plot(history['epoch_data'], history['val_losses'], label="Validation Loss {:.5f}".format(history['val_losses'][-1]))
#   plt.plot(history['epoch_data'], history['train_accuracy'],label="Train Accuracy {:.5f}".format(history['train_accuracy'][-1]))
#   plt.plot(history['epoch_data'], history['val_accuracy'], label="Validation Accuracy {:.5f}".format(history['val_accuracy'][-1]))
  IPython.display.clear_output(wait=False)
  plt.legend()
  plt.show()
