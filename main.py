import spacy

from PyPDF2 import PdfReader

# creating a pdf reader object
reader = PdfReader('example.pdf')

# printing number of pages in pdf file
print(len(reader.pages))

# getting a specific page from the pdf file
page = reader.pages[0]

# extracting text from page
text = page.extract_text()
print(text)

# example text
# text = "Compatibility of systems of linear constraints over the set of " \
#        "natural numbers. Criteria of compatibility of a system of linear " \
#        "Diophantine equations, strict inequations, and nonstrict inequations " \
#        "are considered. Upper bounds for components of a minimal set of " \
#        "solutions and algorithms of construction of minimal generating sets " \
#        "of solutions for all types of systems are given. These criteria and " \
#        "the corresponding algorithms for constructing a minimal supporting " \
#        "set of solutions can be used in solving all the considered types " \
#        "systems and systems of mixed types. "

# load a spaCy model, depending on language, scale, etc
nlp = spacy.load("en_core_web_sm")

# add PyTextRank to the spaCy pipeline
nlp.add_pipe("textrank")
doc = nlp(text)

# examine the top-ranked phrases in the document
for phrase in doc._.phrases:
    print(phrase.text)
    print(phrase.rank, phrase.count)
    print(phrase.chunks)

from icecream import ic

for p in doc._.phrases:
    ic(p.rank, p.count, p.text)
    ic(p.chunks)

sent_bounds = [[s.start, s.end, set([])] for s in doc.sents]

limit_phrases = 4

phrase_id = 0
unit_vector = []

for p in doc._.phrases:
    ic(phrase_id, p.text, p.rank)

    unit_vector.append(p.rank)

    for chunk in p.chunks:
        ic(chunk.start, chunk.end)

        for sent_start, sent_end, sent_vector in sent_bounds:
            if chunk.start >= sent_start and chunk.end <= sent_end:
                ic(sent_start, chunk.start, chunk.end, sent_end)
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
    ic(sent_vector)
    sum_sq = 0.0
    for phrase_id in range(len(unit_vector)):
        ic(phrase_id, unit_vector[phrase_id])

        if phrase_id not in sent_vector:
            sum_sq += unit_vector[phrase_id] ** 2.0

    sent_rank[sent_id] = sqrt(sum_sq)
    sent_id += 1

from operator import itemgetter

sorted(sent_rank.items(), key=itemgetter(1))

limit_sentences = 5

sent_text = {}
sent_id = 0

for sent in doc.sents:
    sent_text[sent_id] = sent.text
    sent_id += 1

num_sent = 0

for sent_id, rank in sorted(sent_rank.items(), key=itemgetter(1)):
    ic(sent_id, sent_text[sent_id])
    num_sent += 1

    if num_sent == limit_sentences:
        break
