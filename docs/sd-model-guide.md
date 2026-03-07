# Stable Diffusion 모델 다운로드 가이드

RTX 3050 6GB VRAM에 최적화된 SD 1.5 기반 모델 구성입니다.

## 디렉토리 구조

```
E:\sd-webui\models\
├── Stable-diffusion\    ← 체크포인트 모델 (.safetensors)
├── VAE\                 ← VAE 파일
├── Lora\                ← LoRA 파일
└── embeddings\          ← Textual Inversion 임베딩
```

## 1. 체크포인트 모델 (필수)

모델은 [Civitai](https://civitai.com/)에서 다운로드합니다.
다운로드 후 `E:\sd-webui\models\Stable-diffusion\`에 배치합니다.

### 애니메이션 스타일 추천 (게임 CG 용도)

| 모델명 | 특징 | 용량 |
|---|---|---|
| **AnyLoRA** | 범용 애니 스타일, LoRA 호환성 최고 | ~2GB |
| **Anything V5** | 고전적 애니 스타일, 안정적 | ~2GB |
| **MeinaMix** | 고퀄리티 애니, 디테일 우수 | ~2GB |
| **AbyssOrangeMix3** | NSFW 특화, 피부 표현 우수 | ~2GB |

> [!TIP]
> 처음엔 **AnyLoRA** 하나만 받아서 테스트하세요. 이후 스타일에 맞게 추가하면 됩니다.

## 2. VAE (필수)

VAE가 없으면 색감이 흐릿하게 나옵니다.

- **vae-ft-mse-840000-ema-pruned.safetensors** (Stability AI 공식)
- 다운로드: [HuggingFace](https://huggingface.co/stabilityai/sd-vae-ft-mse-original)
- 배치: `E:\sd-webui\models\VAE\`

WebUI 설정에서 `Settings > Stable Diffusion > SD VAE`를 다운받은 VAE로 변경

## 3. Negative Embedding (권장)

품질 저하 요소를 자동 제거해주는 임베딩입니다.

| 이름 | 용도 |
|---|---|
| **EasyNegative** | 범용 품질 향상 |
| **bad-hands-5** | 손 표현 개선 |
| **badquality** | 전반적 품질 향상 |

- Civitai에서 검색 후 다운로드
- 배치: `E:\sd-webui\embeddings\`
- Negative Prompt에 `EasyNegative, bad-hands-5` 추가하면 적용

## 4. LoRA (선택, 강력 추천)

캐릭터 일관성이나 특정 스타일을 적용하는 데 사용합니다.

- 배치: `E:\sd-webui\models\Lora\`
- 프롬프트에 `<lora:이름:가중치>` 형식으로 사용
- 예: `<lora:anime_style:0.7>`

> [!IMPORTANT]
> LoRA는 나중에 게임 캐릭터 스타일이 확정된 후에 특화된 것을 찾으면 됩니다. 처음엔 체크포인트 + VAE + Negative Embedding만으로 충분합니다.

## 첫 실행 순서

1. 위 모델들을 해당 폴더에 배치
2. `E:\sd-webui\webui-user.bat` 실행
3. 첫 실행 시 자동으로 의존성 설치 (10~20분 소요)
4. 브라우저에서 `http://127.0.0.1:7860` 접속
5. 좌측 상단에서 체크포인트 모델 선택
6. Settings > SD VAE에서 VAE 설정
