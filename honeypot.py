#!/usr/bin/env python3

import socket, paramiko, threading

class SSH_Server(paramiko.ServerInterface):
	def check_auth_password(self, username, password):
		creds = f"{username}:{password}"
		with open('./honeypot_log/honeypot_creds.log', 'a') as log_file_creds:
			print(creds, file=log_file_creds)
		return paramiko.AUTH_FAILED
		
	def check_auth_publickey(self, username, key):
		return paramiko.AUTH_FAILED
		
def handle_connection(client_sock, server_key):
	transport = paramiko.Transport(client_sock)
	transport.add_server_key(server_key)
	ssh = SSH_Server()
	transport.start_server(server=ssh)
	
def main():
	server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_sock.setsockopt(socket.SOL_SOCKET, socket. SO_REUSEADDR, 1)
	server_sock.bind(('0.0.0.0', 22))
	server_sock.listen(100)
	
	server_key = paramiko.RSAKey.generate(2048)
	
	while True:
		client_sock, client_addr = server_sock.accept()
		clientAddr = f"Connection: {client_addr[0]}:{client_addr[1]}"
		with open('./honeypot_log/honeypot_addr.log', 'a') as log_file_addr:
			print(clientAddr, file=log_file_addr)
		t = threading.Thread(target=handle_connection, args=(client_sock, server_key))
		t.start()
		
if __name__ == "__main__":
	main()
