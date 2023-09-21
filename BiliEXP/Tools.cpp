#include "Tools.h"

int Tools::SetColorAndBackground(int ForgC, int BackC) {
	try {
		WORD wColor = ((BackC & 0x0F) << 4) + (ForgC & 0x0F);
		SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), wColor);
		return 0;
	}
	catch (...) {
		errorPause("setcolor error");
		return -1;
	}
}

int Tools::encodeToUTF8(char* text) {
	try {
		TCHAR wscBuffer[4097]{ 0 };
		int recLen = strlen(text);
		MultiByteToWideChar(CP_UTF8, 0, text, recLen + 1, wscBuffer, sizeof(wscBuffer) / sizeof(wchar_t));
		memset(text, 0, recLen);
		WideCharToMultiByte(CP_ACP, 0, wscBuffer, -1, text, recLen, NULL, NULL);
		return 0;
	}
	catch (...) {
		errorPause("UTF8 encode error");
		return -1;
	}
}

std::string Tools::replaceStrAll(std::string s, std::string old_str, std::string new_str) {
	try {
		std::string::size_type pos = 0;
		while ((pos = s.find(old_str)) != std::string::npos) {
			s.replace(pos, old_str.length(), new_str);
		}
		return s;
	}
	catch (...) {
		errorPause("replaceStr error");
		return "";
	}
}

int Tools::setSysTime(long long time) {
	try {
		time_t tick = (time_t)time / 1000;
		struct tm tm;
		localtime_s(&tm, &tick);
		SYSTEMTIME myTime{};
		myTime.wYear = tm.tm_year + 1900;
		myTime.wMonth = tm.tm_mon + 1;
		myTime.wDay = tm.tm_mday;
		myTime.wHour = tm.tm_hour;
		myTime.wMinute = tm.tm_min;
		myTime.wSecond = tm.tm_sec;
		myTime.wMilliseconds = time % 1000;
		SetLocalTime(&myTime);
		return 0;
	}
	catch (...) {
		errorPause("setSysTime error");
		return -1;
	}
}

bool Tools::isAdmin() {
	BOOL b;
	SID_IDENTIFIER_AUTHORITY NtAuthority = SECURITY_NT_AUTHORITY;
	PSID AdministratorsGroup;
	b = AllocateAndInitializeSid(&NtAuthority, 2, SECURITY_BUILTIN_DOMAIN_RID, DOMAIN_ALIAS_RID_ADMINS, 0, 0, 0, 0, 0, 0, &AdministratorsGroup);
	if (b)
	{
		if (!CheckTokenMembership(NULL, AdministratorsGroup, &b))
		{
			b = FALSE;
		}
		FreeSid(AdministratorsGroup);
	}
	return b;
}

std::string Tools::findValue(char* buf, std::string start, std::string end) {
	try {
		std::string s = buf;
		int pos = s.find(start);
		if (pos != -1) {
			int length = start.length();
			if (end == "NULL") {
				return s.substr(pos + length);
			}
			else {
				return s.substr(pos + length, s.find(end, pos + length) - pos - length);
			}
		}
		return "";
	}
	catch (...) {
		errorPause("findValue error");
		return "";
	}
}

long long Tools::standardToStamp(char* standardTime) {
	try {
		struct tm stm;
		int iY, iM, iD, iH, iMin, iS;
		memset(&stm, 0, sizeof(stm));
		iY = atoi(standardTime);
		iM = atoi(standardTime + 5);
		iD = atoi(standardTime + 8);
		iH = atoi(standardTime + 11);
		iMin = atoi(standardTime + 14);
		iS = atoi(standardTime + 17);

		stm.tm_year = iY - 1900;
		stm.tm_mon = iM - 1;
		stm.tm_mday = iD;
		stm.tm_hour = iH;
		stm.tm_min = iMin;
		stm.tm_sec = iS;

		return (long long)mktime(&stm);
	}
	catch (...) {
		errorPause("stdToTmp error");
		return -1;
	}
}

std::string Tools::stampTostandard(long long timeStamp) {
	try {
		time_t tick = (time_t)timeStamp;
		struct tm tm;
		char s[40];
		localtime_s(&tm, &tick);
		strftime(s, sizeof(s), "%Y-%m-%d %H:%M:%S", &tm);
		std::string str(s);
		return str;
	}
	catch (...) {
		errorPause("tmpToStd error");
		return "";
	}
}

int Tools::errorPause(std::string msg) {
	Tools::SetColorAndBackground(4, 0);
	std::cout << msg << std::endl;
	//WSACleanup();
	system("pause");
	//exit(0);
	return 0;
}

std::string Tools::uuid(unsigned int len) {
	try {
		std::string uuidLib = "0123456789abcdef";
		std::string uuid = "";
		unsigned seed;
		seed = time(0);
		srand(seed);
		for (int i = 0; i < len; i++) {
			uuid += uuidLib[rand() % 16];
		}
		return uuid;
	}
	catch (...) {
		errorPause("UUID error");
		return "";
	}
}

std::string Tools::intToHex(long long i) {
	try {
		std::string hexLib = "0123456789abcdef";
		long long x;
		std::string s;
		while (i != 0) {
			x = i % 16;
			s = hexLib[x] + s;
			i = i / 16;
		}
		return s;
	}
	catch (...) {
		errorPause("intToHex error");
		return "";
	}
}