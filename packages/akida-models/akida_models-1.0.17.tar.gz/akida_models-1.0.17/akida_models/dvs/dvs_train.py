#!/usr/bin/env python
# ******************************************************************************
# Copyright 2020 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
"""
Training script for DVS models.
"""

import os
import argparse
import numpy as np

from keras.utils.data_utils import get_file
from keras.utils.np_utils import to_categorical

from cnn2snn import load_quantized_model, convert

from ..cyclic_lr import CyclicLR
from ..training import get_training_parser, compile_model, evaluate_model

from .dvs_generator import DVS_DataGenerator


def get_data(dataset):
    """ Loads data.

    Dataset parameters for DVSDataGenerator are set from DVS pickles.

    Args:
        dataset (str): name of the dataset to load, either 'dvs_gesture' or
            'samsung_handy'.

    Returns:
        tuple: train data, test data, test labels, classes selected for training
            and number of times that every sample have to be repeated for
            training.
    """
    # Load pre-processed dataset
    train_file = get_file(fname=dataset + '_preprocessed_train.npy',
                          origin=os.path.join(
                              'http://data.brainchip.com/dataset-mirror',
                              dataset, dataset + '_preprocessed_train.npy'),
                          cache_subdir=os.path.join('datasets', dataset))

    test_file = get_file(fname=dataset + '_preprocessed_test.npy',
                         origin=os.path.join(
                             'http://data.brainchip.com/dataset-mirror',
                             dataset, dataset + '_preprocessed_test.npy'),
                         cache_subdir=os.path.join('datasets', dataset))

    train_set = list(np.load(train_file, allow_pickle=True))
    test_set = list(np.load(test_file, allow_pickle=True))

    # prepare data with DVS_DataGenerator
    if dataset == 'dvs_gesture':
        events_inversion = False
        allow_duplicate_events = False
        packets_fixed_by = 'dur'
        packets_per_sample = 3
        # packet_length is in milliseconds
        packet_length = 60
        downscale = 2
        camera_dims = (128, 128, 2)
        # class_list is used to define class that have to be learnt
        class_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        # sample_repeats define number of time that sample should be repeated
        sample_repeats = 5
    elif dataset == 'samsung_handy':
        events_inversion = False
        allow_duplicate_events = False
        packets_fixed_by = 'dur'
        packets_per_sample = 1
        packet_length = 20
        downscale = 4
        camera_dims = (480, 640, 2)
        class_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        sample_repeats = 30
    else:
        print('ERROR: Dataset "{}" not recognised'.format(dataset))

    # Generate DVS data from preprocessed NPY files with params defined above
    train_data = DVS_DataGenerator(
        inversion=events_inversion,
        dataset=train_set,
        subpacket_length=packet_length,
        subpackets_per_packet=packets_per_sample,
        camera_dims=camera_dims,
        packets_fixed_by=packets_fixed_by,
        include_polarity=True,
        allow_duplicate_events=allow_duplicate_events,
        downscale=downscale)

    test_data = DVS_DataGenerator(inversion=events_inversion,
                                  dataset=test_set,
                                  subpacket_length=packet_length,
                                  subpackets_per_packet=packets_per_sample,
                                  camera_dims=camera_dims,
                                  packets_fixed_by=packets_fixed_by,
                                  include_polarity=True,
                                  allow_duplicate_events=allow_duplicate_events,
                                  downscale=downscale)

    x_test_ev, y_test = test_data.get_random_samples(
        class_list=class_list, samples_per_trial=sample_repeats)
    x_test = test_data.samples_evs2images(x_test_ev)
    y_test = to_categorical(y_test)

    return train_data, x_test, y_test, class_list, sample_repeats


def train_model(model, train_set, test_set, class_list, sample_repeats,
                batch_size, max_learning_rate, epochs):
    """ Trains the model.

    Args:
        model (keras.Model): the model to train
        train_set (DVS_DataGenerator): train data generator
        test_set (tuple): test data and test labels as np.arrays
        class_list (list): classes selected for training
        sample_repeats (int): number of times that every sample have to be
         repeated for training
        batch_size (int): the batch size
        max_learning_rate (float): learning rate maximum value
        epochs (int): the number of epochs
    """
    min_lr = max_learning_rate * 0.01

    callbacks = []
    n_iterations = np.round(
        len(train_set.dataset) * sample_repeats / batch_size)

    lr_scheduler = CyclicLR(base_lr=min_lr,
                            max_lr=max_learning_rate,
                            step_size=4 * n_iterations,
                            mode='triangular2')
    callbacks.append(lr_scheduler)

    for j in range(epochs):
        print('Epoch: ' + str(j))
        x_train_ev, y_train = train_set.get_random_samples(
            class_list=class_list, samples_per_trial=sample_repeats)
        y_train = to_categorical(y_train)

        augmentation_repeats = 4
        for _ in range(augmentation_repeats):
            x_train_ev_aug = train_set.augment_data(x_train_ev,
                                                    polarity_flip=True,
                                                    rotation_range=30,
                                                    width_shift_range=1.5,
                                                    height_shift_range=1.5)

            x_train = train_set.samples_evs2images(x_train_ev_aug)
            model.fit(x_train,
                      y_train,
                      epochs=1,
                      batch_size=batch_size,
                      callbacks=callbacks,
                      validation_data=test_set)

        del x_train_ev, x_train, y_train


def main():
    """ Entry point for script and CLI usage.
    """
    global_parser = argparse.ArgumentParser(add_help=False)
    global_parser.add_argument("-d",
                               "--dataset",
                               type=str,
                               default='dvs_gesture',
                               choices=['dvs_gesture', 'samsung_handy'],
                               help="Dataset name (defaut=dvs_gesture)")

    parsers = get_training_parser(batch_size=32,
                                  tune=True,
                                  global_batch_size=False,
                                  global_parser=global_parser)

    tune_parser = parsers[2]
    tune_parser.add_argument("-ft",
                             "--fine_tune",
                             type=bool,
                             default=False,
                             help="Fine tune the model (lower learning rate)")

    args = parsers[0].parse_args()

    # Load the source model
    model = load_quantized_model(args.model)

    # Compile model
    learning_rate = 0.001
    if args.action == 'tune':
        learning_rate = 0.00001 if args.fine_tune else 0.0001

    compile_model(model, learning_rate=learning_rate)

    # Load data
    train_data, x_test, y_test, class_list, sample_repeats = get_data(
        args.dataset)

    # Train model
    if args.action in ["train", "tune"]:
        train_model(model=model,
                    train_set=train_data,
                    test_set=(x_test, y_test),
                    class_list=class_list,
                    sample_repeats=sample_repeats,
                    batch_size=args.batch_size,
                    max_learning_rate=learning_rate,
                    epochs=args.epochs)

        # Save model in Keras format (h5)
        if args.savemodel:
            model.save(args.savemodel, include_optimizer=False)
            print(f"Trained model saved as {args.savemodel}")

    elif args.action == "eval":
        # Evaluate model accuracy
        if args.akida:
            model_ak = convert(model, input_is_image=False)
            preds = model_ak.predict(np.swapaxes(x_test, 1, 2).astype('uint8'))
            accuracy = (np.argmax(y_test, 1) == preds).mean()
            print(f"Akida accuracy: {accuracy}")
        else:
            evaluate_model(model, x_test, y=y_test)


if __name__ == "__main__":
    main()
