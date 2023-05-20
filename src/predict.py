from transformers import pipeline


def fill_mask_model(x):
    unmasker = pipeline('fill-mask',
                        model='distilbert-base-uncased')
    return unmasker(x)[0]['sequence']
