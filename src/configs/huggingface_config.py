from pathlib import Path

# Datasets
dataset_path = Path('../data/ml-arxiv-papers/')
dataset_path_hf = 'aalksii/ml-arxiv-papers'
select_ratio = 0.1
test_size = 1 / 9

# Cache
cache_dir = Path('../cache/huggingface/')

# Models
model_checkpoint_hf = 'aalksii/distilbert-base-uncased-ml-arxiv-papers'
trained_model_name = 'distilbert-base-uncased-ml-arxiv-papers-trained'
trained_model_path = Path('../models/') / trained_model_name
chunk_size = 16
batch_size = 16
wwm_probability = 0.15
push_to_hub = False
fp16 = False  # Use it for GPU
wwm_collator = True
