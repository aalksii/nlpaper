from pathlib import Path

# Datasets
dataset_path = Path('./data/') / 'ml-arxiv-papers/'
dataset_path_hf = 'aalksii/ml-arxiv-papers'
select_ratio = 0.001
test_size = 1 / 9

# Models
model_checkpoint_hf = 'aalksii/distilbert-base-uncased-ml-arxiv-papers'
trained_model_name = 'distilbert-base-uncased-ml-arxiv-papers-trained'
trained_model_path = Path('./models/') / trained_model_name
chunk_size = 16
batch_size = 16
wwm_probability = 0.15
push_to_hub = False
fp16 = False  # Use it for GPU
wwm_collator = True
num_train_epochs = 1
learning_rate = 2e-5
weight_decay = 0.01

# Logging
logging_strategy = 'epoch'

# Metrics log file
eval_metrics_path = './models/metrics.csv'

# Best model name loading
model_path = Path('./models/best_model_name.txt')
if model_path.exists():
    with model_path.open() as f:
        best_model_name = f.readline()
else:
    best_model_name = model_checkpoint_hf
