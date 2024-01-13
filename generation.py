import logging
import os
import sys
import time
from timeit import default_timer as timer
from pathlib import Path
import torch_directml
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, TextStreamer
from transformers import StoppingCriteriaList, StoppingCriteria
from datetime import datetime, timedelta
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

sys.stdout.reconfigure(encoding='utf-8')

io_folder_path = "io"
io_file_path = os.path.join("io", "io.txt")
Path(io_folder_path).mkdir(parents=True, exist_ok=True)
Path(io_file_path).touch(exist_ok=True)

# Mix of copy-pasted code from
# - https://huggingface.co/AI-Sweden-Models/gpt-sw3-1.3b
# - https://learn.microsoft.com/en-us/windows/ai/directml/gpu-pytorch-windows

device = torch_directml.device()
# device = "cpu"

model_name = "../gpt-sw3-1.3b"

# Initialize Tokenizer & Model
logging.info("Loading model...")
tokenizer = AutoTokenizer.from_pretrained(model_name, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(model_name, local_files_only=True)
streamer = TextStreamer(tokenizer, skip_prompt=False)
model.eval()
model.to(device)

class InputChangeHandler(FileSystemEventHandler):
    def __init__(self) -> None:
        self.last_input = ""
        self.last_output = ""
        super().__init__()
    
    def on_modified(self, event):     
        if event.src_path != io_file_path:
            return
        
        with open(event.src_path, "r", encoding="utf-8") as f:
            prompt = f.read()
        
        if prompt == self.last_input or prompt == self.last_output:
            return
        
        self.last_input = prompt
        
        start = timer()
        logging.info("Generating...")
        
        generator = pipeline('text-generation', tokenizer=tokenizer, model=model, device=device)
        generated_text = generator(
            prompt,
            max_new_tokens=1024,
            max_time=30.0,
            do_sample=True,
            temperature=0.6,
            repetition_penalty=2.0,
            top_p=1,
            streamer=streamer
        )[0]["generated_text"]

        # When using streamer = TextStreamer(tokenizer, skip_prompt=False),
        # the generated text will include the prompt.
        self.last_output = generated_text
        
        end = timer()
        logging.info(f"Done text generation. (Time took: {timedelta(seconds=end - start)})")

        with open(event.src_path, "w+", encoding="utf-8") as f:
            f.write(self.last_output)
        
        backup_path = os.path.join("io", f"{datetime.now().astimezone().replace(microsecond=0).isoformat().replace(':', '')}.txt")
        with open(backup_path, "w+", encoding="utf-8") as f:
            f.write(self.last_output)
            


if __name__ == "__main__":
    try:
        observer = PollingObserver()
        
        event_handler = InputChangeHandler()
        observer.schedule(event_handler,  path=io_folder_path,  recursive=False)
        observer.start()
        
        logging.info(f"Ready! Edit the content of {io_file_path} to start the text generation.")
        
        while True:
            time.sleep(0.01)
    except KeyboardInterrupt:
        logging.info("Exiting...")
        observer.stop()
    observer.join()
