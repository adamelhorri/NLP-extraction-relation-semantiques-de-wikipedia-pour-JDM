import stanza
import socket
import pickle

# Initialize Stanza pipeline for French
nlp = stanza.Pipeline('fr')

# Create a socket for inter-process communication
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 65432))
server_socket.listen(1)

print("Stanza pipeline initialized and server is listening on port 65432.")

while True:
    conn, addr = server_socket.accept()
    data = conn.recv(4096)
    if data:
        if data == b'shutdown':
            break
        text = pickle.loads(data)
        doc = nlp(text)
        conn.sendall(pickle.dumps(doc))
    conn.close()

server_socket.close()
print("Stanza pipeline server shut down.")
