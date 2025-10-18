# Hack Backend 배포 가이드

## 🚀 Railway 배포 (추천)

### 1. Railway 계정 생성
1. https://railway.app 접속
2. GitHub 계정으로 로그인
3. "New Project" 클릭

### 2. 프로젝트 배포
1. "Deploy from GitHub repo" 선택
2. `hack-backend` 저장소 선택
3. "Deploy" 클릭

### 3. 환경변수 설정 (선택사항)
Railway 대시보드에서 다음 환경변수 설정:
```
SPRING_PROFILES_ACTIVE=production
ZIPKIN_BASE_URL=https://your-zipkin-url.com
```

### 4. 도메인 설정
- Railway에서 자동으로 `https://hack-backend-production.up.railway.app` 형태의 URL 제공
- 커스텀 도메인도 설정 가능

## 🐳 Docker 로컬 테스트

```bash
# Docker 이미지 빌드
docker build -t hack-backend .

# 로컬에서 실행
docker run -p 8080:8080 hack-backend

# 헬스체크
curl http://localhost:8080/api/health
```

## 📊 모니터링 설정

### Zipkin (선택사항)
프로덕션에서 Zipkin을 사용하려면:
1. 별도의 Zipkin 서버 배포 (Railway, Render 등)
2. 환경변수로 `ZIPKIN_BASE_URL` 설정

### Railway 내장 모니터링
- Railway 대시보드에서 CPU, 메모리, 네트워크 사용량 확인
- 로그 실시간 확인
- 메트릭 그래프 제공

## 🔧 다른 배포 옵션

### Render
1. https://render.com 접속
2. "New Web Service" 선택
3. GitHub 저장소 연결
4. Build Command: `mvn clean package -DskipTests`
5. Start Command: `java -jar target/hack-backend-1.0.0.jar`

### Fly.io
1. `flyctl` 설치
2. `flyctl launch` 실행
3. `flyctl deploy` 실행

## 📝 배포 후 확인사항

1. **헬스체크**: `https://your-app-url.com/api/health`
2. **API 테스트**: 
   ```bash
   curl -X POST https://your-app-url.com/api/button-click \
     -H "Content-Type: application/json" \
     -d '{"nickname": "test", "buttonType": "purple"}'
   ```
3. **로그 확인**: Railway/Render 대시보드에서 실시간 로그 확인

## 🚨 주의사항

- **무료 티어 제한**: Railway는 월 $5 크레딧 제공
- **슬립 모드**: 일정 시간 비활성 시 슬립 모드 진입 (첫 요청 시 깨어남)
- **환경변수**: 민감한 정보는 환경변수로 관리
- **로그**: 프로덕션에서는 로그 레벨 조정 권장

## 🔄 자동 배포

GitHub에 push할 때마다 자동으로 배포되도록 설정:
1. Railway/Render에서 GitHub 연동
2. `main` 브랜치 push 시 자동 배포 활성화
3. 배포 상태는 GitHub Actions나 서비스 대시보드에서 확인
