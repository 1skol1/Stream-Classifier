"""Train and evaluate the model

This file trains the model upon the training data and evaluates it with
the eval data.
"""

import argparse


from pathlib import Path
from datetime import datetime

import tensorflow as tf
from tensorflow import keras
import model

def create_data_with_labels(data_dir,batch_size,img_height,img_width,img_channels):

    dataset = tf.keras.utils.image_dataset_from_directory(
                data_dir,
                seed=123,
                image_mode = img_channels,
                image_size = (img_width,img_height),
                label_mode= 'int',
                batch_size=batch_size)
                
    return dataset


def preprocess(dataset):
    normalization_layer = keras.layers.Rescaling(1./255)
    normalized_ds = dataset.map(lambda x, y: (normalization_layer(x), y))
    normalized = next(iter(normalized_ds))
    return (normalized)

def preprocess_mnist(train_data,test_data):
    # scale the values to 0.0 to 1.0
    train_data = train_data / 255.0
    test_data = test_data / 255.0

    # reshape for feeding into the model
    train_data = train_data.reshape(train_data.shape[0], 28, 28, 1)
    test_data = test_data.reshape(test_data.shape[0], 28, 28, 1)

    return (train_data,test_data)


def export_model(model,export_dir, model_dir='exported_model/1'):
    model_path = Path(export_dir) / model_dir
    if model_path.exists():
        timestamp = datetime.now().strftime("-%d-%m-%Y-%H-%M-%S")
        model_path = Path(str(model_path) + timestamp)

    tf.saved_model.save(model, str(model_path))

def train_model(data_flag,model_export_dir,data_dir_train=None,data_dir_test=None,batch_size=None,img_height=None,img_width=None,img_channels=None):
    """The function gets the training data & evaluation data and trains the model
       from the model.py file with it.

    Parameters:
        params: parameters for training the model
    """
    if data_flag == '0':
        fashion_mnist = keras.datasets.fashion_mnist
        (train_data, train_labels), (test_data, test_labels) = fashion_mnist.load_data()
        train_data,test_data = preprocess_mnist(train_data,test_data)
        img_shape = (28, 28, 1)
        ml_model = model.nnet(img_shape)
        if ml_model is None:
            print("No model found. You need to implement one in model.py")
        else:
            ml_model.fit(train_data, train_labels,
                        batch_size=batch_size,
                        epochs=model.get_epochs())
            ml_model.evaluate(test_data, test_labels, verbose=1)
            export_model(ml_model, export_dir=model_export_dir)
    else:
        train_ds= create_data_with_labels(data_dir_train,batch_size,img_height,img_width,img_channels)
        test_ds = create_data_with_labels(data_dir_test,batch_size,img_height,img_width,img_channels)
        train_ds = preprocess(train_ds)
        test_ds = preprocess(test_ds)
        ml_model = model.nnet()
        if ml_model is None:
            print("No model found. You need to implement one in model.py")
        else:
            ml_model.fit(train_ds,
                        epochs=model.get_epochs())
            ml_model.evaluate(test_ds, verbose=1)
            export_model(ml_model, export_dir=model_export_dir)
    
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-df','--data_flag', help='0 for fashion_mnist, 1 for other multiclass dataset', required=True)
    parser.add_argument('-med','--model_export_dir', help='path of parent directory where you want to store the exported model', required=True)
    parser.add_argument('-train','--data_dir_train', help='path to training dataset directory')
    parser.add_argument('-test','--data_dir_test', help='path to test/eval dataset directory')
    parser.add_argument('-bs','--batch_size', help='batch size to be used while training')
    parser.add_argument('-ih','--img_height', help='height of images in the dataset')
    parser.add_argument('-iw','--img_width', help='width of images in the dataset')
    parser.add_argument('-ic','--img_channel', help='no of color channels for the image,for RGB its 3, for grayscale its 1 ')
    args = parser.parse_args()
    

    train_model(args.data_flag,args.model_export_dir,args.data_dir_train,args.data_dir_test,args.batch_size,args.img_height,args.img_width,args.img_channel)