import tiktoken

# Paste your JSON here
conversation_json = """
hello world! how are you?
"""
enc = tiktoken.get_encoding("")

print(len(enc.encode(conversation_json)))
