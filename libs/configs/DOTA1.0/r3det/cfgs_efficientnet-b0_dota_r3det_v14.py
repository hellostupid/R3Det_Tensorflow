# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import
import os
import tensorflow as tf
import math

"""
v12 + efficientnet-b0

This is your result for task 1:

    mAP: 0.6029497407279398
    ap of each class:
    plane:0.8431575297888173,
    baseball-diamond:0.627275049142723,
    bridge:0.4078551416023289,
    ground-track-field:0.5626007035529952,
    small-vehicle:0.6503533901303012,
    large-vehicle:0.6581003350035809,
    ship:0.6788574638941842,
    tennis-court:0.9079975643498643,
    basketball-court:0.6843903186775995,
    storage-tank:0.7456208170800375,
    soccer-ball-field:0.3385574205648121,
    roundabout:0.5804213139065293,
    harbor:0.4444497708547192,
    swimming-pool:0.5840748822421656,
    helicopter:0.33053441012844065

The submitted information is :

Description: RetinaNet_DOTA_R3Det_2x_20200507_70.2w
Username: SJTU-Det
Institute: SJTU
Emailadress: yangxue-2019-sjtu@sjtu.edu.cn
TeamMembers: yangxue

"""

# ------------------------------------------------
VERSION = 'RetinaNet_DOTA_R3Det_2x_20200507'
NET_NAME = 'efficientnet-b0'  # 'MobilenetV2'
ADD_BOX_IN_TENSORBOARD = True

# ---------------------------------------- System_config
ROOT_PATH = os.path.abspath('../')
print(20*"++--")
print(ROOT_PATH)
GPU_GROUP = "2,3"
NUM_GPU = len(GPU_GROUP.strip().split(','))
SHOW_TRAIN_INFO_INTE = 20
SMRY_ITER = 200
SAVE_WEIGHTS_INTE = 27000 * 2

SUMMARY_PATH = ROOT_PATH + '/output/summary'
TEST_SAVE_PATH = ROOT_PATH + '/tools/test_result'

if NET_NAME.startswith("resnet"):
    weights_name = NET_NAME
elif NET_NAME.startswith("MobilenetV2"):
    weights_name = "mobilenet/mobilenet_v2_1.0_224"
elif 'efficientnet' in NET_NAME:
    weights_name = "/efficientnet/{}/model".format(NET_NAME)
else:
    raise Exception('net name must in [resnet_v1_101, resnet_v1_50, MobilenetV2, efficient]')

PRETRAINED_CKPT = ROOT_PATH + '/data/pretrained_weights/' + weights_name + '.ckpt'
TRAINED_CKPT = os.path.join(ROOT_PATH, 'output/trained_weights')
EVALUATE_DIR = ROOT_PATH + '/output/evaluate_result_pickle/'

# ------------------------------------------ Train config
RESTORE_FROM_RPN = False
FIXED_BLOCKS = 1  # allow 0~3
FREEZE_BLOCKS = [True, False, False, False, False]  # for gluoncv backbone
USE_07_METRIC = True

MUTILPY_BIAS_GRADIENT = 2.0  # if None, will not multipy
GRADIENT_CLIPPING_BY_NORM = 10.0  # if None, will not clip

CLS_WEIGHT = 1.0
REG_WEIGHT = 1.0
USE_IOU_FACTOR = True

BATCH_SIZE = 1
EPSILON = 1e-5
MOMENTUM = 0.9
LR = 5e-4
DECAY_STEP = [SAVE_WEIGHTS_INTE*12, SAVE_WEIGHTS_INTE*16, SAVE_WEIGHTS_INTE*20]
MAX_ITERATION = SAVE_WEIGHTS_INTE*20
WARM_SETP = int(1.0 / 4.0 * SAVE_WEIGHTS_INTE)

# -------------------------------------------- Data_preprocess_config
DATASET_NAME = 'DOTA'  # 'pascal', 'coco'
PIXEL_MEAN = [123.68, 116.779, 103.939]  # R, G, B. In tf, channel is RGB. In openCV, channel is BGR
PIXEL_MEAN_ = [0.485, 0.456, 0.406]
PIXEL_STD = [0.229, 0.224, 0.225]  # R, G, B. In tf, channel is RGB. In openCV, channel is BGR
IMG_SHORT_SIDE_LEN = 800
IMG_MAX_LENGTH = 800
CLASS_NUM = 15

