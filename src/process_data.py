import re

from datasets import DatasetDict, load_from_disk
from transformers import (
    AutoTokenizer
)

from configs.common_config import random_state
from configs.huggingface_config import (
    dataset_path,
    model_checkpoint_hf,
    chunk_size,
    test_size
)

latex_pattern = r'(\$+)(?:(?!\1)[\s\S])*\1|' \
                r'\\[a-zA-Z]+(?:\{[^\}]+\})?|' \
                r'http[s]?://\S+'


def clean_text(example):
    example['abstract'] = re.sub(latex_pattern, '', example['abstract'])
    example['abstract'] = example['abstract'].replace('\n', ' ').strip()
    return example


def group_texts(examples):
    # Concatenate all texts
    concatenated_examples = {k: sum(examples[k], []) for k in examples.keys()}
    # Compute length of concatenated texts
    total_length = len(concatenated_examples[list(examples.keys())[0]])
    # We drop the last chunk if it's smaller than chunk_size
    total_length = (total_length // chunk_size) * chunk_size
    # Split by chunks of max_len
    result = {
        k: [t[i: i + chunk_size] for i in range(0, total_length, chunk_size)]
        for k, t in concatenated_examples.items()
    }
    # Create a new labels column
    result['labels'] = result['input_ids'].copy()
    return result


def process_dataset():
    def tokenize_function(examples):
        result = tokenizer(examples['abstract'])
        if tokenizer.is_fast:
            result['word_ids'] = [result.word_ids(i) for i in
                                  range(len(result['input_ids']))]
        return result

    # Load cached dataset
    dataset = load_from_disk(dataset_path / 'train')

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint_hf)

    # Clean text
    dataset = dataset.map(clean_text)

    # Tokenize (use batched=True to activate fast multithreading!)
    tokenized_dataset = dataset.map(
        tokenize_function, batched=True, remove_columns=['title', 'abstract']
    )

    # Group dataset rows into chunks
    lm_datasets = tokenized_dataset.map(group_texts, batched=True)

    # Split dataset
    train_val_dataset = lm_datasets.train_test_split(test_size=test_size,
                                                     seed=random_state)

    processed_dataset = DatasetDict({
        'train': train_val_dataset['train'],
        'val': train_val_dataset['test'],
    })

    processed_dataset.save_to_disk(dataset_path / 'processed_train_dataset')


if __name__ == '__main__':
    print('>>> files:')
    import os
    print(os.getcwd())
    print(os.listdir('.'))
    process_dataset()
    print(os.getcwd())
