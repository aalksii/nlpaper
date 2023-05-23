from transformers import AutoConfig, AutoTokenizer, AutoModelForMaskedLM


def load_tokenizer_and_model(model_name):
    if './' in model_name:
        # Load model, model config and tokenizer via Transformers
        custom_config = AutoConfig.from_pretrained(model_name,
                                                   local_files_only=True)
        custom_config.output_hidden_states = True
        tokenizer = AutoTokenizer.from_pretrained(model_name,
                                                  config=custom_config,
                                                  local_files_only=True)
        model = AutoModelForMaskedLM.from_pretrained(model_name,
                                                     config=custom_config,
                                                     local_files_only=True)
    else:
        # Load tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForMaskedLM.from_pretrained(model_name)
    return tokenizer, model
