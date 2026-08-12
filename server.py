import socket
import json
import subprocess
import platform
import sys

HOST = '127.0.0.1'  # Localhost (use '0.0.0.0' to accept connections from other devices on your LAN)
PORT = 65432        # Non-privileged port

def handle_request(data_str):
    """Parses JSON request, executes the corresponding action, and returns a dict response."""
    try:
        request = json.loads(data_str)
        action = request.get("action")
        payload = request.get("payload", "")

        # Request 1: System Information
        if action == "SYS_INFO":
            return {
                "status": "SUCCESS",
                "data": {
                    "os": platform.system(),
                    "os_release": platform.release(),
                    "architecture": platform.machine(),
                    "python_version": sys.version.split()[0]
                }
            }

        # Request 2: Execute Terminal Command
        elif action == "EXEC_CMD":
            if not payload:
                return {"status": "ERROR", "data": "No command provided in payload."}
            
            # Runs command in shell and captures stdout/stderr
            output = subprocess.getoutput(payload)
            return {"status": "SUCCESS", "data": output}

        # Request 3: Echo Message
        elif action == "ECHO":
            return {"status": "SUCCESS", "data": f"Server Echo: {payload}"}

        # Request 4: Server Shutdown
        elif action == "SHUTDOWN":
            return {"status": "SUCCESS", "data": "Server is shutting down..."}

        else:
            return {"status": "ERROR", "data": f"Unknown action: '{action}'"}

    except json.JSONDecodeError:
        return {"status": "ERROR", "data": "Invalid JSON format received."}
    except Exception as e:
        return {"status": "ERROR", "data": str(e)}


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Allows immediate reuse of port after stopping server
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"[SERVER] Listening on {HOST}:{PORT}...")

    while True:
        conn, addr = server_socket.accept()
        print(f"[SERVER] Connected by {addr}")
        
        while True:
            data = conn.recv(4096)
            if not data:
                break
            
            # Process incoming JSON command
            request_str = data.decode('utf-8')
            print(f"[RECEIVED]: {request_str}")

            response_dict = handle_request(request_str)
            response_json = json.dumps(response_dict)

            # Send back the JSON response
            conn.sendall(response_json.encode('utf-8'))

            # Exit server loop if client sent SHUTDOWN command
            if response_dict.get("data") == "Server is shutting down...":
                print("[SERVER] Shutting down...")
                conn.close()
                server_socket.close()
                return

        conn.close()
        print(f"[SERVER] Connection with {addr} closed.")


if __name__ == "__main__":
    start_server()