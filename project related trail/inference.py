from transformers import T5ForConditionalGeneration, T5Tokenizer, pipeline

model = T5ForConditionalGeneration.from_pretrained("./t5_phrase_model", local_files_only=True)
tokenizer = T5Tokenizer.from_pretrained("./t5_phrase_model", local_files_only=True)

generator = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer
)

test_sentence = "v100 hp text hook required"
known_phrases = "v100 v3 sp, audio control, navigation system"
prompt = f"extract known pharases from the sentence:{test_sentence} known phrases: {known_phrases}  provide tag as known_phrases and other non extracted sentence should name as unknown_phrases"
output = generator(prompt, max_length=62)
print("Generated Phrases:", output[0]["generated_text"])
