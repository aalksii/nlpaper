import re
import collections

import numpy as np
from datasets import load_dataset, DatasetDict, Dataset
from transformers import (
    AutoModelForMaskedLM,
    AutoTokenizer,
    DataCollatorForLanguageModeling,
    default_data_collator,
    TrainingArguments,
    Trainer,
    AutoConfig,
    AutoTokenizer,
    AutoModel,
    pipeline
)

from configs.huggingface_config import (
    dataset_path,
    model_checkpoint_hf,
    chunk_size,
    wwm_probability
)
from configs.common_config import RANDOM_STATE

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
        k: [t[i : i + chunk_size] for i in range(0, total_length, chunk_size)]
        for k, t in concatenated_examples.items()
    }
    # Create a new labels column
    result["labels"] = result["input_ids"].copy()
    return result






def process_dataset():
    def tokenize_function(examples):
        result = tokenizer(examples["abstract"])
        if tokenizer.is_fast:
            result["word_ids"] = [result.word_ids(i) for i in
                                  range(len(result["input_ids"]))]
        return result

    # def whole_word_masking_data_collator(features):
    #     for feature in features:
    #         word_ids = feature.pop("word_ids")
    #
    #         # Create a map between words and corresponding token indices
    #         mapping = collections.defaultdict(list)
    #         current_word_index = -1
    #         current_word = None
    #         for idx, word_id in enumerate(word_ids):
    #             if word_id is not None:
    #                 if word_id != current_word:
    #                     current_word = word_id
    #                     current_word_index += 1
    #                 mapping[current_word_index].append(idx)
    #
    #         # Randomly mask words
    #         mask = np.random.binomial(1, wwm_probability, (len(mapping),))
    #         input_ids = feature["input_ids"]
    #         labels = feature["labels"]
    #         new_labels = [-100] * len(labels)
    #         for word_id in np.where(mask)[0]:
    #             word_id = word_id.item()
    #             for idx in mapping[word_id]:
    #                 new_labels[idx] = labels[idx]
    #                 input_ids[idx] = tokenizer.mask_token_id
    #         feature["labels"] = new_labels
    #
    #     return default_data_collator(features)


    # Load cached dataset
    dataset = load_dataset(dataset_path / 'train')

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
    train_val_dataset = lm_datasets.train_test_split(test_size=1 / 9,
                                                     seed=RANDOM_STATE)

    processed_dataset = DatasetDict({
        'train': train_val_dataset['train'],
        'val': train_val_dataset['test'],
    })

    processed_dataset.save_to_disk(dataset_path / 'processed_dataset')


if __name__ == '__main__':
    process_dataset()
