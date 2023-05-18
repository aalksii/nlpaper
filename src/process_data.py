import re

from datasets import load_dataset
from transformers import (
    AutoTokenizer
)

from configs.huggingface_config import (
    dataset_path, model_checkpoint_hf
)
from configs.common_config import RANDOM_STATE

latex_pattern = r'(\$+)(?:(?!\1)[\s\S])*\1|' \
                r'\\[a-zA-Z]+(?:\{[^\}]+\})?|' \
                r'http[s]?://\S+'


def clean_text(example):
    example['abstract'] = re.sub(latex_pattern, '', example['abstract'])
    example['abstract'] = example['abstract'].replace('\n', ' ').strip()
    return example


def process_dataset():
    # Load cached dataset
    dataset = load_dataset(dataset_path / 'train')

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint_hf)

    # Clean text
    dataset = dataset.map(clean_text)

    # Tokenize
    def tokenize_function(examples):
        result = tokenizer(examples["abstract"])
        if tokenizer.is_fast:
            result["word_ids"] = [result.word_ids(i) for i in
                                  range(len(result["input_ids"]))]
        return result

    # Use batched=True to activate fast multithreading!
    tokenized_dataset = dataset.map(
        tokenize_function, batched=True, remove_columns=['title', 'abstract']
    )


if __name__ == '__main__':
    process_dataset()
