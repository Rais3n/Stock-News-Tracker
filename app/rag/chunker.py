def create_chunks(text):
    length = len(text)
    chunk_length = 750
    chunks = []
    for start in range(0, length-1, chunk_length):
        chunks.append(text[start:start+chunk_length])
    return chunks
