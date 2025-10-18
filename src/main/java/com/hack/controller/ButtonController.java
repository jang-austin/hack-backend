package com.hack.controller;

import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.Map;
import java.util.concurrent.atomic.AtomicReference;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class ButtonController {

    private static final Logger logger = LoggerFactory.getLogger(ButtonController.class);

    // 맨 처음과 마지막 사람을 저장하는 변수들
    private static final AtomicReference<String> firstPerson = new AtomicReference<>(null);
    private static final AtomicReference<String> lastPerson = new AtomicReference<>(null);

    @PostMapping("/button-click")
    public ResponseEntity<String> handleButtonClick(@RequestBody Map<String, Object> request) {
        try {
            // 요청에서 닉네임 추출
            String nickname = (String) request.get("nickname");
            String buttonType = (String) request.get("buttonType");
            
            if (nickname != null) {
                // 맨 처음 사람 설정 (한 번만 설정됨)
                firstPerson.compareAndSet(null, nickname);
                
                // 마지막 사람 업데이트 (항상 업데이트됨)
                lastPerson.set(nickname);
                
                logger.info("=== 보라색 버튼 확률 당첨! (hack-backend) ===");
                logger.info("당첨자: {}", nickname);
                if (buttonType != null) {
                    logger.info("버튼 타입: {}", buttonType);
                }
                
                // 맨 처음과 마지막 사람 정보 출력
                logger.info("--- 해킹 통계 ---");
                logger.info("맨 처음 당첨자: {}", firstPerson.get() != null ? firstPerson.get() : "아직 없음");
                logger.info("마지막 당첨자: {}", lastPerson.get() != null ? lastPerson.get() : "아직 없음");
                logger.info("================================");
                
                return ResponseEntity.ok("버튼 클릭 이벤트가 성공적으로 처리되었습니다.");
            } else {
                logger.warn("닉네임이 제공되지 않았습니다.");
                return ResponseEntity.badRequest().body("닉네임이 필요합니다.");
            }
        } catch (Exception e) {
            logger.error("버튼 클릭 처리 중 오류 발생: {}", e.getMessage(), e);
            return ResponseEntity.internalServerError().body("서버 오류가 발생했습니다.");
        }
    }
    
    @GetMapping("/health")
    public ResponseEntity<String> health() {
        return ResponseEntity.ok("hack-backend 서버가 정상적으로 실행 중입니다.");
    }
}
