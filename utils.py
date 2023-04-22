import spacy
import pytextrank

print(pytextrank.__version__)
from PyPDF2 import PdfReader


def pdf_to_text(file_path):
    reader = PdfReader(file_path)
    full_text = ''

    for page in reader.pages:
        text = page.extract_text()
        full_text += text

    full_text = full_text.replace('\n', ' ')

    return full_text


def get_ranked_sentences(text, limit_sentences=3):
    # load a spaCy model, depending on language, scale, etc
    nlp = spacy.load("en_core_web_sm")

    # add PyTextRank to the spaCy pipeline
    nlp.add_pipe("textrank")
    doc = nlp(text)

    # examine the top-ranked phrases in the document
    # for phrase in doc._.phrases:
    #     print(phrase.text)
    #     print(phrase.rank, phrase.count)
    #     print(phrase.chunks)

    from icecream import ic

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

    for sent_id, rank in sorted(sent_rank.items(), key=itemgetter(1)):
        # ic(sent_id, sent_text[sent_id])

        sentences.append(sent_text[sent_id])

        num_sent += 1

        if num_sent == limit_sentences:
            break

    return sentences
