# Overview

This project is a lightweight, socket-based Remote Control Application designed to enable secure and reliable command execution across a network. As a software engineer, my goal for this project was to gain a practical, hands-on understanding of low-level network programming, application-layer protocol design, and stream-based data transmission without relying on high-level web frameworks.

The system consists of two separate Python programs: a **Server** that listens for incoming remote commands and executes system operations, and a **Client** that provides an interactive interface for sending requests and displaying execution results.

### How to Run the Software

1. **Start the Server:**
   Open a terminal and run python server.py 
   Open a split terminal and run python client.py 
   Go through the selections on client.py 

[Software Demo Video](https://youtu.be/PxBq0mdMLR0)

## Purpose
The primary purpose of writing this software was to explore the OSI Transport and Application layers in practice, specifically learning how to establish reliable TCP socket connections, encode and decode custom JSON message formats, and safely handle remote command execution (subprocess).

## Network Communication
Software Architecture
This software uses a traditional Client-Server Architecture:

Server: Acts as a passive listener, receiving incoming connections, parsing commands, executing system operations, and returning structured responses.

Client: Acts as the active requester, initiating TCP handshakes, formatting user requests into structured messages, and displaying server responses.

Transport Protocol & Port
Protocol: TCP (Transmission Control Protocol) was selected to guarantee reliable, ordered, and error-checked data delivery, which is essential for executable system commands.

Port Number: Default is set to 65432 (a non-privileged user port), running on the loopback address (127.0.0.1) for local testing.

Message Structure Format: Data exchanged between the client and server is structured as **UTF-8 encoded JSON strings**:

Client Request Format:
JSON
{
  "action": "EXEC_CMD",
  "payload": "dir"
}

Server Response Format:
JSON
{
  "status": "SUCCESS",
  "data": "Volume in drive C has no label..."
}

## Development Environment
Development Tools: Visual Studio Code, Git, GitHub, Terminal / Windows Command Prompt

Programming Language: Python 3.x

Libraries & Modules Used:

socket – Low-level networking interface for TCP connection management

json – Serializing and deserializing network data payloads

subprocess – Executing underlying OS terminal commands on the server

platform & sys – Extracting host system metadata
   
# Useful Websites

- [Python Official Socket Programming Documentation](https://docs.python.org/3/library/socket.html)
- [Real Python: Socket Programming in Python (Guide)](https://realpython.com/python-sockets/)
- [GeeksforGeeks: Socket Programming in Python](https://www.geeksforgeeks.org/python/socket-programming-python/)

## Future Work
1. Graphical User Interface (GUI): Replace the terminal-based menu on the client with a clean desktop interface built using Tkinter or PySide/PyQt.

2. Expanded Command Requests: Add support for file transfer capabilities (uploading/downloading files) and taking remote desktop screenshots.

3. Security & Authentication: Implement SSL/TLS encryption for socket streams and add password-based authentication to prevent unauthorized command execution on the server.