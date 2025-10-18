# Hack Backend - Render 배포 가이드

## 🚀 Render 배포 단계

### 1. Render 계정 생성
1. https://render.com 접속
2. GitHub 계정으로 로그인
3. "New +" → "Web Service" 클릭

### 2. GitHub 저장소 연결
1. "Build and deploy from a Git repository" 선택
2. "Connect account" → GitHub 계정 연결
3. `hack-backend` 저장소 선택
4. "Connect" 클릭

### 3. 서비스 설정
```
Name: hack-backend
Environment: Java
Region: Oregon (US West)
Branch: main
Root Directory: (비워두기)
```

### 4. 빌드 및 배포 설정
```
Build Command: mvn clean package -DskipTests
Start Command: java -jar target/hack-backend-1.0.0.jar
```

### 5. 환경변수 설정 (선택사항)
```
SPRING_PROFILES_ACTIVE=production
```

### 6. 배포
1. "Create Web Service" 클릭
2. 자동으로 빌드 및 배포 시작
3. 배포 완료 후 URL 확인

## 📊 배포 후 확인

### 헬스체크
```bash
curl https://hack-backend.onrender.com/api/health
```

### API 테스트
```bash
curl -X POST https://hack-backend.onrender.com/api/button-click \
  -H "Content-Type: application/json" \
  -d '{"nickname": "test", "buttonType": "purple"}'
```

## 🛌 Render 슬립 모드

### 슬립 조건
- **15분간 요청 없음** → 자동 슬립
- **첫 요청 시** → 자동 깨어남 (10-30초 소요)

### 슬립 모드 대응
1. **헬스체크 설정**: Render 대시보드에서 Health Check Path 설정
2. **외부 모니터링**: UptimeRobot 등으로 주기적 ping
3. **사용자 알림**: 첫 요청 시 로딩 시간 안내

## 🔧 Render 설정 최적화

### 1. 자동 배포 설정
- GitHub push 시 자동 배포 활성화
- 특정 브랜치만 배포 설정 가능

### 2. 환경변수 관리
- Render 대시보드에서 환경변수 설정
- 민감한 정보는 환경변수로 관리

### 3. 로그 확인
- Render 대시보드에서 실시간 로그 확인
- 에러 로그 및 성능 메트릭 제공

## 📈 모니터링

### Render 내장 모니터링
- **CPU/메모리 사용량**: 실시간 그래프
- **응답 시간**: 평균 응답 시간 추적
- **에러율**: 실패한 요청 비율
- **로그**: 실시간 로그 스트림

### 외부 모니터링 (선택사항)
- **UptimeRobot**: 무료 50개 모니터
- **Pingdom**: 웹사이트 모니터링
- **New Relic**: APM (유료)

## 🚨 주의사항

### 무료 티어 제한
- **월 750시간**: 슬립 시간 포함
- **슬립 모드**: 15분 무요청 시 슬립
- **콜드 스타트**: 첫 요청 시 10-30초 지연

### 성능 최적화
- **JVM 튜닝**: 메모리 설정 최적화
- **의존성 최적화**: 불필요한 라이브러리 제거
- **로깅 레벨**: 프로덕션에서 로그 레벨 조정

## 🔄 자동 배포

### GitHub 연동
1. Render에서 GitHub 저장소 연결
2. `main` 브랜치 push 시 자동 배포
3. 배포 상태는 Render 대시보드에서 확인

### 수동 배포
- Render 대시보드에서 "Manual Deploy" 클릭
- 특정 커밋으로 배포 가능

## 📝 배포 체크리스트

- [ ] GitHub 저장소 연결
- [ ] 빌드 명령어 설정
- [ ] 시작 명령어 설정
- [ ] 환경변수 설정
- [ ] 헬스체크 경로 설정
- [ ] 자동 배포 활성화
- [ ] 도메인 설정 (선택사항)
- [ ] SSL 인증서 확인
- [ ] API 테스트
- [ ] 모니터링 설정
