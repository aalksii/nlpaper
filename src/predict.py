from summarizer import Summarizer
from transformers import pipeline

from configs.huggingface_config import best_model_name
from configs.summarizer_config import return_as_list, ratio
from model_utils import load_tokenizer_and_model


def fill_mask(x):
    unmasker = pipeline('fill-mask',
                        model=best_model_name)
    output = unmasker(x)[0]['sequence']
    return output


def summarize(x):
    tokenizer, model = load_tokenizer_and_model(best_model_name)

    summarizer = Summarizer(custom_tokenizer=tokenizer, custom_model=model)
    output = summarizer(x, ratio=ratio, return_as_list=return_as_list)
    return output


if __name__ == '__main__':
    print(fill_mask('New study links disturbed [MASK] metabolism in depressed '
                    'individuals to disruption of the gut microbiome.'))
    print(summarize('Depression is a widespread mental health condition '
                    'that significantly affects population health. Major '
                    'depression is known to cause a range of debilitating '
                    'symptoms beyond emotional distress, including cognitive '
                    'impairments, motor function problems, inflammation, '
                    'disturbances in the immune system, and increased risk '
                    'of cardiometabolic disorders and mortality.'))
