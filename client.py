# import the necessary librabries
import socket
import tqdm
import os
import argparse

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

def send_file(filename, host, port):
    # total file size read 
    total = 0

    # get the file size
    filesize = os.path.getsize(filename)

    # create the client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"[+] One sec... trying to connect to {host}:{port}")
    client_socket.connect((host, int(port)))
    print("[+] Yay, client successfully connected to the server!")

    # send the filename and filesize
    client_socket.send(f"{filename}{SEPARATOR}{filesize}".encode())

    # progress bar to show transfer in percentage
    progress = tqdm.tqdm(range(filesize), f"Current progress of sending {filename}", unit="B", unit_scale=True, unit_divisor=1024, leave=True)        
    
    # prepare to read the file
    with open(filename, "rb") as f:
        for _ in progress:
            while total != filesize:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)

                # to check when file is done transmitting
                if total == filesize:
                    break

                # send the bytes from the client
                client_socket.sendall(bytes_read)

                # update the progress bar
                progress.update(len(bytes_read))
                total += len(bytes_read)
    
    # close the file
    f.close()

    # close the socket
    client_socket.close()

if __name__ == "__main__":
    # get the arguments to use in the function call
    parser = argparse.ArgumentParser(description="DS Lab 6")
    parser.add_argument("file")
    parser.add_argument("host")
    parser.add_argument("port")
    args = parser.parse_args()
    filename = args.file
    host = args.host
    port = args.port
    # call the function to send the file
    send_file(filename, host, port)