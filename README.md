# Movie_review_analysis


## 프로젝트 개요
> 사용자가 영화를 선택하는 과정에 도움을 주기 위한 API 개발<br>
> **개발기간 2023.04 ~ 2023.05**


## API 기능 소개
> - 영화 기본 정보(출연진, 줄거리 등)
> - 평점, 긍/부정별 리뷰에 대한 테이블 뷰, 워드클라우드 제공
> 
## Stacks 🐈

### 스크래핑
<img src="https://img.shields.io/badge/selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white">

### 긍/부정 모델
<img src="https://img.shields.io/badge/pytorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white"><img src="https://img.shields.io/badge/pytorchlightning-792EE5?style=for-the-badge&logo=pytorchlightning&logoColor=white">

### 시각화 및 API
<img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=Plotly&logoColor=white">


## API 화면
| 영화 기본정보  |  평점, 긍/부정별 리뷰 빈도수 시각화  |
| :-------------------------------------------: | :------------: |
|  <img width="1194" alt="스크린샷 2023-05-15 오후 4 08 36" src="https://github.com/in-sukim/Naver_review_analysis/assets/43094223/1f73f836-4c68-4058-b321-cc5bffe2d23b"> |  <img width="676" alt="스크린샷 2023-05-15 오후 4 08 56" src="https://github.com/in-sukim/Naver_review_analysis/assets/43094223/bffd527b-2add-4b16-9701-13720eb29f91">|  
| 평점 별 리뷰에 대한 테이블 뷰, 워드클라우드  |  긍/부정 별 리뷰에 대한 테이블 뷰, 워드클라우드   |  
| <img width="1309" alt="스크린샷 2023-05-15 오후 4 10 12" src="https://github.com/in-sukim/Naver_review_analysis/assets/43094223/f819456f-dd2e-4c36-9f26-a87869321af3">   |  <img width="1223" alt="스크린샷 2023-05-15 오후 4 10 31" src="https://github.com/in-sukim/Naver_review_analysis/assets/43094223/5aa31693-bc94-40e7-a4b2-4adef0594ad2">     |

---

## 디렉토리 구조
```bash
├── README.md
├── app.py
├── modules : 
│   ├── info_prepare : 영화 기본정보 스크래핑.
│   ├── review_prepare : 영화 리뷰 스크래핑.
│   ├── sentiment_model.py: 긍/부정 모델 추론과정.
│   ├── sentiment_model_config.json: 긍/부정 모델 config.
│   ├── nsmc_clf_ver1.pth: 긍/부정 모델 state_dict(model 로드 시 필요).
│   ├── sentiment_review.py: 스크래핑한 리뷰 긍/부정 분류
---
```
## 유의사항
### Mecab 설치 필요
https://github.com/nuri428/mecab-ko-m1

## 보완점
### 사용자가 영화를 선택할 때 고려하는 사항에 대한 정보를 제공할 수 있는 기능 부족
>   - 좋아하는 영화감독이나 배우가 출현하는 영화에 대한 정보 노출 기능<br>
>   - 다음영화 사이트에 스크래핑 과정 최적화를 통한 소요시간 단축
>   
### 긍/부정 모델 성능 개선
>   - 분류 정확도 향상
>   - 모델을 경량화하여 추론 시간 단축
>   - 모델 성능 향상 및 긴 길이의 리뷰 처리 가능한 모델로 교체(RoBERTa)
>   - 영화와 관련 없는 리뷰 필터링(정치, 광고 등에 관한 리뷰)
