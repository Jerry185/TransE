#!/usr/bin/env bash
CUDA_VISIBLE_DEVICES=0 \
python src/main.py \
--data_dir ./data/ownthink/ \
--embedding_dim 100 \
--margin_value 1 \
--batch_size 10000 \
--learning_rate 0.003 \
--n_generator 24 \
--n_rank_calculator 24 \
--eval_freq 10 \
--max_epoch 1 \
--save_epoch 1 \
--model_save_path model