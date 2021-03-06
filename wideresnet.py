# model mainly taken from here https://github.com/titu1994/Wide-Residual-Networks/blob/master/wide_residual_network.py
from keras.models import Model
from keras.layers import Input, Add, Activation, Dropout, Flatten, Dense
from keras.layers import Conv2D, MaxPooling2D, AveragePooling2D, ZeroPadding2D
from keras.layers import BatchNormalization
from keras import backend as K
from keras.regularizers import l2

def expand_conv(init, base, k, stride):
    channel_axis = 1 if K.image_data_format() == "channels_first" else -1
    shortcut  = BatchNormalization(axis=channel_axis, momentum=0.1, epsilon=1e-5, gamma_initializer='uniform')(init)
    shortcut  = Activation('relu')(shortcut)
    x = ZeroPadding2D((1, 1))(shortcut)
    x = Conv2D(base * k, (3, 3), strides=stride, padding='valid', kernel_initializer='he_normal', use_bias=False)(x)
    x = BatchNormalization(axis=channel_axis, momentum=0.1, epsilon=1e-5, gamma_initializer='uniform')(x)
    x = Activation('relu')(x)
    x = ZeroPadding2D((1, 1))(x)
    x = Conv2D(base * k, (3, 3), strides=(1, 1), padding='valid', kernel_initializer='he_normal', use_bias=False)(x)
    # Add shortcut
    shortcut = Conv2D(base * k, (1, 1), strides=stride, padding='same', kernel_initializer='he_normal', use_bias=False)(shortcut)
    m = Add()([x, shortcut])
    return m

def conv_block(input, n, stride, k=1, dropout=0.0):
    init = input
    channel_axis = 1 if K.image_data_format() == "channels_first" else -1
    x = BatchNormalization(axis=channel_axis, momentum=0.1, epsilon=1e-5, gamma_initializer='uniform')(input)
    x = Activation('relu')(x)
    x = Conv2D(n * k, (3, 3), strides=(1, 1), padding='same', kernel_initializer='he_normal', use_bias=False)(x)
    if dropout > 0.0: x = Dropout(dropout)(x)
    x = BatchNormalization(axis=channel_axis, momentum=0.1, epsilon=1e-5, gamma_initializer='uniform')(x)
    x = Activation('relu')(x)
    x = Conv2D(n * k, (3, 3), strides=(1, 1), padding='same', kernel_initializer='he_normal', use_bias=False)(x)
    m = Add()([init, x])
    return m

def create_wide_residual_network(input_dim, nb_classes=10, N=28, k=10, dropout=0.3, verbose=1):
    """
    Creates a Wide Residual Network with specified parameters
    :param input: Input Keras object
    :param nb_classes: Number of output classes
    :param N: Depth of the network. Compute N = (n - 4) / 6.
              Example : For a depth of 16, n = 16, N = (16 - 4) / 6 = 2
              Example2: For a depth of 28, n = 28, N = (28 - 4) / 6 = 4
              Example3: For a depth of 40, n = 40, N = (40 - 4) / 6 = 6
    :param k: Width of the network.
    :param dropout: Adds dropout if value is greater than 0.0
    :param verbose: Debug info to describe created WRN
    :return:
    """
    ip = Input(shape=input_dim)
    x = ZeroPadding2D((1, 1))(ip)
    channel_axis = 1 if K.image_data_format() == "channels_first" else -1
    x = Conv2D(16, (3, 3), padding='same', kernel_initializer='he_normal', use_bias=False)(x)
    nb_conv = 4
    x = expand_conv(x, 16, k, stride=(1,1))
    for i in range(N - 1):
        x = conv_block(x, n=16, stride=(1,1), k=k, dropout=dropout)
        nb_conv += 2
    x = expand_conv(x, 32, k, stride=(2,2))
    for i in range(N - 1):
        x = conv_block(x, n=32, stride=(2,2), k=k, dropout=dropout)
        nb_conv += 2
    x = expand_conv(x, 64, k, stride=(2,2))
    for i in range(N - 1):
        x = conv_block(x, n=64, stride=(2,2), k=k, dropout=dropout)
        nb_conv += 2
    x = AveragePooling2D((8, 8))(x)
    x = Flatten()(x)
    x = Dense(nb_classes, activation='softmax')(x)
    model = Model(ip, x)
    return model

if __name__ == "__main__":
    from keras.utils import plot_model
    from keras.layers import Input
    from keras.models import Model

    init = (32, 32, 3)


