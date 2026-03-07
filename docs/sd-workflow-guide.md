# Stable Diffusion 워크플로우 가이드

RTX 3050 6GB VRAM 최적화 워크플로우입니다.

## 기본 생성 설정

### txt2img (텍스트 → 이미지)

| 설정 | 권장값 | 이유 |
|---|---|---|
| **Width × Height** | 512 × 768 | 세로형 캐릭터 일러스트 기본 |
| **Sampling Method** | DPM++ 2M Karras | 속도/퀄리티 균형 최적 |
| **Sampling Steps** | 20~30 | 20이면 빠르고, 30이면 디테일↑ |
| **CFG Scale** | 7~8 | 프롬프트 반영 강도 |
| **Seed** | -1 (랜덤) | 마음에 드는 결과 나오면 시드 고정 |

### Hires Fix (업스케일)

6GB VRAM에서 512px 생성 후 업스케일하는 핵심 기능입니다.

| 설정 | 권장값 |
|---|---|
| **Upscaler** | R-ESRGAN 4x+ Anime6B |
| **Hires Steps** | 10~15 |
| **Denoising Strength** | 0.4~0.55 |
| **Upscale by** | 1.5~2x |

> [!WARNING]
> 6GB VRAM에서 2x 업스케일 시 768×1152까지 가능합니다. 그 이상은 OOM(메모리 부족) 발생 가능.

## 프롬프트 작성법

### 기본 구조

```
(품질 태그), (캐릭터 묘사), (포즈/동작), (배경/환경), (조명/분위기)
```

### 예시 프롬프트

**Positive:**
```
masterpiece, best quality, 1girl, black hair, long hair, brown eyes, 
school uniform, standing, looking at viewer, 
indoor, bedroom, evening light, soft lighting
```

**Negative:**
```
EasyNegative, bad-hands-5, lowres, bad anatomy, bad hands, 
text, error, missing fingers, extra digit, fewer digits, 
cropped, worst quality, low quality, jpeg artifacts
```

### 품질 향상 팁

- `masterpiece, best quality`를 항상 앞에 배치
- 괄호 `(tag:1.3)` 으로 가중치 조절 (1.0이 기본, 높을수록 강조)
- Negative에 `EasyNegative` 임베딩 필수

## img2img (이미지 → 이미지)

AI 초안을 수정하거나, 러프 스케치를 정리할 때 사용합니다.

| 설정 | 권장값 | 용도 |
|---|---|---|
| **Denoising Strength** | 0.3~0.5 | 낮을수록 원본 유지, 높을수록 변경 많음 |
| **Width × Height** | 원본과 동일 | 비율 유지 |

### 워크플로우

```
러프 스케치 → img2img (0.5~0.7) → 수정 → img2img (0.3~0.4) → 완성
```

## Inpaint (부분 수정)

이미지의 특정 부분만 다시 그리는 기능입니다.

1. img2img 탭 → Inpaint 선택
2. 수정할 부분을 브러시로 마스킹
3. 해당 영역에 대한 프롬프트 입력
4. Denoising 0.5~0.7 권장

> [!TIP]
> 캐릭터 표정만 바꾸거나, 의상 일부를 수정할 때 매우 유용합니다.

## ControlNet (포즈 제어)

캐릭터 포즈를 정확하게 제어하는 확장 기능입니다.
A1111 설치 후 별도 확장 설치가 필요합니다.

### 설치 방법
1. WebUI → Extensions → Install from URL
2. URL: `https://github.com/Mikubill/sd-webui-controlnet`
3. Apply and restart UI
4. ControlNet 모델 다운로드 (OpenPose, Canny 등)

### 주요 프리프로세서

| 프리프로세서 | 용도 |
|---|---|
| **OpenPose** | 포즈 (전신/얼굴/손) 제어 |
| **Canny** | 선화 기반 제어 |
| **Depth** | 깊이감/구도 제어 |

## VRAM 절약 팁

1. **배치 사이즈는 항상 1** — 2 이상은 OOM 위험
2. **--medvram 플래그** — 이미 설정됨 (webui-user.bat)
3. **Hires Fix는 1.5x까지** — 2x 이상 주의
4. **생성 중 다른 GPU 작업 자제** — 브라우저 하드웨어 가속 끄기 권장
5. **VAE로 디코딩 중 OOM 시** — `--no-half-vae` 이미 설정됨
