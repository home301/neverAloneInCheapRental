# Core Data Model Specification (Unity C#)

본 문서는 `req-game-scenario.md`의 기획 스펙을 바탕으로, Unity 엔진에서 구동될 핵심 데이터 모델(Model)과 매니저(Controller)의 C# 클래스 뼈대를 정의합니다. 'Project Charlie'의 공통 서브 모듈 연동을 고려하여 직렬화(Serialization) 친화적인 구조로 설계되었습니다.

---

## 1. 모델 아키텍처 (Model Architecture)

MVC 패턴에 따라 데이터(Model)는 순수하게 상태만 지니며, MonoBehaviour 구조에서 탈피하여 직렬화(`[Serializable]`) 기반의 순수 C# 클래스로 작성됩니다. 이를 통해 `com.projectcharlie.save` 모듈과 즉각적으로 연동할 수 있습니다.

### 1.1. PlayerState (주인공 상태)

주인공의 3대 생존 자원과 경제/사회적 지위를 담당하는 데이터 클래스입니다.

```csharp
[System.Serializable]
public class PlayerState
{
    // --- 3대 생존 스탯 ---
    public float currentStamina; // 현재 체력
    public float maxStamina;     // 최대 체력 (음수 판정으로 데스체크 수행)
    
    public float currentVitality; // 현재 양기
    public float maxVitality;     // 최대 양기 (운동을 통해 영구 상승)
    
    public float currentSanity;   // 현재 정신력 (0이 되면 빙의 자살 엔딩)
    public float maxSanity;

    // --- 9대 영양/기호식품 (Nutrition & Vices) 상태 ---
    // 필수 영양소 (Essential)
    public float currentCarbs;    // 탄수화물 (방치 시 다음 날 체력 회복 불가)
    public float currentProtein;  // 단백질 (방치 시 양기 최대치 감소)
    public float currentFat;      // 지방 (과다 시 비만 디버프 판정)
    
    // 미량 영양소 (Micro)
    public float currentMinerals; // 잔여 무기질 (비타민과 합산하여 정신력 회복률 결정)
    public float currentVitamins; // 잔여 비타민
    public float currentFiber;    // 식이섬유
    public bool hasDisease;       // 식이섬유 0 도달 장기화 시 소화불량/질병 (체력 소모 1.5배)

    // 기호식품 (Vices - 버프 & 치명적 리스크)
    public float sugarLevel;      // 당류 (단기 정신력 펌핑, 장기 비만 스택)
    public float caffeineLevel;   // 카페인 (체력 가불기, 다음 날 양기 떡락)
    public float nicotineLevel;   // 니코틴/알코올 복합 (단기 귀신 방어, 장기 Max 체력 영구 깎임)

    // --- 경제 및 사회 상태 ---
    public int money; // 소지금

    public enum JobType { PROBATION, PART_TIME, FIRED }
    public JobType currentJobStatus; // 현재 직장 상태 (초기: 수습사원)

    // --- 소유 아이템/플래그 ---
    public bool hasPurchasedGhostTracker; // 중고 폴라로이드/부적 등 귀신 스탯 관측 아이템 해금 여부
    
    // 생성자 초기화 로직 등
}
```

### 1.2. GhostState (귀신 상태 - Base & DLC 통합)

귀신의 공격성과 DLC 해금 시 드러나는 4대 감정 결핍 스탯을 보관합니다. 결핍 스탯은 Base 버전에서는 숨겨져 있거나 값이 고정/비활성화 상태로 처리됩니다.

```csharp
[System.Serializable]
public class GhostState
{
    // --- Base 스탯 ---
    public float aggression; // 기본 공격성 (밤마다 빼앗는 양기 기본 배수 결정)

    // --- DLC 4대 욕구/결핍 스탯 (해소 지향형: 0이 완벽히 해소된 상태) ---
    // 값이 오를수록(양수) 결핍/불만이 극에 달함을 의미합니다.
    public float affection; // 친근감 (유일하게 결핍이 아닌 호감 척도. 높아야 상호작용 가능)
    public float lust;      // 성욕 누적치 (성적 상호작용으로 해소)
    public float maternity; // 모성애 누적치 (아기 용품/수유 상호작용으로 해소)
    public float grudge;    // 원한 (성욕과 모성애가 방치되어 특정 임계치를 넘기면 상승. 치명적 페널티 스탯)
}
```

### 1.3. GameState (게임 전역 상태)

진행 일수와 같은 시스템 전역 데이터를 보관합니다. **세이브 파일(SaveData)의 루트 객체** 역할을 합니다.

```csharp
[System.Serializable]
public class GameState
{
    public int currentDay; // 생존 일수 (Score)
    public bool isDlcEnabled; // DLC 런타임 활성화 플래그

    // 모델 의존성 포함
    public PlayerState player;
    public GhostState ghost;

    public GameState()
    {
        player = new PlayerState();
        ghost = new GhostState();
    }
}
```

---

## 2. 매니저 시스템 (Controller Architecture)

`GameState` 데이터를 갱신하고 게임의 룰을 강제하는 코어 싱글톤/매니저들입니다.

### 2.1. CoreManager (게임 루프 제어)

하루(Day)의 흐름과 턴 제어를 관장합니다. 사용자가 '수면'을 취하거나 액션을 다 써서 밤으로 넘어가는 트랜지션을 처리합니다.

*   `void PassTimeToNight()`: 밤으로 전환.
*   `void EvaluateNightEvents()`: 밤 사이 발생하는 귀신 공격(GhostController), 보름달 이벤트, 수면 중 체력/양기 회복 등을 연산.
*   `void StartNextDay()`: 연산 결과를 바탕으로 아침을 맞이함. 생존 체크(사망 이벤트 팝업) 수행.

### 2.2. Event/Survival Director

데이터를 모니터링하다가 특정 조건이 만족되면 엔딩 플래그나 미션을 트리거합니다. `com.projectcharlie.mission` 모듈과 연동하여 콜백을 발송합니다.

*   조건 1: `PlayerState.currentSanity <= 0` ➡️ 자살 배드 엔딩 트리거
*   조건 2: `PlayerState.currentCurrentVitality <= 0` ➡️ 빙의/자연사 트리거
*   조건 3: `GhostState.grudge > OVERLOAD_LIMIT` ➡️ 원한 폭발 강제 페널티 이벤트 트리거

---

## 3. Project Charlie 공통 모듈 연동 계획

### 3.1. Save/Load (`com.projectcharlie.save`)
*   `GameState` 객체를 JSON으로 통째로 직렬화하여 로컬 디스크 스토리지에 저장 및 로드.
*   하루가 끝날 때(`StartNextDay()`) Auto-Save를 호출하여 억까/세이브-로드 반복 꼼수 방지 가능성을 열어둡니다.

### 3.2. Settings (`com.projectcharlie.settings`)
*   BGM, SFX 볼륨, 해상도 조절용 UI 연결. 
*   호러 게임 특성상 심박수 사운드, 귀신 숨소리 등 오디오 채널 분리(Audio Mixer)가 필수적이므로 세팅 모듈과 깊게 연관됩니다.

### 3.3. Mission/Tutorial (`com.projectcharlie.mission`)
*   최초 1일차 튜토리얼 (출근, 식사, 수면 튜토리얼)
*   10일 생존 돌파, 첫 보름달 생존, 첫 관측 아이템 획득 등의 플레이어 마일스톤 관리.
