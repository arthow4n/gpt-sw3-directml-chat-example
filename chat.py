import argparse
import torch_directml
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from transformers import StoppingCriteriaList, StoppingCriteria

import torch
import sentencepiece

# Mix of copy-pasted code from
# - https://huggingface.co/AI-Sweden-Models/gpt-sw3-1.3b-instruct
# - https://learn.microsoft.com/en-us/windows/ai/directml/gpu-pytorch-windows

device = torch_directml.device()
# device = "cpu"

model_name = "../gpt-sw3-1.3b-instruct"

# Initialize Tokenizer & Model
tokenizer = AutoTokenizer.from_pretrained(model_name, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(model_name, local_files_only=True)
model.eval()
model.to(device)

class StopOnTokenCriteria(StoppingCriteria):
    def __init__(self, stop_token_id):
        self.stop_token_id = stop_token_id

    def __call__(self, input_ids, scores, **kwargs):
        return input_ids[0, -1] == self.stop_token_id

stop_on_token_criteria = StopOnTokenCriteria(stop_token_id=tokenizer.bos_token_id)

while True:
    print("User: ", end="")
    userSays = input().strip()
    if userSays == "":
        print("\n")
        continue

    prompt = f"""
<|endoftext|><s>
User:
{userSays}
<s>
Bot:
""".strip()

    input_ids = tokenizer(prompt, return_tensors="pt")["input_ids"].to(device)
    generated_token_ids = model.generate(
        inputs=input_ids,
        max_new_tokens=1024,
        do_sample=True,
        temperature=0.6,
        top_p=1,
        stopping_criteria=StoppingCriteriaList([stop_on_token_criteria])
    )[0]
    generated_text = tokenizer.decode(generated_token_ids[len(input_ids[0]):-1])

    print(f"Bot: {generated_text.strip()}\n\n")
