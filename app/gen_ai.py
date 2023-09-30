"""
This code should be run on GPU for best performance
Use this link to run the code on collab https://colab.research.google.com/drive/1g3k550B45gi8xAA2GpppUelmtseOnEnH?usp=sharing
"""
# Dependencies
"""
pip install the following dependencies in your env when you decide to run it locally

!pip install auto-gptq --extra-index-url https://huggingface.github.io/autogptq-index/whl/cu117/
!pip install -q -U optimum auto-gptq accelerate
!pip install transformers
!pip install transformers[torch]
"""

#Transformer models(from huggingface)
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import InferenceClient

import pandas as pd
import numpy as np
##this function will be used for inference. 
def inference(text, model, tokenizer, max_input_tokens=1000, max_output_tokens=512):
  # Tokenize
  input_ids = tokenizer.encode(
          text,
          return_tensors="pt",
          truncation=True,
          max_length=max_input_tokens
  )

  # Generate
  device = model.device
  generated_tokens_with_prompt = model.generate(
    input_ids=input_ids.to('cuda'),
    max_length=max_output_tokens
  )

  # Decode
  generated_text_with_prompt = tokenizer.batch_decode(generated_tokens_with_prompt, skip_special_tokens=True)

  # Strip the prompt
  generated_text_answer = generated_text_with_prompt[0]

  return generated_text_answer

model_id = "TheBloke/Llama-2-7b-Chat-GPTQ"#llama-2 7b finetuned for chat (capable of running on a single GPU due to quantization and LoRa configs)
tokenizer = AutoTokenizer.from_pretrained(model_id)
base_model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto")
tokenizer.pad_token = tokenizer.eos_token



question = input("Ask a question: ") #take input question
#prompt template(alpaca template)
prompt_template = f""" You are legal practioner with indepth knowledge about law. write a response that correcty answers the following question

### Instruction:
{question}

### Response: """
print("Question:", question)
print("Model's answer: ")
print(inference(prompt_template, base_model, tokenizer))

"""
Simplest method is to use huggingface inference api
However the previous method will be good for finetuning on our own documents
"""



client = InferenceClient(token='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')
question = input("Ask a question: ") #take input question
#prompt template(alpaca template)
prompt_template = f""" You are legal practitioner with indepth knowledge about law. write a response that correcty answers the following question

### Instruction:
{question}
### Response: """
response=client.text_generation(prompt=prompt_template,max_new_tokens=1000,model='tiiuae/falcon-7b-instruct')
print(response)