IMG_ROTATE = False
RGB2GRAY = False
VERTICAL_FLIP = False
HORIZONTAL_FLIP = True
IMAGE_PYRAMID = False

# --------------------------------------------- Network_config
SUBNETS_WEIGHTS_INITIALIZER = tf.random_normal_initializer(mean=0.0, stddev=0.01, seed=None)
SUBNETS_BIAS_INITIALIZER = tf.constant_initializer(value=0.0)
PROBABILITY = 0.01
FINAL_CONV_BIAS_INITIALIZER = tf.constant_initializer(value=-math.log((1.0 - PROBABILITY) / PROBABILITY))
WEIGHT_DECAY = 1e-4
USE_GN = False
NUM_SUBNET_CONV = 4
NUM_REFINE_STAGE = 2
USE_RELU = False
efficientdet_model_param_dict = {'efficientnet-b0': dict(fpn_num_filters=64, fpn_cell_repeats=3, box_class_repeats=3),
                                 'noisy_student_efficientnet-b1': dict(fpn_num_filters=88, fpn_cell_repeats=4, box_class_repeats=3),
                                 'efficientnet-b2': dict(fpn_num_filters=112, fpn_cell_repeats=5, box_class_repeats=3),
                                 'efficientnet-b3': dict(fpn_num_filters=160, fpn_cell_repeats=6, box_class_repeats=4),
                                 'efficientnet-b4': dict(fpn_num_filters=224, fpn_cell_repeats=7, box_class_repeats=4),
                                 'efficientnet-b5': dict(fpn_num_filters=288, fpn_cell_repeats=7, box_class_repeats=4),
                                 'efficientnet-b6': dict(fpn_num_filters=384, fpn_cell_repeats=8, box_class_repeats=5),
                                 'efficientnet-b7': dict(fpn_num_filters=384, fpn_cell_repeats=8, box_class_repeats=5),
                                 }

# ---------------------------------------------Anchor config
LEVEL = ['P3', 'P4', 'P5', 'P6', 'P7']
BASE_ANCHOR_SIZE_LIST = [32, 64, 128, 256, 512]
ANCHOR_STRIDE = [8, 16, 32, 64, 128]
ANCHOR_SCALES = [1.]
ANCHOR_RATIOS = [1.]
ANCHOR_ANGLES = [-90, -75, -60, -45, -30, -15]
ANCHOR_SCALE_FACTORS = None
USE_CENTER_OFFSET = True
METHOD = 'H'
USE_ANGLE_COND = False
ANGLE_RANGE = 90

# --------------------------------------------RPN config
SHARE_NET = True
USE_P5 = True
IOU_POSITIVE_THRESHOLD = 0.35
IOU_NEGATIVE_THRESHOLD = 0.25
REFINE_IOU_POSITIVE_THRESHOLD = [0.5, 0.6]
REFINE_IOU_NEGATIVE_THRESHOLD = [0.4, 0.5]

NMS = True
NMS_IOU_THRESHOLD = 0.1
MAXIMUM_DETECTIONS = 100
FILTERED_SCORE = 0.05
VIS_SCORE = 0.4

# --------------------------------------------MASK config
USE_SUPERVISED_MASK = False
MASK_TYPE = 'r'  # r or h
BINARY_MASK = False
SIGMOID_ON_DOT = False
MASK_ACT_FET = True  # weather use mask generate 256 channels to dot feat.
GENERATE_MASK_LIST = ["P3", "P4", "P5", "P6", "P7"]
ADDITION_LAYERS = [4, 4, 3, 2, 2]  # add 4 layer to generate P2_mask, 2 layer to generate P3_mask
ENLAEGE_RF_LIST = ["P3", "P4", "P5", "P6", "P7"]
SUPERVISED_MASK_LOSS_WEIGHT = 1.0
