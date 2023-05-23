import collections

import numpy as np
from datasets import load_from_disk
from transformers import (
    DataCollatorForLanguageModeling,
    default_data_collator,
    TrainingArguments,
    Trainer
)

from configs.huggingface_config import (
    batch_size,
    dataset_path,
    push_to_hub as push_to_hub_config,
    fp16,
    wwm_probability,
    wwm_collator,
    num_train_epochs,
    logging_strategy,
    learning_rate,
    weight_decay,
)
from model_utils import load_tokenizer_and_model


def load_trainer(input_model_name,
                 output_model_path=None,
                 push_to_hub=push_to_hub_config):
    tokenizer, model = load_tokenizer_and_model(input_model_name)

    # Load prepared dataset
    processed_dataset = load_from_disk(
        dataset_path / 'processed_train_dataset'
    )

    # Show the training loss with every epoch
    logging_steps = len(processed_dataset['train']) // batch_size

    remove_unused_columns = False if wwm_collator else True

    training_args = TrainingArguments(
        output_dir=output_model_path,
        overwrite_output_dir=True,
        evaluation_strategy='epoch',
        learning_rate=learning_rate,
        weight_decay=weight_decay,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        push_to_hub=push_to_hub,
        fp16=fp16,
        logging_steps=logging_steps,
        logging_strategy=logging_strategy,
        remove_unused_columns=remove_unused_columns,
        num_train_epochs=num_train_epochs
    )

    if wwm_collator:
        def whole_word_masking_data_collator(features):
            for feature in features:
                word_ids = feature.pop('word_ids')

                # Create a map between words and corresponding token indices
                mapping = collections.defaultdict(list)
                current_word_index = -1
                current_word = None
                for idx, word_id in enumerate(word_ids):
                    if word_id is not None:
                        if word_id != current_word:
                            current_word = word_id
                            current_word_index += 1
                        mapping[current_word_index].append(idx)

                # Randomly mask words
                mask = np.random.binomial(1, wwm_probability, (len(mapping),))
                input_ids = feature['input_ids']
                labels = feature['labels']
                new_labels = [-100] * len(labels)
                for word_id in np.where(mask)[0]:
                    word_id = word_id.item()
                    for idx in mapping[word_id]:
                        new_labels[idx] = labels[idx]
                        input_ids[idx] = tokenizer.mask_token_id
                feature['labels'] = new_labels

            return default_data_collator(features)

        data_collator = whole_word_masking_data_collator
    else:
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=tokenizer,
            mlm_probability=wwm_probability)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=processed_dataset['train'],
        eval_dataset=processed_dataset['val'],
        data_collator=data_collator,
        tokenizer=tokenizer,
    )
    return trainer
