#include "HttpRequests.h"

HttpRequests::HttpRequests(std::string url, const char *servicePort) {
    char hostName[64]{};
    strcpy_s(_url, url.c_str());
    int pos = url.find("://");
    if (pos < 0) {
        int p = url.find("/");
        if (p > 0) {
            strcpy_s(_hostAddr, url.substr(0, p).c_str());
        } else {
            strcpy_s(_hostAddr, url.c_str());
        }
        if (servicePort == "") {
            strcpy_s(_PORT, "https");
        } else {
            strcpy_s(_PORT, servicePort);
        }
    } else {
        int p = url.find("/", pos + 3);
        if (p > 0) {
            strcpy_s(_hostAddr, url.substr(pos + 3, p - pos - 3).c_str());
        } else  {
            strcpy_s(_hostAddr, url.substr(pos + 3).c_str());
        }
        if (servicePort == "") {
            strcpy_s(_PORT, url.substr(0, pos).c_str());
        }
        else {
            strcpy_s(_PORT, servicePort);
        }
    }
    //std::cout << _hostAddr << ":" << _PORT << std::endl;
    //strcpy_s(_hostAddr, hostName);
    //strcpy_s(_PORT, servicePort);
    if (strcmp(_PORT, "443") == 0 || strcmp(_PORT, "https") == 0) {
        _isSSL = true;
    }

    memset(_sendMessage, 0, sizeof(_sendMessage));
    int err = 0;
    _wVersionRequested = MAKEWORD(2, 2);
    err = WSAStartup(_wVersionRequested, &_wsaData);
    if (err != 0) {
        printf("WSAStartup failed with error: %d\n", err);
    }
    if (LOBYTE(_wsaData.wVersion) != 2 || HIBYTE(_wsaData.wVersion) != 2) {
        printf("Could not find a usable version of Winsock.dll\n");
        WSACleanup();
    }

    addrinfo hints{};
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_protocol = IPPROTO_TCP;

    err = getaddrinfo(_hostAddr, _PORT, &hints, &_result);
    if (err != 0) {
        printf("GetHostIP failed with error: %d\n", err);
        WSACleanup();
    }

    _connectSocket = INVALID_SOCKET;
    _connectSocket = socket(_result->ai_family, _result->ai_socktype, _result->ai_protocol);
    if (_connectSocket == INVALID_SOCKET) {
        printf("Error at socket(): %ld\n", WSAGetLastError());
        freeaddrinfo(_result);
        WSACleanup();
    }
    int nNetTimeout = 500;
    setsockopt(_connectSocket, SOL_SOCKET, SO_RCVTIMEO, (char*)&nNetTimeout, sizeof(int));

    SSLeay_add_ssl_algorithms();
    OpenSSL_add_all_algorithms();
    SSL_load_error_strings();
    _ctx = SSL_CTX_new(_meth);
    if (_ctx == NULL) {
        printf("SSL CTX failed with error");
    }
    _ssl = SSL_new(_ctx);
    SSL_set_fd(_ssl, _connectSocket);
    SSL_CTX_set_verify(_ctx, SSL_VERIFY_PEER, NULL);
}

HttpRequests::~HttpRequests() {
    SSL_shutdown(_ssl);
    SSL_free(_ssl);
    SSL_CTX_free(_ctx);
    closesocket(_connectSocket);
    WSACleanup();
}

int HttpRequests::connectHost() {
    int err = 0;
    err = connect(_connectSocket, _result->ai_addr, sizeof(*_result->ai_addr));
    if (err != 0) {
        printf("ConnectHost failed with error: %d\n", err);
        return -1;
    }

    if (_isSSL) {
        err = SSL_connect(_ssl);
        if (err < 0) {
            printf("ConnectSSL failed with error: %d\n", err);
            return -1;
        }
    }

    return 0;
}

