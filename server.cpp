#include<winsock2.h>                        //����ͷ�ļ�  
#include<stdio.h>  
#include<windows.h>  
#pragma comment(lib,"WS2_32.lib")           //��ʽ�����׽��ֿ�  

int main()                                  //��������ʼ  
{
    WSADATA data;                           //����WSADATA�ṹ�����  
    WORD w = MAKEWORD(2, 0);                   //����汾����  
    char sztext[] = "��ӭ��\r\n";                //���岢��ʼ�����͵��ͻ��˵��ַ�����  
    ::WSAStartup(w, &data);                  //��ʼ���׽��ֿ�  
    SOCKET s, s1;                            //���������׽��ֺ������շ��׽��־��  
    s = ::socket(AF_INET, SOCK_STREAM, 0);      //����TCP�׽���  
    sockaddr_in addr, addr2;                 //�����׽��ֵ�ַ�ṹ  
    int n = sizeof(addr2);                    //��ȡ�׽��ֵ�ַ�ṹ��С  
    addr.sin_family = AF_INET;                //��ʼ����ַ�ṹ  
    addr.sin_port = htons(75);
    addr.sin_addr.S_un.S_addr = INADDR_ANY;
    ::bind(s, (sockaddr*)&addr, sizeof(addr));    //���׽���  
    ::listen(s, 5);                              //�����׽���  
    printf("�������Ѿ�����\r\n");              //�����ʾ��Ϣ  

    while (true)
    {
        s1 = ::accept(s, (sockaddr*)&addr2, &n);    //������������  
        if (s1 != NULL)
        {
            printf("%s�Ѿ�������\r\n", inet_ntoa(addr2.sin_addr));
            ::send(s1, sztext, sizeof(sztext), 0); //��ͻ��˷����ַ�����  
        }
        ::closesocket(s);                       //�ر��׽��־��  
        ::closesocket(s1);
        ::WSACleanup();                         //�ͷ��׽��ֿ�  
        if (getchar())                           //��������룬��رճ���  
        {
            return 0;                           //������������  
        }
        else
        {
            ::Sleep(100);                       //Ӧ��˯��0.1��  
        }
    }
}