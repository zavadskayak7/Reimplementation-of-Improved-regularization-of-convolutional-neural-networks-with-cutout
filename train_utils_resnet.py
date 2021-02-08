import numpy as np

def lr_schedule_rn(epoch):
    # learning rate schedule
    lr = 1e-3 # initial lr
    if epoch > 180:
        lr *= 0.5e-3
    elif epoch > 160:
        lr *= 1e-3
    elif epoch > 120:
        lr *= 1e-2
    elif epoch > 60:
        lr *= 1e-1
    print('Learning rate: ', lr)
    return lr

def hms_string(sec_elapsed):
    # formatted time string for the training
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60
    return f"{h}:{m:>02}:{s:>05.2f}"

def get_random_cutout(p=1.0, size=16):
    def cutout(input_img):
        img_h, img_w, img_c = input_img.shape # 32 32 3

        # probability of applying 
        p_1 = np.random.rand()
        if p_1 > p:
            return input_img

        # pick random center
        y = np.random.randint(img_h)
        x = np.random.randint(img_w)
        # compute borders of the cutout
        y1 = np.clip(max(0, y - size // 2), 0, img_h)
        y2 = np.clip(max(0, y + size // 2), 0, img_h)
        x1 = np.clip(max(0, x - size // 2), 0, img_w)
        x2 = np.clip(max(0, x + size // 2), 0, img_w)

        # filling value for the cutout 
        c = np.random.uniform(1,1)
        input_img[y1: y2, x1: x2,:] = c
        return input_img
    return cutout