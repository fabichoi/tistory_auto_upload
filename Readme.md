# ~~티스토리~~ 블로그스팟(블로거) 자동 글 생성기

## 사용법

### [1] 관련 모듈 설치
python 3.8.2 가 설치되어 있다는 가정하에
```
pip install -r requirements.txt
```
를 입력하면 실행과 관련된 패키지가 설치된다. 

### [2] .env 파일 작성
.env 파일을 만들고 아래와 같은 내용을 입력해준다.
```
CLIENT_ID=클라이언트 정보의 Client ID (티스토리 API 문서 참조) 
REDIRECT_URI=사용자가 인증 후에 리디렉션할 URI (티스토리 API 문서 참조)
RESPONSE_TYPE=항상 'code'를 사용 (티스토리 API 문서 참조)
STATE=사이트간 요청 위조 공격을 보호하기 위한 임의의 고유한 문자열 (티스토리 API 문서 참조)
GRANT_TYPE=항상 'authorization_code'를 사용합니다 (티스토리 API 문서 참조)
CLIENT_SECRET=클라이언트 정보의 Secret Key (티스토리 API 문서 참조)
ACCESS_TOKEN=발급받은 Access Token (티스토리 API 문서 참조)
OUTPUT_TYPE=json
BLOG_NAME=티스토리 주소의 아이디 부분(https://xxx.tistory.com 에서 xxx)
```

### [3] 업로드 관련 설정 파일 수정(혹은 작성)
example.csv 파일을 수정한다. <br/>
Microsoft Excel을 이용해도 되고 다른 editor를 사용해도 상관없다. </br>
Microsoft Excel을 이용할 경우 저장할 때 반드시 example.csv와 동일한 format이어야 한다. </br>
Github Action을 사용하면서 csv의 사용법이 변경되었다.

### [4] 실행
```
python main.py example.csv
```
example.csv외 다른 파일로 가능하나<br/>
example.csv와 동일한 포맷으로 구성된 파일이어야 한다.

### 개발 로그
https://fabichoi.tistory.com/337 - 1일차 <br/>
https://fabichoi.tistory.com/341 - 2일차 <br/>
https://fabichoi.tistory.com/353 - 3일차 <br/>
https://fabichoi.tistory.com/363 - 4일차 <br/>

### 최근 변경 사항
티스토리가 제공하던 OpenAPI 서비스를 종료함에 따라
공부 습관을 유지하기 위해 블로그스팟(구글 블로거)으로 이동하기로 결정함.
이에 따라 자동 글 생성기의 소스도 수정 반영.