# NLPaper

**NLPaper** is a telegram bot that will help you to highlight the most
important information of a research paper.

## Aim 

To develop an extractive summarization system for research papers.

## Tasks

1. Research current approaches for extractive summarization;
2. develop the system architectures (diagrams);
3. collect and analyze the data from research papers (arXiv);
4. develop an API for PDF files edits (including telegram bot);
5. develop preprocessing pipeline for the extracted text;
6. prepare pretrained transformer models (DistilBERT and ALBERT) and
   tokenizers;
7. fine-tune the models using a masked language modeling (MLM) objective;
8. use the models as feature extractors with a summarizer and get top n
   sentences;
9. get the PDF coordinates of selected parts of the text and highlight them;
10. evaluate metrics on the dataset (perplexity);
11. choose the best model based on the metric;
12. deploy the service on a server (Heroku);
13. optimize the selected model (or data), such as compression;
14. write a report about the developed system.

## Dataset

**Link:** 
[CShorten/ML-ArXiv-Papers](https://huggingface.co/datasets/CShorten/ML-ArXiv-Papers).

**Description:** 
The dataset consists of 117592 research paper abstracts from arXiv. The average
length of the abstracts is 1157 symbols.

**Expediency of its use:** 
The abstracts can be used to fine-tune BERT-based models using masked language
modeling technique. Since a BERT model was pre-trained using only an unlabeled,
plain text corpus (English Wikipedia, the Brown Corpus), it can be less
prepared for a scientific language such as that found in arXiv dataset.
However, the dataset can be edited with masking and fed into the models. Then
it is possible to use such a fine-tuned model for sentence embeddings.
