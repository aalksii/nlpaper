# NLPaper

**NLPaper** is a telegram bot that will help you to highlight the most important information of a research paper.

**Aim:** to develop an extractive summarization system for research papers.

**Tasks:**

1. research current approaches for extractive summarization;
2. develop the system architectures (diagrams);
3. collect and analyze the data from research papers (arXiv);
4. develop an API for pdf files edits (including telegram bot);
5. develop preprocessing pipeline for the extracted text;
6. prepare pretrained transformer models (DistilBERT and ALBERT) and tokenizers;
7. fine-tune the models using a masked language modeling (MLM) objective;
8. use the models as feature extractors with a summarizer and get top n sentences; 
9. get the PDF coordinates of selected parts of the text and highlight them;
10. evaluate metrics on the dataset (perplexity);
11. choose the best model based on the metric; 
12. deploy the service on a server (Heroku);
13. optimize the selected model (or data), such as compression;
14. write a report about the developed system.

**Dataset:** [arXiv Papers](https://huggingface.co/datasets/CShorten/ML-ArXiv-Papers).

**Dataset description and expediency of its use:**

The dataset consists of 117592 research paper abstracts from arXiv. 
The average length of the abstracts is 1157 symbols.