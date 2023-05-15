# Movie_review_analysis


## 프로젝트 개요
> 사용자가 영화를 선택하는 과정에 도움을 주기 위한 API 개발<br>
> **개발기간 2023.04 ~ 2023.05**


## API 기능 소개
> - 영화 기본 정보(출연진, 줄거리 등)
> - 평점, 긍/부정별 리뷰에 대한 테이블 뷰, 워드클라우드 제공

## API 화면


### 디렉토리 구조
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
