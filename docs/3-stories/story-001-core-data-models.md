# Story 001: Core Data Models (PlayerState, GhostState, GameState)

**Epic**: Architecture Foundation
**Priority**: Highest
**Status**: To Do
**Assignee**: Dev / Solo-Dev Agent

## 1. 개요 (Overview)
기획 스펙(`req-game-scenario.md`)과 모델 설계서(`des-data-model.md`)에 정의된 핵심 3대 데이터 모델을 순수 C# `[System.Serializable]` 클래스로 구현합니다. 이 모델들은 `com.projectcharlie.save`를 통해 JSON 파일로 직렬화되어야 합니다.

## 2. 작업 내역 (Tasks)

1. **`PlayerState.cs` 구현**:
   - 3대 생존 스탯 (Stamina, Vitality, Sanity)의 `current~` 및 `max~` 멤버 변수 선언.
   - 9대 영양/기호 스탯 (Carbs, Protein, Fat, Minerals, Vitamins, Fiber, Sugar, Caffeine, Nicotine) 변수 선언.
   - 경제/건강 스탯 (`money`, `hasDisease`, `currentJobStatus` enum 등) 구현.
2. **`GhostState.cs` 구현**:
   - Base용 `aggression` 스탯 및 DLC용 4대 해소 지향 스탯(`affection`, `lust`, `maternity`, `grudge`) 선언.
3. **`GameState.cs` 구현**:
   - 일차(`currentDay`), DLC 플래그(`isDlcEnabled`) 멤버 변수 선언.
   - 맴버 변수로 `PlayerState player`와 `GhostState ghost`를 인스턴스화하여 포함.

## 3. 합격 기준 (Acceptance Criteria, AC)

- [ ] 세 클래스 모두 Unity의 `[System.Serializable]` 속성이 정확히 붙어 있어야 한다.
- [ ] `GameState` 객체를 인스턴스화했을 때, 내부에 `PlayerState`와 `GhostState`가 Null 처리가 되지 않고 정상 할당되어야 한다.
- [ ] MonoBehaviour를 상속받지 않은 (상태 데이터만 담는) 순수 클래스로 설계되어야 한다.
- [ ] 스크립트는 `DevProject/Assets/Scripts/Models/` 경로에 저장되어야 한다.

## 4. 로컬 참고 문서 (References)
* [Data Model Specs](file:///d:/work_home/neverAloneInCheapRental/docs/2-design/des-data-model.md)
* [PRD Scenario](file:///d:/work_home/neverAloneInCheapRental/docs/1-requirements/req-game-scenario.md)
