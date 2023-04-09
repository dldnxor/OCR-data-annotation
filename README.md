# 🏆데이터 제작 프로젝트🏆
---
![](https://velog.velcdn.com/images/tls991105/post/22fe4b87-92dd-44e9-a6c0-5a8cf60cbae9/image.png)

---
## 🔥Member
| [정승윤](https://github.com/syoon6682) | [김주희](https://github.com/alias26) | [신현수](https://github.com/Hyun-soo-Shin) | [이우택](https://github.com/dldnxor) | [이해욱](https://github.com/woooo-k) |
| :-: | :-: | :-: | :-: | :-: |
| <img src="https://avatars.githubusercontent.com/syoon6682" width="100"> | <img src="https://avatars.githubusercontent.com/alias26" width="100"> | <img src="https://avatars.githubusercontent.com/Hyun-soo-Shin" width="100"> | <img src="https://avatars.githubusercontent.com/dldnxor" width="100"> | <img src="https://avatars.githubusercontent.com/woooo-k" width="100"> |
---
## Index
- [🏆데이터 제작 프로젝트🏆](#데이터-제작-프로젝트)
  - [🔥Member](#member)
  - [Index](#index)
  - [🏅Project Summary](#project-summary)
  - [👨‍👩‍👧‍👧Team Roles](#team-roles)
  - [🗃️Procedures](#️procedures)
  - [📊Result](#result)
    - [Data Augmentation](#data-augmentation)
    - [모델 개요](#모델-개요)
    - [시연결과](#시연결과)
  - [👨‍💻Conclusion](#conclusion)
  - [💻Requirements](#requirements)
  - [🏗️Folder Structure](#️folder-structure)
---
## 🏅Project Summary

>### - 프로젝트 주제
> 스마트폰으로 카드를 결제하거나, 카메라로 카드를 인식할 경우 자동으로 카드 번호가 입력되는 경우가 있습니다. 또 주차장에 들어가면 차량 번호가 자동으로 인식되는 경우도 흔히 있습니다. 이처럼 OCR (Optimal Character Recognition) 기술은 사람이 직접 쓰거나 이미지 속에 있는 문자를 얻은 다음 이를 컴퓨터가 인식할 수 있도록 하는 기술로, 컴퓨터 비전 분야에서 현재 널리 쓰이는 대표적인 기술 중 하나입니다.
OCR task는 글자 검출 (text detection), 글자 인식 (text recognition), 정렬기 (Serializer) 등의 모듈로 이루어져 있습니다.
>
>### - 개요 및 기대효과
> 학교나 수업에서 다루는 AI 모델 연구과정에서는 일반적으로 데이터와 평가 방법이 주어지고, 모델 구조를 변경하면서 해당 데이터와 평가방식에 가장 잘맞는 모델을 찾아나가는 과정을 배우게 됩니다. 하지만 실무에서는 서비스의 기획만 존재할 뿐, 데이터, 베이스라인 모델, 평가방법 모두 제공되지 않는 경우가 일반적입니다. 모델의 성능을 개선하기 위하여 정답 라벨링 노이즈가 없는 양질의 데이터를 확보해야 하고, 또한 모델을 공정하게 평가하기 위해선 테스트 데이터의 정답이 정확해야 하는 등 전체 프로세스에서 데이터 제작 작업이 차지하는 비중이 높고 매우 중요한 작업입니다. 이번 프로젝트를 통해 실무에서 활용되는 AI 프로젝트 과정의 전반적인 이해(데이터 제작, 모델 개발, 성능 평가)와, 피드백 사이클을 통하여 점진적으로 모델 성능을 개선해나가는 전체적인 프로세스를 경험해 볼 수 있습니다.
>
>### - 활용 장비 및 재료 
>- 서버: V100 GPU
>- 사용 모델: EAST + VGG16 
>- 개발 및 협업 툴: Git, Slack, Zoom, Visual Studio Code
>
> ### - 데이터 셋의 구조도
>- 전체 이미지 개수 : ICDAR17(2970장) + ICDAR15(1000장) + upstage_data(702장)
>- Input : 글자가 포함된 전체 이미지
>- Format : bbox 좌표가 포함된 UFO Format
>
---
## 👨‍👩‍👧‍👧Team Roles
>- **이우택**: EDA, upstage 데이터 전처리
>- **정승윤**: Dataset 탐색 및 결합, 모델 에러 디버깅, 야외 한글 데이터 전처리
>- **김주희**: Wandb Logging, Augmentation 실험 및 관리, 데이터셋 탐색
>- **이해욱**: W&B Sweep을 이용한 Hyperparameter Tuning 시도 
>- **신현수**: Dataset 탐색 및 결합, EDA
---
## 🗃️Procedures
>**[2022.12.05 ~ 2022.12.07]**
>- Data Annotation 강의 수강 및 프로젝트 기획
서버 설정 및 개발 환경 setting
>- Annotation 툴을 활용하여 Annotation 실습 진행
><br>
>
>**[2022.12.08 ~ 2022.12.10]**
>- 오피스아워를 통한 Baseline 이해
>- Baseline 팀 환경에 맞게 setting
>  - Seed 고정
>  - Validation Dataset 설정
>  - Wandb setting
><br>
>
>**[2022.12.11 ~ 2022.12.12]**
>- 추가 데이터 탐색 및 Concat 시도
>  - 기본 데이터: ICDAR17_Korea
>  - ICDAR15, ICDAR17 All 데이터 탐색 및 UFO 형태로 JSON 파일 제작
><br>
>
>**[2022.12.13 ~ 2022.12.14]**
>- Augmentation 실험 진행
>  - 많은 실험을 위해 ICDAR_Korea 데이터로만 진행 
>  - Distortion, MotionBlur, GuassNoise, Weather 등 다양한 Augmentation을 상관관계를 생각하며 적용
><br>
>
>**[2022.12.13 ~ 2022.12.14]**
>- 최종 학습
>   - ICDAR15, ICDAR17, Upstage 데이터셋을 Concat
>   - Augmentation 실험을 통해 얻은 최적의 Augmentation을 활용
>   - 팀원 별로 Input size와 Image size를 다르게 적용하며 학습 진행 

---
## 📊Result
>### 탐색적 분석(EDA) 및 데이터 전처리
>> * 이미지 분포
>>
>>|ICDAR15|ICDAR17|Upstage|
>>|:----:|:----:|:----:|
>>|모든  데이터의  크기가  1280  X  720|<img src="https://velog.velcdn.com/images/tls991105/post/c1f2ef7d-91bb-4032-9c3d-023ee680c7ac/image.png" width="400"/>|<img src="https://velog.velcdn.com/images/tls991105/post/7fecd8d8-c5f1-4bd1-ad2b-c30f4df0cb97/image.png" width="400"/>|
>>
>> ICDAR17의 이미지 크기가 다양하게 분포하고 있음
>
>> * 이미지당 단어 개수
>>
>>|ICDAR15|ICDAR17|Upstage|
>>|:----:|:----:|:----:|
>>|<img src="https://velog.velcdn.com/images/tls991105/post/d401749f-bd10-401a-8d95-85d2dc9c1f23/image.png">|<img src="https://velog.velcdn.com/images/tls991105/post/00b03251-a5bf-4a09-9f76-8ed048d12c06/image.png">|<img src="https://velog.velcdn.com/images/tls991105/post/8df3ba94-1c0e-49c8-9886-c704e4971288/image.png">|
>>
>> 이미지당 단어는 0~10개 사이의 분포가 가장 많았음

>> * 언어 분포
>>
>>|ICDAR15|ICDAR17|Upstage|
>>|:----:|:----:|:----:|
>>|<img src="https://velog.velcdn.com/images/tls991105/post/46e4f837-4b4f-4db1-bcbd-ba72c256ea08/image.png">|<img src="https://velog.velcdn.com/images/tls991105/post/a9befc27-0b0f-4cba-a812-67ce7b98b9ed/image.png">|<img src="https://velog.velcdn.com/images/tls991105/post/f254f4dc-a7ec-461e-98ed-c003a8b1fee1/image.png">|
>>
>> ICDAR15와 ICDAR17 데이터는 영어의 비중이 매우 많았고 Upstage 데이터는 한글과 영어의 비중이 1:1의 비율을 보여주었다. 
>
>> * BBOX size
>>
>>|ICDAR15|ICDAR17|Upstage|
>>|:----:|:----:|:----:|
>>|<img src="https://velog.velcdn.com/images/tls991105/post/bc4538f8-9c54-4c41-ae99-b4786187c21e/image.png">|<img src="https://velog.velcdn.com/images/tls991105/post/db9bacbb-544b-406e-871f-d472e707c75f/image.png">|<img src="https://velog.velcdn.com/images/tls991105/post/1cfc4952-aa8e-4836-8964-b88ca0f29ebd/image.png">|
>>
>> 대부분의 이미지의 BBox 1프로보다 작은 크기의 BBox가 대부분임을 확인.
>
>> 

>#### 데이터 전처리
>- 야외 실제 촬영 한글 이미지
>   - Test Data가 주로 한글로 이루어졌으므로 AI-Hub에 있는 야외 실제 촬영 한글 이미지를 추가하여 활용하고자 함
>   - Data annotation 파일이 이미지당 하나의 txt 파일로 이루어져 통합하여 UFO 형태로 바꾸는 python 파일을 작성함
>   - 그러나 원데이터가 너무 큰 용량을 가져서 전체 데이터를 활용할 수 없고, 샘플데이터는 bias가 너무 커서 실제로 데이터를 활용하진 못함
>
>- upstage 데이터
>   - 원활한 학습을 위해 upstage 데이터 중 사각형이 아닌 다각형 형태로 이루어진 bbox를 포함한 이미지를 제외함
>   - 제외한 이미지들에 대해 annotation 파일을 편집함

### Data Augmentation
>**Metric: F1-Score**
>|None|Distort|+MotionBlur|+GaussianNoise|All|
>|:----:|:----:|:----:|:----:|:----:|
>|0.4621|0.4939|0.4934|0.5398|0.5627|


### 모델 개요
>EAST + VGG16  

### 시연결과
>**Metric: F1-Score**
>|F1-Score|Recall|Precision|
>|:----:|:----:|:----:|
>|0.6364|0.5689|0.7220|
---
## 👨‍💻Conclusion
>#### 잘한 점들
>1. Augmentation 실험을 체계적으로 진행함
>2. 소통과 협업이 원활하게 잘 이루어짐
>3. 서로의 코드를 보고 리뷰하면서 실험 관리 
>
>#### 아쉬운 점들
>1. 저번 프로젝트보다는 활용을 좀더 했으나 아직 github 프로젝트 활용도가 높지 않음
>2. W&B Sweep을 이용한 Hyperparameter Tuning을 시도해보려고 하였으나 실패함
>3. 학습 도중에 멈추는 상황이 여럿 발생하여 원하는 결과를 보는데에 어려움이 있었음
>
> #### 프로젝트를 통해 배운점
>1. 일관성 있는 데이터와 라벨링의 중요성을 알게 됐음.
>2. OCR Task에 대한 이해도를 높일 수 있었음.
>3. 실제로 annotation 툴을 활용하여 데이터를 제작해보고 제작된 데이터를 실제로 활용을 어떻게 하는지 경험해봄
---
## 💻Requirements
```
pip install -r requirements.txt

apt-get update
apt-get install ffmpeg libsm6 libxext6  -y
```
---
## 🏗️Folder Structure
```
└── level2_dataannotation_level2_cv_09  
      ├── convert_mlt  #ICDAR Json to UFO Format
      ├── dataset
      ├── detect
      ├── deteval  #Metrics
      ├── east_dataset 
      ├── inference
      ├── loss
      ├── merge_data
      ├── model
      ├── train_many  #Multiple Dataset
      ├── train_noval  #No Validation
      ├── train 
      ├── transfer_outsideKo  #AIHub Json to UFO Format
      └── upstage_preprocess  #Preprocess Upstage Dataset

```
---
