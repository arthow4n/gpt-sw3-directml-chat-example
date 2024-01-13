# gpt-sw3-directml-chat-example

Random notes for trying out Swedish large language model https://www.ai.se/sv/projekt/gpt-sw3 on my machine. I'm not a Python expert 🤷‍♂️.

## Setup

```sh
# Download the models
cd ../
git lfs install
git clone https://huggingface.co/AI-Sweden-Models/gpt-sw3-1.3b-instruct
git clone https://huggingface.co/AI-Sweden-Models/gpt-sw3-1.3b

cd -
source venv/Scripts/activate
pip install -r requirements.txt # created using pipreqs
```

## Chat examples

```sh
# Enable the venv in the terminal first before running.
source venv/Scripts/activate
# Start the chat loop
python chat.py
```

### Grammar check

```
User: Rätta språkfelen i följande meningen: Jag kört ett rött bil igår.
Bot: Jag körde en röd bil igår.
```

```
User: Rätta språkfelen i följande meningen: Jag ska kör ett rött bil imorgon om jag behöver inte jobba.
Bot: Jag ska köra en röd bil imorgon om jag inte behöver arbeta.
```

### Others

There're some hallucinations here.

```
User: Vad kostar en etta i Göteborg?
Bot: I genomsnitt kostar en lägenhet i centrala Göteborg cirka 1,4 miljoner svenska kronor (2023) per månad.

Det är värt att notera att detta kan variera beroende på faktorer som plats, storlek och kvalitet på lägenheten. Dessutom kan det finnas skillnader mellan olika 
delar av staden, så det är alltid en bra idé att göra lite forskning innan du gör en investering.
```

```
User: Vad kostar en etta i Göteborg?
Bot: Den genomsnittliga hyran för en lägenhet i centrala Göteborg är runt 7 500 kronor per månad. Detta kan dock variera beroende på en rad faktorer, inklusive plats, storlek och typ av egendom som används.

Det är också värt att notera att priset på en lägenhet i centrala Göteborg kan variera kraftigt beroende på faktorer som läge, storlek och typ av egendom som används. Det är därför viktigt att göra lite forskning och jämföra priser från olika källor innan du gör en bindande offert.
```

## Text generation example

```sh
# Enable the venv in the terminal first before running.
source venv/Scripts/activate
# Start the generation loop
python generation.py

# A file io/io.txt will be created upon start.
# 1. Edit io/io.txt and save, the content in that file will be used as prompt, this will trigger the text generation.
# 2. The process will generate and write back to io/io.txt.
# 3. Go back to 1., text generation is only triggered when the content of io/io.txt has changed.
```

# Known issues

The GPU loaded the language model and did the computation, but in the terminal it showed the warning message below:

```
C:\Users\...\AppData\Local\Programs\Python\Python310\lib\site-packages\transformers\generation\utils.py:823: UserWarning: The operator 'aten::repeat_interleave.Tensor' is not currently supported on the DML backend and will fall back to run on the CPU. This may have performance implications. (Triggered internally at D:\a\_work\1\s\pytorch-directml-plugin\torch_directml\csrc\dml\dml_cpu_fallback.cpp:17.)
  input_ids = input_ids.repeat_interleave(expand_size, dim=0)
```
