import imageio
import numpy as np
import random
import torch
from torchvision import transforms
from torchvision.utils import save_image

from siren import Siren
from training import Trainer
import util

def encode(image, 
           layer_size = 28, num_layers = 10, w0 = 30.0, w0_initial = 30.0, 
           learning_rate = 2e-4, num_iters = 50000,
           out_name = "./../data/coin"):
    
    seed = random.randint(1, int(1e6))

    # Set up torch and cuda
    dtype = torch.float32
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    torch.set_default_tensor_type('torch.cuda.FloatTensor' if torch.cuda.is_available() else 'torch.FloatTensor')

    # Set random seeds
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

    # Dictionary to register mean values (both full precision and half precision)
    results = {'fp_bpp': [], 'hp_bpp': [], 'fp_psnr': [], 'hp_psnr': []}

    img = transforms.ToTensor()(image).float().to(device, dtype)

    # Setup model
    func_rep = Siren(
        dim_in=2,
        dim_hidden=layer_size,
        dim_out=image.shape[2],
        num_layers=num_layers,
        final_activation=torch.nn.Identity(),
        w0_initial=w0_initial,
        w0=w0
    ).to(device)

    # Set up training
    trainer = Trainer(func_rep, lr=learning_rate)
    coordinates, features = util.to_coordinates_and_features(img)
    coordinates, features = coordinates.to(device, dtype), features.to(device, dtype)

    # Calculate model size. Divide by 8000 to go from bits to kB
    model_size = util.model_size_in_bits(func_rep) / 8000.
    print(f'Model size: {model_size:.1f}kB')
    fp_bpp = util.bpp(model=func_rep, image=img)
    print(f'Full precision bpp: {fp_bpp:.2f}')

    # Train model in full precision
    trainer.train(coordinates, features, num_iters=num_iters)
    print(f'Best training psnr: {trainer.best_vals["psnr"]:.2f}')

    # Log full precision results
    results['fp_bpp'].append(fp_bpp)
    results['fp_psnr'].append(trainer.best_vals['psnr'])

    # Save best model
    torch.save(trainer.best_model, out_name + f'.pt')

    # Update current model to be best model
    # func_rep.load_state_dict(trainer.best_model)

    # # Save full precision image reconstruction
    # with torch.no_grad():
    #     img_recon = func_rep(coordinates).reshape(img.shape[1], img.shape[2], 1).permute(2, 0, 1)
    #     save_image(torch.clamp(img_recon, 0, 1).to('cpu'), f'./fp_reconstruction.png')

    print('encode finished...\n')

def decode(model_name, 
           nWidth = 1920, nHeight = 1080, nChannel = 3, 
           layer_size = 28, num_layers = 10, 
           w0 = 30.0, w0_initial = 30.):
    dtype = torch.float32
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    torch.set_default_tensor_type('torch.cuda.FloatTensor' if torch.cuda.is_available() else 'torch.FloatTensor')

    image = [0] * (nWidth * nHeight * nChannel)
    image = np.array(image)
    image = image.reshape(nHeight, nWidth, nChannel)
    img = transforms.ToTensor()(image).float().to(device, dtype)
    
    coordinates, features = util.to_coordinates_and_features(img)
    coordinates, features = coordinates.to(device, dtype), features.to(device, dtype)

    func_rep = Siren(
        dim_in=2,
        dim_hidden=layer_size,
        dim_out=nChannel,
        num_layers=num_layers,
        final_activation=torch.nn.Identity(),
        w0_initial=w0_initial,
        w0=w0
    ).to(device)
    best_model = torch.load(model_name)
    func_rep.load_state_dict(best_model)

    with torch.no_grad():
        img_recon = func_rep(coordinates).reshape(img.shape[1], img.shape[2], nChannel).permute(2, 0, 1)
        save_image(torch.clamp(img_recon, 0, 1).to('cpu'), f'./../data/coin_fp_reconstruction.png')
    return True

if __name__ == '__main__':
    # image = imageio.imread(f"./../data/gray.jpg")
    image = imageio.imread(f"./../data/rgb.jpg")
    encode(image)

    decode(f"./../data/coin.pt")
