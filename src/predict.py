from summarizer import Summarizer
from transformers import pipeline


def fill_mask(x):
    unmasker = pipeline('fill-mask',
                        model='distilbert-base-uncased')
    output = unmasker(x)[0]['sequence']
    return output


def summarize(x):
    summarizer = Summarizer(model='distilbert-base-uncased')
    output = summarizer(x, ratio=0.2, return_as_list=False)
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
