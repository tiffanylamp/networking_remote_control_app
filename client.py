import socket
import json

HOST = '127.0.0.1'  # Server IP address
PORT = 65432        # Server Port

def send_request(sock, action, payload=""):
    """Helper function to format, send, and print JSON requests and responses."""
    request_dict = {
        "action": action,
        "payload": payload
    }
    
    # 1. Encode JSON and send
    sock.sendall(json.dumps(request_dict).encode('utf-8'))

    # 2. Receive response
    data = sock.recv(4096)
    if not data:
        print("[CLIENT] Server closed connection unexpectedly.")
        return None

    # 3. Parse JSON response
    response = json.loads(data.decode('utf-8'))
    return response


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
        print(f"[CLIENT] Connected to server at {HOST}:{PORT}")
    except ConnectionRefusedError:
        print("[CLIENT] Connection failed! Ensure 'server.py' is running first.")
        return

    while True:
        print("\n--- Remote Control Menu ---")
        print("1. Get System Info (SYS_INFO)")
        print("2. Execute Command (EXEC_CMD)")
        print("3. Echo Message (ECHO)")
        print("4. Shutdown Server (SHUTDOWN)")
        print("5. Exit Client")
        
        choice = input("Select an option (1-5): ").strip()

        if choice == '1':
            res = send_request(client_socket, "SYS_INFO")
            print("\nServer Output:", json.dumps(res.get("data"), indent=2))

        elif choice == '2':
            cmd = input("Enter terminal command (e.g., 'dir' or 'ls'): ")
            res = send_request(client_socket, "EXEC_CMD", payload=cmd)
            print(f"\nServer Output:\n{res.get('data')}")

        elif choice == '3':
            msg = input("Enter message to echo: ")
            res = send_request(client_socket, "ECHO", payload=msg)
            print(f"\nServer Output: {res.get('data')}")

        elif choice == '4':
            res = send_request(client_socket, "SHUTDOWN")
            print(f"\nServer Output: {res.get('data')}")
            break

        elif choice == '5':
            print("Exiting client...")
            break
        else:
            print("Invalid choice, try again.")

    client_socket.close()


if __name__ == "__main__":
    start_client()