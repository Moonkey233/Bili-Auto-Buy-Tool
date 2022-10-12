#ifndef _TOOLS_H_
#define _TOOLS_H_
#include <windows.h>
#include <string>
#include <ctime>
#include <iostream>

class Tools
{
public:
	static int SetColorAndBackground(int ForgC, int BackC);
	static int encodeToUTF8(char* text);
	static std::string replaceStrAll(std::string s, std::string old_str, std::string new_str);
	static int setSysTime(long long time);
	static bool isAdmin();
	static std::string findValue(char* buf, std::string start, std::string end);
	static long long standardToStamp(char* standardTime);
	static std::string stampTostandard(long long timeStamp);
	static int errorPause(std::string msg);
	static std::string uuid(unsigned int len = 32);
	static std::string intToHex(long long i);
};

#endif  // !_TOOLS_H_
