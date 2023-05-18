from pathlib import Path

dataset_path = Path('data/ml-arxiv-papers/')
dataset_path_hf = 'aalksii/ml-arxiv-papers'
select_ratio = 0.001
cache_dir = Path('cache/huggingface/')
model_checkpoint_hf = 'aalksii/distilbert-base-uncased-ml-arxiv-papers'
chunk_size = 16
wwm_probability = 0.15
batch_size = 16
trained_model_name = 'distilbert-base-uncased-ml-arxiv-papers-trained'
trained_model_path = Path('models/') / trained_model_name
push_to_hub = False
fp16 = False  # Use it for GPU
wwm_collator = True
