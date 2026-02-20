

def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """
    Split text into chunks with overlap
    Example: For text "Hello World Programming" with chunk_size=8 and overlap=3:
        Chunk 1: "Hello Wo" (positions 0-7)
        Chunk 2: "o World " (positions 5-12, overlapping "o W")
        Chunk 3: "ld Progr" (positions 10-17, overlapping "ld ")
        And so on...
    """
    if not text:
        return []

    if len(text) <= chunk_size:
        return [text]

    chunks = []
    current_position = 0

    while current_position < len(text):
        end_position = min(current_position + chunk_size, len(text))
        chunk = text[current_position:end_position]
        chunks.append(chunk)

        current_position = end_position - overlap

        if current_position >= len(text) - overlap and end_position == len(text):
            break

    return chunks