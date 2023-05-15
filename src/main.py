from configs import *
from utils import highlight

highlight(str(downloaded_path / input_file_name),
          str(downloaded_path / output_file_name),
          limit_sentences=limit_sentences)
