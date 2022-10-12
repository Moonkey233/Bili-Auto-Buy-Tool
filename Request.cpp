#include "Request.h"

char* Request::get(bool decode)
{
	SSL_write(ssl, sendData, sendLength);

	if (decode) {
		memset(rec, '\0', sizeof(rec));
		memset(buf, '\0', sizeof(buf));
		int recvLen = 1024;
		char recvBuf[1025]{};
		int ret = 0;
		while (ret = SSL_read(ssl, recvBuf, recvLen) > 0)
		{
			strcat(rec, recvBuf);
			memset(recvBuf, '\0', sizeof(recvBuf));
		}
		TCHAR wscBuffer[51200]{};
		int recLen = strlen(rec);
		MultiByteToWideChar(CP_UTF8, 0, rec, recLen + 1, wscBuffer, sizeof(wscBuffer) / sizeof(wchar_t));
		memset(rec, 0, recLen);
		WideCharToMultiByte(CP_ACP, 0, wscBuffer, -1, rec, recLen, NULL, NULL);
	}
	else
	{
		memset(rec, '\0', 1024);
		memset(buf, '\0', 1024);
		SSL_read(ssl, rec, 1024);
	}

	rec[strlen(rec)] = '\0';
	if (decode) {
		int i = strlen(rec) - 1;
		while (rec[i] == '\n' || rec[i] == '\r' || rec[i] == '0') {
			rec[i] = '\0';
			i--;
		}
	}

	for (int i = strlen(rec) - 1; i >= 0; i--) {
		if (decode) {
			if (rec[i] != '\n' || rec[i - 1] != '\r' || rec[i - 2] != '\n' || rec[i - 3] != '\r') {
				if (rec[i] == '\n' || rec[i] == '\r') {
					rec[i] = '0';
				}
				continue;
			}
			else {
				int j = 0;
				while (rec[i] != '{') {
					i++;
				}
				while (rec[i] != '\0') {
					buf[j++] = rec[i++];
				}
				buf[j] = '\0';
				break;
			}
		}
		else
		{
			if (rec[i] != '\n') {
				continue;
			}
			else {
				int j = 0;
				while (rec[++i] != '\0') {
					buf[j++] = rec[i];
				}
				buf[j] = '\0';
				break;
			}
		}
	}
	//cout << buf << endl;
	return buf;
}

Request::Request(string url, Json::Value headers, string cookies)
{
	WORD w_req = MAKEWORD(2, 2);
	if (WSAStartup(w_req, &wsadata) == 0) {

	}
	req_socket = socket(AF_INET, SOCK_STREAM, 0);

	int pos = url.find("https://") + 8;
	string host = url.substr(pos, url.find("/", pos) - pos);
	//cout << host << endl;
	//system("pause");

	ip = gethostbyname(host.c_str());
		sin.sin_family = AF_INET;
		sin.sin_port = htons(port);
		sin.sin_addr = *(in_addr*)ip->h_addr_list[0];

	SSLeay_add_ssl_algorithms();
	ctx = SSL_CTX_new(meth);
	ssl = SSL_new(ctx);
	SSL_set_fd(ssl, req_socket);
	SSL_CTX_set_verify(ctx, SSL_VERIFY_NONE, NULL);

	stringstream data;
	data << "GET " << url << " HTTP/1.1\r\n";
	data << "Host: " << host << "\r\n";
	if (headers != Json::nullValue) {
		Json::Reader reader;
		Json::Value::Members member = headers.getMemberNames();
		for (Json::Value::Members::iterator iter = member.begin(); iter != member.end(); ++iter)
		{
			data << (string)(*iter) << ": ";
			string s = headers[(string)(*iter)].toStyledString();
			s = replaceStr(s, "\"", "");
			s = replaceStr(s, "\r", "");
			s = replaceStr(s, "\n", "");
			data << s << "\r\n";
		}
	}
	if (cookies != "") {
		data << "cookie: " << cookies << "\r\n";
	}
	data << "\r\n";

	string s = data.str();
	//cout << s << endl;
	strcpy(sendData, s.c_str());
	sendLength = strlen(sendData);

	//cout << sendData << endl;
	//system("pause");
	connect(req_socket, (sockaddr*)&sin, sizeof(sin));
	SSL_connect(ssl);
}

string Request::replaceStr(string s, string old_str, string new_str) {
	string::size_type pos = 0;
	while ((pos = s.find(old_str)) != string::npos)
	{
		s.replace(pos, old_str.length(), new_str);
	}
	return s;
}

Request::~Request()
{
	SSL_shutdown(ssl);
	SSL_free(ssl);
	SSL_CTX_free(ctx);
	closesocket(req_socket);
	WSACleanup();
}
