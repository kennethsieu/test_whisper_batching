import os
import tiktoken

texts = [f for f in os.listdir('.') if os.path.isfile(f)]

training = ""
validation = ""

for text in texts:
    with open(text, 'r') as file:
        data = file.read()
        data = data.split(".")

        n = len(data)

        train_data = data[:int(n*0.9)]
        val_data = data[int(n*0.9):]

        t = ".".join(train_data)
        v = ".".join(val_data)

        training = " ".join([training, t])
        validation = " ".join([validation, v])

enc = tiktoken.get_encoding("gpt2")
train_ids = enc.encode_ordinary(training)
val_ids = enc.encode_ordinary(validation)
print(f"train has {len(train_ids):,} tokens")
print(f"val has {len(val_ids):,} tokens")
    
with open("training.txt", "w", encoding="utf-8") as txt:
    txt.write(training)

with open("validation.txt", "w", encoding="utf-8") as txt:
    txt.write(validation)

