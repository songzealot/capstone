# AI를 활용한 네트워크 침입 탐지 시스템(미완성)
## 소개
NSL-KDD, CSE-CIC-IDS 2018의 데이터를 사용해 실시간 네트워크 패킷에서 Brute Force, DoS, DDoS, Probe 공격을 탐지하는 프로그램입니다.  
실시간 패킷을 NSL-KDD의 형태로 변환하는 코드는 C++로 만들어졌고 나머지 코드는 파이썬으로 제작되었습니다.  
프로젝트를 위한 프로그램이며, 실사용을 위해 제작된 프로그램이 아닙니다.  

## 이슈
완전히 개발된 프로그램이 아닙니다.
최적화가 되지 않았으므로 버그가 발생할 수 있습니다.  
모델의 정확도를 보장하지 않습니다.  

## 실행
```python main.py```

***
이 프로그램은 중부대학교 정보보호학과 Dogu 팀에 의해 제작되었습니다.  
  
김명섭(팀장): 기획, Brute Force 모델 제작  
박재희: DDoS 모델 제작  
송우영: 소프트웨어 개발  
신정훈: DoS 모델 제작  
천호범: Probe 모델 제작  

***

## 참고
[실시간 패킷 -> NSL-KDD 데이터](https://github.com/AI-IDS/kdd99_feature_extractor)  
[실시간 패킷 -> CSE-CIC-IDS 2018](https://github.com/datthinh1801/cicflowmeter)  
