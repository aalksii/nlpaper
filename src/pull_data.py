from datasets import load_dataset
from configs.huggingface_config import (
    dataset_path, dataset_path_hf, select_ratio
)


def filter_none(example):
    return example['abstract'] is not None and len(example['abstract'])


def prepare_dataset():
    # Download dataset
    dataset = load_dataset(dataset_path_hf)
    train = dataset['train']
    test = dataset['test']

    # Select a part of the dataset
    train = train.select(range(int(select_ratio * len(train))))
    test = test.select(range(int(select_ratio * len(test))))

    # Filter None values and empty strings
    train = train.filter(filter_none)
    test = test.filter(filter_none)

    # Save datasets
    train.save_to_disk(dataset_path / 'train')
    test.save_to_disk(dataset_path / 'test')


if __name__ == '__main__':
    prepare_dataset()
