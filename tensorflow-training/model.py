"""Model to classify fashion MNIST

This file contains all the model information: the training steps, the batch
size and the model itself.
"""

import tensorflow as tf

def get_batch_size():
    """Returns the batch size.
    """
    return None

def get_epochs():
    """Returns number of epochs.
    """
    return 10

def nnet(img_shape):
    """Returns a compiled model.

    A

    Parameters:
        input_layer: A tf.keras.layers.Conv2D().
            shape: (width, height, 1)
    Returns:
        model: A compiled model
    """


    # TODO: Code of your solution
    model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(input_shape=img_shape, filters=8, kernel_size=3, 
                      strides=2, activation='relu', name='Conv1'),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(10, name='Dense')
            ])
    model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=[tf.keras.metrics.SparseCategoricalAccuracy()])


    return model