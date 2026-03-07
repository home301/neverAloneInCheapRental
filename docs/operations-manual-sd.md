# SD 이미지 생성 운영 매뉴얼 (SOP)

이 매뉴얼은 "싼 월세집은 나 혼자가 아니었다" 프로젝트의 아트 에셋을 생성하기 위한 표준 운영 절차를 다룹니다.

---

## 1. 실행 및 환경 설정

### 실행 환경 (Forge SD)
- **실행 경로**: `C:\sd-webui-forge\run.bat`
- **최적화 인수** (`webui-user.bat` 편집):
  ```bash
  set COMMANDLINE_ARGS=--api --no-half-vae --theme dark
  ```
  > [!NOTE]
  > Forge는 메모리를 자동 관리하므로 `--medvram`이나 `--xformers` 인수가 더 이상 필요하지 않습니다.

### 모델 구성 (Checkpoint)
- **권장 모델**: **DreamShaper 8** (실사~반실사), **AnyLoRA** (애니메이션 스타일)
- **VAE**: `vae-ft-mse-840000-ema-pruned` (색감 보정 필수)

---

## 2. 캐릭터 생성 가이드 (Prompt Sheet)

### A. 주인공 (히키코모리/모쏠)
주인공의 '평범하고 찌질한' 느낌을 유지하는 것이 핵심입니다.
- **핵심 키워드**: `1man, solo, short height, chubby, messy hair, glasses, plain t-shirt, hoodie, hikikomori, otaku, depressed expression`
- **Negative**: `handsome, muscular, tall, athletic, sharp jawline`

### B. 처녀귀신 (히로인)
단계별 외형 변화를 프롬프트로 제어합니다.

| 단계 | 프롬프트 키워드 | 분위기/외형 |
| :--- | :--- | :--- |
| **1. 악귀 상태** | `ghastly woman, hollow eyes, pale skin, wet long black hair, tattered white dress, no lower body, floating, scary, horror atmosphere` | 공포, 흉측함 |
| **2. 복원 중** | `semi-transparent woman, belly visible, recovering skin texture, long black hair, traditional white dress (sobok)` | 신비로움, 기묘함 |
| **3. 완전 복원** | `1girl, beautiful korean woman, long black hair, soft skin, white sobok, gentle smile, glowing eyes` | 청순, 아름다움 |

---

## 3. 배경 생성 가이드

### 싼 월세집 (좁고 어두움)
- **키워드**: `narrow studio apartment, cluttered room, old wallpaper, fluorescent light, computer desk (multiple monitors), trash bags, evening light through small window, dim lighting, messy bed`
- **호러 연출**: `creepy shadows, handprints on walls, flickering lights, dark corners`

---

## 4. 6GB VRAM 생존 워크플로우

### 1) 기초 생성 (txt2img)
- **크기**: 512x768 (세로형 캐릭터)
- **Sampling**: DPM++ 2M Karras, Steps 20~25
- **CFG Scale**: 7

### 2) 고화질화 (Hires. fix)
- **Upscaler**: `R-ESRGAN 4x+ Anime6B` 또는 `Latent`
- **Denoising strength**: 0.4~0.5 (너무 높으면 형태가 무너짐)
- **Upscale by**: **1.5x** (최종 768x1152)
  - *[!WARNING] 2.0x 시도 시 OOM(메모리 부족) 발생 가능성 높음.*

### 3) 리터칭 및 수정 (Inpaint)
- 손가락이 뭉쳐지거나 표정이 어색할 경우 `img2img > Inpaint` 사용
- **Denoising**: 0.5 전후로 설정하여 자연스럽게 합성

---

## 5. 결과물 관리
- 생성된 이미지는 `art/concepts/` 및 `art/characters/` 폴더로 이동하여 게임 기획과 연동합니다.
- 마음에 드는 시드(Seed) 번호는 따로 텍스트 파일로 메모해두는 것을 권장합니다.
