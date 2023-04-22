from utils import pdf_to_text, get_ranked_sentences

text = pdf_to_text('example.pdf')
ranked_sentences = get_ranked_sentences(text)
print(ranked_sentences)
print()
