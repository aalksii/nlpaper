from pathlib import Path

dataset_path = Path('../data/ml-arxiv-papers/')
dataset_path_hf = 'aalksii/ml-arxiv-papers'
select_ratio = 0.001
cache_dir = Path('../cache/huggingface/')
model_checkpoint_hf = 'aalksii/distilbert-base-uncased-ml-arxiv-papers'
