import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter, median_filter

def plot(image, result):
    plt.subplot(121)
    plt.imshow(image[0].permute(1,2,0))
    plt.subplot(122)
    plt.imshow(result)
    plt.show()

def Filter(score_map, type=0):
    '''
    Parameters
    ----------
    score_map : score map as tensor or ndarray
    type : Int, optional
            DESCRIPTION. The values are:
            0 = Gaussian
            1 = Median

    Returns
    -------
    score: Filtered score

    '''
    if type ==0:
        score = gaussian_filter(score_map, sigma=4)
    if type == 1:
        score = median_filter(score_map, size=3)
    return score