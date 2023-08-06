import hmac
import string
import hashlib
import base64
import requests
from requests.structures import CaseInsensitiveDict
import re
import socket
import ssl
import json

def login(username, password):
    url = "https://api.animaljam.com/login"

    headers = CaseInsensitiveDict()
    headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    data = f'screen_name={username}&password={password}'

    resp = requests.post(url, headers=headers, data=data)
    if resp.status_code == 200:
        accinfo = json.loads(resp.content)
        resp = requests.get('https://www.animaljam.com/flashvars')
        server = json.loads(resp.content)
        gameserver = re.findall(r"iss([^']+)-classic.prod.animaljam.internal", server["smartfoxServer"])
        
        packet, reply = b"<msg t='sys'><body action='rndK' r='-1'></body></msg>\x00", ""
        loginTag = f'<login z="sbiLogin"><nick><![CDATA[{username}%%0%{server["deploy_version"]}%electron%1.4.3%WIN]]></nick><pword><![CDATA[{accinfo["game_auth_token"]}]]></pword></login>'
        loginTag = loginTag.encode('utf-8')
        HOST, PORT = f'lb-iss{gameserver[0]}-classic-prod.animaljam.com', 443

        context = ssl.create_default_context()

        sock = socket.create_connection((HOST, PORT))
        global wrappedSocket
        wrappedSocket = context.wrap_socket(sock, server_hostname=HOST)
        wrappedSocket.version()
        wrappedSocket.send(packet)
        wrappedSocket.recv(1280)
        txt = wrappedSocket.recv(1280)
        start = '<k>'.encode('utf-8')
        end = '</k>'.encode('utf-8')
        key = txt[txt.find(start)+len(start):txt.rfind(end)]
        hmac_result = hmac.new(key, loginTag, hashlib.sha256)
        hsh = base64.b64encode(hmac_result.digest())
        loginpacket, loginreply = b"<msg t='sys' h=" + b'"' + hsh + b'"><body action="login" r="0">' + loginTag + b"</body></msg>\x00", ""
        wrappedSocket.send(loginpacket)
        loginresult = wrappedSocket.recv(1280)
        return loginresult
    else:
        return 'Failed to login.'

def send(content):
    global wrappedSocket
    wrappedSocket.send(content)
    result = wrappedSocket.recv(1280)
    return result

def buddy(user):
    global wrappedSocket
    wrappedSocket.send(f'%xt%o%ba%0%{user}%\x00'.encode('utf-8'))
    result = wrappedSocket.recv(1280)
    return result

def buddyRemove(user):
    global wrappedSocket
    wrappedSocket.send(f'%xt%o%bd%0%{user}%\x00'.encode('utf-8'))
    result = wrappedSocket.recv(1280)
    return result

def message(message):
    global wrappedSocket
    wrappedSocket.send(f"<msg t='sys'><body action='pubMsg' r='7302'><txt><![CDATA[{message}%9]]></txt></body></msg>\x00".encode('utf-8'))
    result = wrappedSocket.recv(1280)
    return result

def jag(user, message):
    global wrappedSocket
    wrappedSocket.send(f"%xt%o%es%1098482%{user}%1188%13%1%{message}%0%-1%0%\x00".encode('utf-8'))
    result = wrappedSocket.recv(1280)
    return result

def action(action):
    global wrappedSocket
    wrappedSocket.send(f"<msg t='sys'><body action='pubMsg' r='198575'><txt><![CDATA[:{action}:%3%4]]></txt></body></msg>\x00".encode('utf-8'))
    result = wrappedSocket.recv(1280)
    return result

def changeColor(color):
    if color == int(color):
        global wrappedSocket
        wrappedSocket.send(f"<msg t='sys'><body action='pubMsg' r='0'><txt><![CDATA[{color}%8]]></txt></body></msg>\x00".encode('utf-8'))
        result = wrappedSocket.recv(1280)
        return result
    else:
        return 'Color value must be an integer!'

def joinDen(user):
    global wrappedSocket
    wrappedSocket.send(f'%xt%o%dj%0%den{user}%1%-1%\x00'.encode('utf-8'))
    result = wrappedSocket.recv(1280)
    return result

def joinRoom(room, server):
    if server == int(server):
        global wrappedSocket
        wrappedSocket.send(f'%xt%o%rj%0%{room}#{server}%1%0%0%\x00'.encode('utf-8'))
        result = wrappedSocket.recv(1280)
        return result
    else:
        return 'Server must be an integer!'

def teleport(x, y):
    if x == int(x) and y == int(y):
        global wrappedSocket
        wrappedSocket.send(f'%xt%o%au%0%1%{x}%{y}%16%1%\x00'.encode('utf-8'))
        result = wrappedSocket.recv(1280)
        return result
    else:
        return 'XY values must be integers!'

def move(x, y):
    if x == int(x) and y == int(y):
        global wrappedSocket
        wrappedSocket.send(f'%xt%o%au%0%1%{x}%{y}%14%0%\x00'.encode('utf-8'))
        result = wrappedSocket.recv(1280)
        return result
    else:
        return 'XY values must be integers!'

def logout():
    global wrappedSocket
    wrappedSocket.close()
    return 'Successfully logged out.'