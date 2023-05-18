import collections
import math

import numpy as np
from datasets import load_from_disk
from transformers import (
    AutoModelForMaskedLM,
    DataCollatorForLanguageModeling,
    default_data_collator,
    TrainingArguments,
    Trainer,
    AutoTokenizer
)

from configs.huggingface_config import (
    model_checkpoint_hf,
    batch_size,
    trained_model_path,
    dataset_path,
    push_to_hub,
    fp16,
    wwm_probability,
    wwm_collator,
)


def train():
    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint_hf)
    model = AutoModelForMaskedLM.from_pretrained(model_checkpoint_hf)

    # Load prepared dataset
    processed_dataset = load_from_disk(
        dataset_path / 'processed_train_dataset'
    )

    # Show the training loss with every epoch
    logging_steps = len(processed_dataset['train']) // batch_size

    training_args = TrainingArguments(
        output_dir=trained_model_path,
        overwrite_output_dir=True,
        evaluation_strategy='epoch',
        learning_rate=2e-5,
        weight_decay=0.01,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        push_to_hub=push_to_hub,
        fp16=fp16,
        logging_steps=logging_steps,
        remove_unused_columns=False
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

    eval_results = trainer.evaluate()
    print(f'>>> Perplexity: {math.exp(eval_results["eval_loss"]):.2f}')

    trainer.train()

    eval_results = trainer.evaluate()
    print(f'>>> Perplexity: {math.exp(eval_results["eval_loss"]):.2f}')

    trainer.save_model(trained_model_path)


if __name__ == '__main__':
    train()