int HttpRequests::generateMsg(const char* method, std::string url, Json::Value headers, Json::Value cookies, std::string data, bool decode, unsigned short recvLen) {
    std::stringstream stream;
    _recvLen = recvLen;
    if (data != "") {
        strcpy_s(_sendData, strlen(data.c_str()) + 1, data.c_str());
    }
    if (decode && data != "") {
        encode(_sendData);
    }
    if (url != "") {
        strcpy_s(_url, url.c_str());
    }
    if (method == "GET") {
        if (data != "") {
            stream << "GET " << _url << "?" << _sendData << " HTTP/1.1" << "\r\n";
        } else {
            stream << "GET " << _url << " HTTP/1.1" << "\r\n";
        }
    } else {
        stream << "POST " << _url << " HTTP/1.1" << "\r\n";
    }
    stream << "Host: " << _hostAddr << "\r\n";
    if (headers != Json::nullValue) {
        Json::Reader reader;
        Json::Value::Members member = headers.getMemberNames();
        std::string key;
        for (Json::Value::Members::iterator iter = member.begin(); iter < member.end(); iter++) {
            key = (std::string)(*iter);
            stream << key << ": ";
            std::string s = headers[key].toStyledString();
            s = replaceStrAll(s, "\"", "");
            s = replaceStrAll(s, "\r", "");
            s = replaceStrAll(s, "\n", "");
            stream << s << "\r\n";
        }
    }

    if (cookies != Json::nullValue) {
        Json::Reader reader;
        Json::Value::Members member = cookies.getMemberNames();
        std::string key;
        stream << "cookie: ";
        for (Json::Value::Members::iterator iter = member.begin(); iter < member.end(); iter++) {
            if (iter != member.begin()) {
                stream << "; ";
            }
            key = (std::string)(*iter);
            stream << key << "=";
            std::string s = cookies[key].toStyledString();
            s = replaceStrAll(s, "\"", "");
            s = replaceStrAll(s, "\r", "");
            s = replaceStrAll(s, "\n", "");
            stream << s;
        }
        stream << "\r\n";
    }
    stream << "\r\n";
    if (method == "POST" && data != "") {
        stream << _sendData;
    }

    const std::string str = stream.str();
    strcpy_s(_sendMessage, str.c_str());
    //std::cout << _sendMessage << std::endl;
    return 0;
}

int HttpRequests::generateMsg(const char* method, std::string url, Json::Value headers, std::string cookies, std::string data, bool decode, unsigned short recvLen) {
    std::stringstream stream;
    _recvLen = recvLen;
    if (data != "") {
        strcpy_s(_sendData, strlen(data.c_str()) + 1, data.c_str());
    }
    if (decode && data != "") {
        encode(_sendData);
    }
    if (url != "") {
        strcpy_s(_url, url.c_str());
    }
    if (method == "GET") {
        if (data != "") {
            stream << "GET " << _url << "?" << _sendData << " HTTP/1.1" << "\r\n";
        }
        else {
            stream << "GET " << _url << " HTTP/1.1" << "\r\n";
        }
    }
    else {
        stream << "POST " << _url << " HTTP/1.1" << "\r\n";
    }
    stream << "Host: " << _hostAddr << "\r\n";
    if (headers != Json::nullValue) {
        Json::Reader reader;
        Json::Value::Members member = headers.getMemberNames();
        std::string key;
        for (Json::Value::Members::iterator iter = member.begin(); iter < member.end(); iter++) {
            key = (std::string)(*iter);
            stream << key << ": ";
            std::string s = headers[key].toStyledString();
            s = replaceStrAll(s, "\"", "");
            s = replaceStrAll(s, "\r", "");
            s = replaceStrAll(s, "\n", "");
            stream << s << "\r\n";
        }
    }
    if (cookies != "") {
        stream << "cookie: " << cookies << "\r\n";
    }
    stream << "\r\n";
    if (method == "POST" && data != "") {
        stream << _sendData;
    }

    const std::string str = stream.str();
    strcpy_s(_sendMessage, str.c_str());
    //std::cout << _sendMessage << std::endl;
    return 0;
}

std::string HttpRequests::replaceStrAll(std::string s, std::string old_str, std::string new_str) {
    std::string::size_type pos = 0;
    while ((pos = s.find(old_str)) != std::string::npos) {
        s.replace(pos, old_str.length(), new_str);
    }
    return s;
}

