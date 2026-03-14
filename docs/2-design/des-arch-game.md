# Architecture: 싼 월세집은 나 혼자가 아니었다 (생존 & DLC 분리)

## 1. 개요 (Architecture Overview)

*   **게임 엔진**: **Unity (C#)**
    *   **선정 사유**: 밀실 환경(원룸) 구성 시 3D 배경과 2D 캐릭터(스프라이트/Spine) 혹은 3D 캐릭터 모델 모델링 혼합에 가장 최적화되어 있습니다. 또한 다양한 에셋 스토어를 통한 저비용 고효율 인디 개발, 강력한 UI/Canvas 시스템(스마트폰 메뉴, HUD 등), 그리고 추후 DLC 분리 배포(Addressables 활용)에 매우 유리합니다.
*   **아키텍처 패턴**: MVC (Model-View-Controller) 변형 (또는 MVP)
    *   생존 시뮬레이션의 특성상(다양한 스탯과 시간이 맞물려 돌아감) 상태(Model)와 화면(View)을 분리하는 구조가 필수적입니다.
*   **세이브 시스템**: JSON 기반 직렬화 (생존 일수, 스탯 파라미터 보존)
*   **데이터 흐름**: Data Model(스탯, 경제, 일차) ↔ Event/Survival Controller(생존 일수, 수익 계산) ↔ UI Manager(인터페이스, 상태바)

## 2. 모듈 구성도 (Module Composition)

*   `CoreManager`: 일자(Time), 전역 State(체력, 양기, 체력/양기 MaxCap, 소지금, 직장 상태) 관리. 핵심 생존 루프 중심.
*   `GhostController`:
    *   **Base**: 매일 밤 랜덤한 위협으로 양기/체력을 탈취하고 공포도를 상승시키는 적대적 AI.
    *   **DLC 확장**: 성욕/호감도 스테이트가 활성화되며, 특정 조건 만족 시 유혹 이벤트 트리거.
*   `EconomySystem`: 출근/알바 처리, 급여 지급, 인터넷 쇼핑(배달 음식) 구매 판정.
*   `ScenarioDirector`: DLC 여부에 따라 4막 시나리오 진행을 활성화하거나, Base의 생존 페널티(과로, 강등, 데스)를 관장.
*   `DLCManager`: 런타임 시 성인용 모듈(에셋, 추가 스크립트) 로드 여부를 체크하고 게임 내 기능(VR 구매)을 플래그로 켜고 끄는 관리자.

## 2.1. 공통 모듈 종속성 (Project Charlie Shared Modules)
상위 디렉토리에 구축된 `projectCharlie`의 검증된 Unity 패키지들을 하위 시스템으로 가져와 게임의 뼈대로 사용합니다.
*   `com.projectcharlie.save`: JSON/바이너리 직렬화 기반의 게임 진행도 및 스탯 세이브/로드 기능.
*   `com.projectcharlie.settings`: 해상도, 오디오 볼륨 등 환경 설정 시스템.
*   `com.projectcharlie.mission`: 튜토리얼 퀘스트나 생존 일수 달성 등 목표 트리거 및 보상 시스템.
*   `com.projectcharlie.audio` / `localization` 등 기구축된 코어 유틸리티 적극 활용.

## 3. 핵심 상태 (Core States)

*   `PlayerState`:
    *   `Stamina`: 현재 체력 / 최대 체력 (음수 허용, 데스 체크, 양질 식사 버프 계수)
    *   `Vitality`: 현재 양기 / 최대 양기 (0 이하 시 디버프 상태 전환)
    *   `Sanity`: 현재 정신력 / 최대 정신력 (운동 지속시간 버프 계수)
    *   `FiberLevel`: 체내 식이섬유 축적량 (0이 되면 질병 상태 돌입)
    *   `Money`: 소지금
    *   `JobStatus`: `PROBATION` (수습), `PART_TIME` (알바), `FIRED` (해고)
    *   `HasDisease`: `bool` (식이섬유 부족 시 True, 체력 소모 1.5배 디버프)
*   `GhostState` (Base): `Aggression` (공격성, 밤마다 빼앗는 양기량 결정)
*   `GhostState` (DLC Only): 
    *   `Affection` (친근감, 상호작용 성공 허들 척도)
    *   `Lust` (성욕, 0이 해소된 상태, 증가할수록 성적 갈증 심화)
    *   `Maternity` (모성애, 0이 해소된 상태, 증가할수록 집착 심화)
    *   `Grudge` (원한, 성욕/모성애 방치 시 증가하는 최종 공격성 척도)
*   `GameState`:
    *   `CurrentDay`: 생존 일수 (Score)
    *   `DLCEnalbed`: Boolean 플래그

## 4. 데이터 플로우 (Data Flow)

1. 플레이어가 행동 액션 (예: `TakeAction: "Exercise"`) 클릭
2. `EconomySystem` 혹은 `CoreManager`가 비용 처리 (체력 대폭 감소, 양기 감소, 양기 MaxCap 증가)
3. 밤(Night Phase) 진입 시 `GhostController`가 공격 배수에 맞춰 플레이어의 양기 탈취
4. `ScenarioDirector` 상태 체크: 체력 0 도달 시 다음 날 결근 처리 -> `JobStatus` 변동
5. `ScenarioDirector` 상태 체크 2: 양기 0 도달 시 데스 이벤트 호출, `CurrentDay`를 최종 스코어로 리포트
6. **(Base)** 보름달 타이머 도달 시 `GhostController`가 특수 배수(발정기)로 체력과 양기를 대폭 차감. 화면 등 간접 묘사만 출력.
7. **(DLC)** DLC 활성화 상태일 경우, Base 플로우 사이에 컷신/성인 이벤트 분기 로직(성교) 병합
