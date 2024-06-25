import torch
import sys
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from transformers.utils import logging

def generate_prompt(question, prompt_file="prompt.md", metadata_file="metadata3.sql"):
    with open(prompt_file, "r") as f:
        prompt = f.read()

    with open(metadata_file, "r") as f:
        table_metadata_string = f.read()

    prompt = prompt.format(
        user_question=question, table_metadata_string=table_metadata_string
    )
    return prompt

def get_tokenizer_model(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        trust_remote_code=True,
        torch_dtype=torch.float16,
        device_map="auto",
        attn_implementation="sdpa",
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
        use_cache=True,
    )

    return tokenizer, model

def run_inference(question, prompt_file="prompt.md", metadata_file="metadata3.sql"):
    tokenizer, model = get_tokenizer_model("defog/sqlcoder-7b-2")
    prompt = generate_prompt(question, prompt_file, metadata_file)
    eos_token_id = tokenizer.eos_token_id
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=250,
        do_sample=False,
        return_full_text=False,
        num_beams=4
    )
    generated_query = (
        pipe(
            prompt,
            num_return_sequences=1,
            eos_token_id=eos_token_id,
            pad_token_id=eos_token_id,
        )[0]["generated_text"]
        .split(";")[0]
        .split("```")[0]
        .strip()
        + ";"
    )
    return generated_query

if __name__ == "__main__":
    logging.set_verbosity_error()
    torch.cuda.empty_cache()
    print('Device name:', torch.cuda.get_device_properties('cuda').name)

    question = str(input('Write a question in natural language: '))
    print('Loading a model and generating a SQL query for answering your question...')
    print('--------------------------------------------------------------------------')
    print(run_inference(question))
    print('--------------------------------------------------------------------------')
    sys.exit()
