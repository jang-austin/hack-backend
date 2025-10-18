# Hack Backend

보라색 버튼 확률 당첨 시 닉네임을 콘솔에 출력하는 스프링부트 서버입니다.

## 기능

- **보라색 버튼 확률 당첨 처리**: hack-library의 PurpleButton에서 5% 확률로 당첨 시 요청을 받아 닉네임을 콘솔에 출력
- **해킹 통계 추적**: 맨 처음과 마지막 당첨자 정보를 메모리에 저장하고 매 요청마다 출력
- **OpenTelemetry 모니터링**: Zipkin을 통한 분산 추적 지원
- **Spring Boot Actuator**: 메트릭 및 헬스체크 엔드포인트 제공

## API 엔드포인트

### POST /api/button-click

보라색 버튼 확률 당첨 시 호출되는 엔드포인트

**요청:**

```json
{
  "nickname": "사용자닉네임",
  "buttonType": "purple"
}
```

**응답:**

```
버튼 클릭 이벤트가 성공적으로 처리되었습니다.
```

**콘솔 출력:**

```
=== 보라색 버튼 확률 당첨! (hack-backend) ===
당첨자: 사용자닉네임
버튼 타입: purple
--- 해킹 통계 ---
맨 처음 당첨자: 첫번째당첨자
마지막 당첨자: 사용자닉네임
================================
```

### GET /api/health

서버 상태 확인

**응답:**

```
hack-backend 서버가 정상적으로 실행 중입니다.
```

## 실행 방법

### 로컬 개발

```bash
mvn spring-boot:run
```

### Docker (모니터링 포함)

```bash
# 모든 서버와 모니터링 시작
./start-all-with-monitoring.sh

# 모든 서버와 모니터링 중지
./stop-all-with-monitoring.sh
```

## 모니터링

- **Zipkin 분산 추적**: http://localhost:9411
- **Spring Boot Actuator**: http://localhost:8081/actuator
- **서버 포트**: 8081

## 기술 스택

- Java 17
- Spring Boot 3.2.0
- Maven
- OpenTelemetry
- Zipkin
- Spring Boot Actuator

## 프로젝트 구조

```
src/main/java/com/hack/
├── HackBackendApplication.java          # 메인 애플리케이션
└── controller/
    └── ButtonController.java           # API 컨트롤러

src/main/resources/
└── application.yml                     # 설정 파일
```

## 설정

### application.yml

```yaml
server:
  port: 8081

spring:
  application:
    name: hack-backend
  zipkin:
    base-url: http://localhost:9411
  sleuth:
    zipkin:
      base-url: http://localhost:9411

management:
  endpoints:
    web:
      exposure:
        include: "*"
  tracing:
    sampling:
      probability: 1.0
```

## 관련 프로젝트

- **hack-library**: 프론트엔드 라이브러리 (PurpleButton 포함)
- **hacked-system**: 데모 웹 애플리케이션
- **hacked-backend**: 일반 버튼 클릭 처리 서버
