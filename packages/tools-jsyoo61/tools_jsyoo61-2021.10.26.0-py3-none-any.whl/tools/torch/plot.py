
import matplotlib.pyplot as plt

# %%
def imshow(tensor, **kwargs):
    '''
    tensor of (Channel, width, height)
    '''
    t=tensor.detach().cpu().numpy()
    fig, ax = plt.subplots()
    ax.imshow(t.transpose(1,2,0))

    return fig, ax
