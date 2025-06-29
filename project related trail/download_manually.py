from transformers import T5ForConditionalGeneration, T5Tokenizer

# Download and save to a folder (e.g., './t5_phrase_model')
model = T5ForConditionalGeneration.from_pretrained("t5-small")  # or your custom model
tokenizer = T5Tokenizer.from_pretrained("t5-small")

# Save locally
model.save_pretrained("./t5_phrase_model")
tokenizer.save_pretrained("./t5_phrase_model")
