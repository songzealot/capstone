
class trans:
    def __init__(self, df):
        self.df = df
        self.protocol_type()
        self.service()
        self.flag()
        
    def protocol_type(self):
        df_list = self.df['protocol_type']
        trans_list = []
        for data in df_list:
            if(data=='icmp'):
                trans_list.append(0)
            elif(data=='tcp'):
                trans_list.append(1)
            elif(data=='udp'):
                trans_list.append(2)
            else:
                trans_list.append(3)
        self.df['protocol_type'] = trans_list
        
    def service(self):
        df_list = self.df['service']
        trans_list = []
        for data in df_list:
            if(data=='IRC'):
                trans_list.append(0)
            elif(data=='X11'):
                trans_list.append(1)
            elif(data=='Z39_50'):
                trans_list.append(2)
            elif(data=='aol'):
                trans_list.append(3)
            elif(data=='auth'):
                trans_list.append(4)
            elif(data=='bgp'):
                trans_list.append(5)
            elif(data=='courier'):
                trans_list.append(6)
            elif(data=='csnet_ns'):
                trans_list.append(7)
            elif(data=='ctf'):
                trans_list.append(8)
            elif(data=='daytime'):
                trans_list.append(9)
            elif(data=='discard'):
                trans_list.append(10)
            elif(data=='domain'):
                trans_list.append(11)
            elif(data=='domain_u'):
                trans_list.append(12)
            elif(data=='echo'):
                trans_list.append(13)
            elif(data=='eco_i'):
                trans_list.append(14)
            elif(data=='ecr_i'):
                trans_list.append(15)
            elif(data=='efs'):
                trans_list.append(16)
            elif(data=='exec'):
                trans_list.append(17)
            elif(data=='finger'):
                trans_list.append(18)
            elif(data=='ftp'):
                trans_list.append(19)
            elif(data=='ftp_data'):
                trans_list.append(20)
            elif(data=='gopher'):
                trans_list.append(21)
            elif(data=='harvest'):
                trans_list.append(22)
            elif(data=='hostnames'):
                trans_list.append(23)
            elif(data=='http'):
                trans_list.append(24)
            elif(data=='http_2784'):
                trans_list.append(25)
            elif(data=='http_443'):
                trans_list.append(26)
            elif(data=='http_8001'):
                trans_list.append(27)
            elif(data=='imap4'):
                trans_list.append(28)
            elif(data=='iso_tsap'):
                trans_list.append(29)
            elif(data=='klogin'):
                trans_list.append(30)
            elif(data=='kshell'):
                trans_list.append(31)
            elif(data=='ldap'):
                trans_list.append(32)
            elif(data=='link'):
                trans_list.append(33)
            elif(data=='login'):
                trans_list.append(34)
            elif(data=='mtp'):
                trans_list.append(35)
            elif(data=='name'):
                trans_list.append(36)
            elif(data=='netbios_dgm'):
                trans_list.append(37)
            elif(data=='netbios_ns'):
                trans_list.append(38)
            elif(data=='netbios_ssn'):
                trans_list.append(39)
            elif(data=='netstat'):
                trans_list.append(40)
            elif(data=='nnsp'):
                trans_list.append(41)
            elif(data=='nntp'):
                trans_list.append(42)
            elif(data=='ntp_u'):
                trans_list.append(43)
            elif(data=='other'):
                trans_list.append(44)
            elif(data=='pm_dump'):
                trans_list.append(45)
            elif(data=='pop_2'):
                trans_list.append(46)
            elif(data=='pop_3'):
                trans_list.append(47)
            elif(data=='printer'):
                trans_list.append(48)
            elif(data=='private'):
                trans_list.append(49)
            elif(data=='remote_job'):
                trans_list.append(50)
            elif(data=='rje'):
                trans_list.append(51)
            elif(data=='shell'):
                trans_list.append(52)
            elif(data=='smtp'):
                trans_list.append(53)
            elif(data=='sql_net'):
                trans_list.append(54)
            elif(data=='ssh'):
                trans_list.append(55)
            elif(data=='sunrpc'):
                trans_list.append(56)
            elif(data=='supdup'):
                trans_list.append(57)
            elif(data=='systat'):
                trans_list.append(58)
            elif(data=='telnet'):
                trans_list.append(59)
            elif(data=='tim_i'):
                trans_list.append(60)
            elif(data=='time'):
                trans_list.append(61)
            elif(data=='urp_i'):
                trans_list.append(62)
            elif(data=='uucp'):
                trans_list.append(63)
            elif(data=='uucp_path'):
                trans_list.append(64)
            elif(data=='vmnet'):
                trans_list.append(65)
            elif(data=='whois'):
                trans_list.append(66)
            else:
                trans_list.append(0)
        self.df['service'] = trans_list
        
    def flag(self):
        df_list = self.df['flag']
        trans_list = []
        for data in df_list:
            if(data=='OTH'):
                trans_list.append(0)
            elif(data=='REJ'):
                trans_list.append(1)
            elif(data=='RSTO'):
                trans_list.append(2)
            elif(data=='RSTOS0'):
                trans_list.append(3)
            elif(data=='RSTR'):
                trans_list.append(4)
            elif(data=='S0'):
                trans_list.append(5)
            elif(data=='S1'):
                trans_list.append(6)
            elif(data=='S2'):
                trans_list.append(7)
            elif(data=='S3'):
                trans_list.append(8)
            elif(data=='SF'):
                trans_list.append(9)
            elif(data=='SH'):
                trans_list.append(10)
        self.df['flag'] = trans_list
        