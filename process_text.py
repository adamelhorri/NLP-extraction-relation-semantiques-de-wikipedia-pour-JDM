import socket
import pickle

def process_text(text):
    # Connect to the Stanza server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 65432))

    # Send the text to the Stanza server
    client_socket.sendall(pickle.dumps(text))

    # Receive the processed document from the server
    data = b''
    while True:
        part = client_socket.recv(4096)
        if not part:
            break
        data += part
    doc = pickle.loads(data)

    client_socket.close()

    token_info_list = []

    # Iterate over each sentence in the document
    for sentence in doc.sentences:
        # Iterate over each token in the sentence
        for token in sentence.tokens:
            for word in token.words:
                token_info = {
                    'id': word.id,
                    'text': token.text,
                    'lemma': word.lemma,
                    'upos': word.upos,
                    'feats': word.feats,
                    'head': word.head,
                    'deprel': word.deprel,
                    'start_char': token.start_char,
                    'end_char': token.end_char,
                    'ner': token.ner if token.ner != 'O' else None,
                    'multi_ner': token.multi_ner if hasattr(token, 'multi_ner') else None,
                    'misc': token.misc if hasattr(token, 'misc') else None
                }
                token_info_list.append(token_info)

    return token_info_list

if __name__ == "__main__":
    text = "Les chats sont des animaux domestiques très populaires dans de nombreux foyers à travers le monde"
    tokens_info = process_text(text)

    print("WORD".ljust(15), "RELATION".ljust(15), "HEAD WORD")
    print("="*45)

    # Iterate through the tokens
    for token in tokens_info:
        head_index = token['head'] - 1  # Adjust index since it's 1-based in the output
        # Retrieve the head token
        head_token = tokens_info[head_index]
        # Print word, relation, and head word
        print(token['text'],token['upos'],end="|")
