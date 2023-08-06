from candinfo import Candidate

data = candinfo.Candidate(key='')
print(data.checkKey(),data.findCandidate(20220309,1),data.candiCount(20220309,1))
print(data.serverStatus(20220309,1))
# print(data1.jobCode(20200415),data1.eduCode(20200415),data1.sgCode(),data.gusigunCode(20200415,'서울특별시'),data.sggCode(20200415,2),data.partyCode(20200415))
