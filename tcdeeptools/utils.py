# AUTOGENERATED! DO NOT EDIT! File to edit: 01_utils.ipynb (unless otherwise specified).

__all__ = ['clean', 'get_files_dir', 'get_name_training', 'get_id_training', 'to_byte_tensor', 'to_float_tensor',
           'normalize_tan', 'decode_from_tan', 'loader', 'show_img_from_tensor', 'gradient_flow', 'viz_grad_flow',
           'get_tb_logdir', 'get_identity_training', 'get_tb_writer']

# Cell
import matplotlib.pyplot as plt
import PIL
import torch
import gc
import os


# Cell
def clean():
    gc.collect()
    gc.collect()

# Cell

def get_files_dir(path, ext, debug=False):
    items = []
    for r, d, f in os.walk(path):
            if debug: print(f'In directory {r}: {len(f)} files')
            for file in f:
                for e in ext:
                    if e in file:
                        items.append(r+'/'+file)
                    if debug: print(f'working on img {path+file}')
    return list(set(items))


def get_name_training(prefix, placeholder=True, config='',learner=''):
    id_training = get_id_training(placeholder=placeholder, config=config,learner=learner)
    return f'{id_training}-{prefix}'


def get_id_training(path='./svg', name='', placeholder=True, config='',learner='', params_opt='', params_sched=''):
    files = get_files_dir(path, [''], debug=False)

    index = 0

    for f in files:
        try:
            number = int(f.split('/')[-1].split('-')[0])
        except ValueError:
            continue

        if number > index:
            index = number

    print(f'Biggest index = {index}, new index = {index+1}')
    if placeholder:
        with open(f'{path}/{index+1}-placeholder-{name}', 'w') as fp:
            fp.write(f'size:{config.size}\nbs:{config.bs}\nopt: {params_opt}\nsched:{params_sched}\nconfig:{config}\nlearner:{learner}\n Zoom: {ZOOM_FACTORS}')


    return index+1

# Cell

def to_byte_tensor(item):
    res = torch.ByteTensor(torch.ByteStorage.from_buffer(item.tobytes()))
    w,h = item.size
    return res.view(h,w,-1).permute(2,0,1)

def to_float_tensor(item): return item.float().div_(255.)


def normalize_tan(x):
    return (x - 0.5) / 0.5

def decode_from_tan(x):
    return (x * 0.5) + 0.5

# Cell

def loader(path, tfms, show_img=False):
    style_im_raw = PIL.Image.open(path).convert('RGB')
    if show_img:
        plt.imshow(style_im_raw)

    im = tfms(style_im_raw)

    show_img_from_tensor(im)
    return im.unsqueeze(0).cuda()

def show_img_from_tensor(x, ax=None, decoder=None, figsize=(8,8), title=''):
    if decoder is not None:
        x = decoder(x)
    img = x.detach().cpu().numpy().transpose((1,2,0))



    if ax:
        ax.imshow(img)
    else:
        fig, ax = plt.subplots(figsize=figsize)
        ax.imshow(img)


        if len(title) > 0:
            fig.suptitle(title, y=0.9, fontsize=15)

# Cell

def gradient_flow(m):
    mean_grad = []
    std_grad = []
    median_grad = []
    norm_grad = []
    names = []
    for i, (n, p) in enumerate(m.named_parameters()):
        if p.grad is not None and p.grad.ndimension() > 1 :
            #print(n, p.grad.shape, p.grad.ndimension())
            mean_grad.append(p.grad.mean())
            std_grad.append(p.grad.std())
            median_grad.append(p.grad.median())
            norm_grad.append(p.grad.norm())
            names.append(n.replace('layers', 'l'))

    return names, mean_grad, std_grad, median_grad, norm_grad

def viz_grad_flow(names, mean_grad, std_grad, median_grad, norm_grad, target= 'Not specified'):
    fig, axes = plt.subplots(nrows=3, ncols=1,figsize=(15, 12))

    axes = axes.flatten()

    axes[0].plot(names, mean_grad, c='r')
    axes[0].plot(names, median_grad, c='b')
    axes[1].plot(names, std_grad)
    axes[2].plot(names, norm_grad)


    axes[0].set_title(f'Mean(R)/Med(B) {target}')
    axes[1].set_title(f'Std {target}')
    axes[2].set_title(f'Norm {target}')


    return fig

# Cell

def get_tb_logdir(name):
    current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    return 'logs/' + current_time + f'/{name}'

def get_identity_training(name):
    return f'{name}-{datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}'

def get_tb_writer(name):

    train_summary_writer = SummaryWriter(get_tb_logdir(name))

    return train_summary_writer