char* HttpRequests::request(bool decode) {
    memset(_recvBuf, '\0', sizeof(_recvBuf));
    if (_isSSL)
        SSL_write(_ssl, _sendMessage, strlen(_sendMessage));
    else
        send(_connectSocket, _sendMessage, strlen(_sendMessage), 0);
    char recvBuf[4097]{};
    memset(recvBuf, '\0', sizeof(recvBuf));
    int ret = 0, cnt = 0;
    if (_recvLen >= 4096) {
        if (_isSSL) {
            while (ret = SSL_read(_ssl, recvBuf, 4096) > 0) {
                if (recvBuf[0] == '0' && strlen(recvBuf) == 5 || cnt >= 7) {
                    break;
                }
                if (decode) {
                    encode(recvBuf);
                }
                if (recvBuf[strlen(recvBuf) - 1] == '\n' && recvBuf[strlen(recvBuf) - 2] == '\r') {
                    recvBuf[strlen(recvBuf) - 2] = '\0';
                }
                if (cnt > 0) {
                    for (int i = 0; i < 10; i++) {
                        if (recvBuf[i] == '\r' && recvBuf[i + 1] == '\n') {
                            memmove(recvBuf, recvBuf + i + 2, strlen(recvBuf) - i - 1);
                        }
                    }
                }
                strcat_s(_recvBuf, recvBuf);
                memset(recvBuf, '\0', sizeof(recvBuf));
                cnt++;
            }
        }
        else
        {
            while (ret = send(_connectSocket, recvBuf, 4096, 0) > 0) {
                if (recvBuf[0] == '0' && strlen(recvBuf) == 5 || cnt >= 7) {
                    break;
                }
                if (decode) {
                    encode(recvBuf);
                }
                if (recvBuf[strlen(recvBuf) - 1] == '\n' && recvBuf[strlen(recvBuf) - 2] == '\r') {
                    recvBuf[strlen(recvBuf) - 2] = '\0';
                }
                if (cnt > 0) {
                    for (int i = 0; i < 10; i++) {
                        if (recvBuf[i] == '\r' && recvBuf[i + 1] == '\n') {
                            memmove(recvBuf, recvBuf + i + 2, strlen(recvBuf) - i - 1);
                        }
                    }
                }
                strcat_s(_recvBuf, recvBuf);
                memset(recvBuf, '\0', sizeof(recvBuf));
                cnt++;
            }
        }
    } else {
        if(_isSSL)
            SSL_read(_ssl, recvBuf, 4096);
        else
            send(_connectSocket, recvBuf, 4096, 0);
        if (decode) {
            encode(recvBuf);
        }
        strcat_s(_recvBuf, recvBuf);
    }
    _recvBuf[strlen(_recvBuf)] = '\0';

    return _recvBuf;
}

int HttpRequests::encode(char* text) {
    TCHAR wscBuffer[4097]{ 0 };
    int recLen = strlen(text);
    MultiByteToWideChar(CP_UTF8, 0, text, recLen + 1, wscBuffer, sizeof(wscBuffer) / sizeof(wchar_t));
    memset(text, 0, recLen);
    WideCharToMultiByte(CP_ACP, 0, wscBuffer, -1, text, recLen, NULL, NULL);
    return 0;
}

char* HttpRequests::getBody(char* message) {
    for (int i = 0; i < strlen(message) - 3; i++) {
        if (message[i] == '\r' && message[i + 1] == '\n' && message[i + 2] == '\r' && message[i + 3] == '\n') {
            i += 4;
            for (int j = i; j < (strlen(message) > 13 + i ? 10 + i : strlen(message) - 3 + i); j++) {
                if (message[ j] == '\r' && message[ j+1] == '\n') {
                    memmove(message, message +  j + 2, strlen(message) - j - 1);
                    return message;
                }
            }
            return message + i;
        }
    }
    return message;
}

Json::Value* HttpRequests::getJson(bool decode) {
    Json::Value* root = new Json::Value;
    Json::Reader reader;
    reader.parse(HttpRequests::getBody(request(decode)), *root);
    return root;
}