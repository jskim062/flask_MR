# 베이스 이미지 지정 (Python 3.9)  
FROM python:3.10
  
# 작업 디렉토리 생성 및 이동   
  
# 필요 파일 복사  
COPY . ./

  
# 필요한 패키지 설치  
RUN pip install --no-cache-dir -r requirements.txt  