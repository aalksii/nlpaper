from utils import highlight_ranked
from configs import *


highlight_ranked(str(downloaded_path / input_file_name),
                 str(downloaded_path / output_file_name),
                 limit_sentences=limit_sentences)
