#!/bin/bash

# this scripts create symbolic links from the data and models 
# and place the links in CenterNet in the right position

#link the coco dataset into CenterNet
DATASOURCE=coco
ln -s /scratch_net/biwidl213/silvasta/datasets/$DATASOURCE /scratch_net/biwidl213/silvasta/detectors/CenterNet/data/

#link the models into CenterNet
MODELSOURCE=CenterNet_models/*
ln -s /scratch_net/biwidl213/silvasta/datasets/$MODELSOURCE /scratch_net/biwidl213/silvasta/detectors/CenterNet/models/
