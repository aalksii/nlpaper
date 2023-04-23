import re

import fitz
import pytextrank
import spacy
from pdfminer.high_level import extract_text
from txtmarker.factory import Factory

# from PyPDF2 import PdfReader

print(pytextrank.__version__)


def extract(path):
    text = extract_text(path)

    # Clean data
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"[^\x20-\x7F]+", "", text)
    return text


def pdf_to_text(file_path):
    doc = fitz.open(file_path)  # open document
    full_text = []
    for page in doc:  # iterate the document pages
        text = page.get_text().encode("utf8")  # get plain text (is in UTF-8)
        full_text.append(str(text).replace('\n', ' '))

    return full_text


def get_ranked(text, limit_sentences):
    # load a spaCy model, depending on language, scale, etc
    try:
        nlp = spacy.load("en_core_web_sm")
    except:  # If not present, we download
        spacy.cli.download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")

    # add PyTextRank to the spaCy pipeline
    nlp.add_pipe("textrank")
    doc = nlp(text)

    # examine the top-ranked phrases in the document
    # for phrase in doc._.phrases:
    #     print(phrase.text)
    #     print(phrase.rank, phrase.count)
    #     print(phrase.chunks)

    # for p in doc._.phrases:
    #     ic(p.rank, p.count, p.text)
    #     ic(p.chunks)

    sent_bounds = [[s.start, s.end, set([])] for s in doc.sents]

    limit_phrases = 4

    phrase_id = 0
    unit_vector = []

    for p in doc._.phrases:
        # ic(phrase_id, p.text, p.rank)

        unit_vector.append(p.rank)

        for chunk in p.chunks:
            # ic(chunk.start, chunk.end)

            for sent_start, sent_end, sent_vector in sent_bounds:
                if chunk.start >= sent_start and chunk.end <= sent_end:
                    # ic(sent_start, chunk.start, chunk.end, sent_end)
                    sent_vector.add(phrase_id)
                    break

        phrase_id += 1

        if phrase_id == limit_phrases:
            break

    sum_ranks = sum(unit_vector)

    unit_vector = [rank / sum_ranks for rank in unit_vector]

    from math import sqrt

    sent_rank = {}
    sent_id = 0

    for sent_start, sent_end, sent_vector in sent_bounds:
        # ic(sent_vector)
        sum_sq = 0.0
        for phrase_id in range(len(unit_vector)):
            # ic(phrase_id, unit_vector[phrase_id])

            if phrase_id not in sent_vector:
                sum_sq += unit_vector[phrase_id] ** 2.0

        sent_rank[sent_id] = sqrt(sum_sq)
        sent_id += 1

    from operator import itemgetter

    sorted(sent_rank.items(), key=itemgetter(1))

    sent_text = {}
    sent_id = 0

    for sent in doc.sents:
        sent_text[sent_id] = sent.text
        sent_id += 1

    num_sent = 0

    sentences = []
    ids = []

    for sent_id, rank in sorted(sent_rank.items(), key=itemgetter(1)):
        # ic(sent_id, sent_text[sent_id])

        sentences.append(sent_text[sent_id])
        ids.append(sent_id)

        num_sent += 1

        if num_sent == limit_sentences:
            break

    return sentences, ids


def highlight_ranked(input_file_path, output_file_path, limit_sentences):
    text = extract(input_file_path)

    sentences, ids = get_ranked(text,
                                limit_sentences=limit_sentences)

    # doc = fitz.open(input_file_path)
    #
    # for sentence in sentences:
    #     for word in sentence.split(' '):
    #         for page in doc:
    #             text_instances = page.search_for(word)
    #             if text_instances:
    #                 for inst in text_instances:
    #                     highlight = page.add_highlight_annot(inst)
    #                     highlight.update()
    #
    # doc.save(output_file_path, garbage=4, deflate=True, clean=True)

    highlights = []
    for i, sentence in enumerate(sentences):
        highlights.append((
            get_importance(i, limit_sentences),
            '(.|\n)*'.join([
                ' '.join([sentence.split(' ')[0],
                          sentence.split(' ')[1]]),
                sentence.split(' ')[-1]
                # ' '.join([sentence.split(' ')[-2],
                #           sentence.split(' ')[-1]])
            ]),
        ))

    print(highlights)

    highlighter = Factory.create("pdf")
    highlighter.highlight(input_file_path, output_file_path, highlights)

    return sentences


def get_importance(rank, n):
    return '!' * (n - rank)
