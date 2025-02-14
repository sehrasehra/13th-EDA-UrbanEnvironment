## 주제: TV광고 시청률을 높이는 요인 분석
#### 참여자 : 복지민, 정주은, 이채원, 송채은
#### EDA 프로젝트 자료 소개
> * Dataset 
>   * [월별 맛집 음식 지상파 광고 집행 DB 정보](https://www.bigdata-culture.kr/bigdata/user/data_market/detail.do?id=c633755c-6631-4cfd-ab20-b16ff294dc2c) : 월별 지상파 채널에서 맛집 음식 광고 집행 내역; 2023년 1월~12월 데이터 사용. 
> * [EDA 발표자료](https://github.com/wlalsl/13th-EDA/blob/main/%EB%AF%B8%EB%94%94%EC%96%B4/25_1_DSL_EDA_%EB%AF%B8%EB%94%94%EC%96%B4.pdf) : EDA 발표 때 사용한 ppt입니다.
> * [EDA 최종 코드](https://github.com/wlalsl/13th-EDA/blob/main/%EB%AF%B8%EB%94%94%EC%96%B4/code/%E1%84%82%E1%85%A1%E1%84%86%E1%85%AE%2B%E1%84%80%E1%85%A5%E1%86%B7%E1%84%8C%E1%85%A5%E1%86%BC%2B%E1%84%92%E1%85%AC%E1%84%80%E1%85%B1.ipynb) : EDA 발표와 관련하여 사용된 코드입니다.

<br>



## EDA 프로젝트 요약

1. 프로젝트 주제 및 목적
        - 2023년 광고 DB 정보를 통해 시청률에 기여하는 요인 파악 & 분석, 향후 광고 효과를 높이기 위해 집중해야 할 요소들 탐색

2. 데이터 전처리

        - 2023년 1월~12월 데이터 merge (merged2023.csv 파일 용량 초과로 인해 데이터전처리.ipynb 코드만 첨부)
           - 중복되거나 관련없는 불필요한 열 삭제
           - `AREA_NM`이 `"전국"`인 행 제거 (극소수)
           - `CHNNEL_NM`이 `"MBC"`, `"SBS"`, `"KBS"` 중 하나인 경우만 유지 (3대 방송사 데이터에 집중적으로 분석)
           - frequency 열 생성 (파생 변수)
             - 모든 노출률(`NT01_EXPSR_REACH_RT` ~ `NT05_EXPSR_REACH_RT`)이 NaN 또는 0인 행 제거
             - `frequency` 컬럼 생성 (노출 빈도 계산)
             - 기존의 `NT01` ~ `NT05` 컬럼 삭제
        - 시각화용 데이터 생성 (visual.csv)
        - 분석용 데이터 생성 (dummy.csv , 더미변수_전처리.ipynb)
           - 범주형 데이터 더미변수화
            
 
4. 분석 방법 및 결과
    
        - 목표변수 설정: GRP(Gross Rating Points)
   
        - 1. Visualization
   
           - (i) Class(TV광고 단가)별 GRP분포 확인
           - (ii) 프로그램 유형(프로,토막,자막)별 GRP분포 확인
           - (iii) 유형&Class별 GRP분포 확인
           - (iv) 지역별 & 타겟별 GRP분포 확인
               - Mann-Whitney U Statistic로 유료매체 vs. 무료매체 간 차이 검정
           - (v) 광고시간대별, 채널별 GRP분포 확인
   
        - 2. Regression
   
           - Frequency간 차이 유효성 검정(Mann-Whitney U statistic)
   
           - (i) Frequency별로 주요 변수 선정 - 랜덤포레스트
           - (ii) 변수 유의성 + 모델 생성 - 회귀분석
               - 랜덤 포레스트에서 선정된 변수 + 교호작용 반영한 회귀모델 생성
               - 전체 변수 + 교호작용 변수 반영한 회귀모델 생성
           - (iii) Elastic-Net (다중공선성 해결 방안)
		    
6. 결론

        - 유의 변수 결과:
          - Random Forest: CLASS_SA / AD_POS_중간 / ADVRTS_TIME
          - Elastic-Net: CLASS_SA / AD_POS_중간 / TYPE_프로
        - 시청 시간대에 따라 나뉘는 CLASS_SA, 광고 위치(중간)이 GRP에 가장 큰 영향을 미치는 변수로 선정됨
        - GRP, 즉 총시청률을 높이기 위해서는 SA 시간대와 프로그램 중간에 광고를 삽입했을때 보다 큰 광고 효과를 불러일으킬 것으로 예상할 수 있음. 
    
8. 아쉬운 점
    
        - 회귀 모델 설명력이 0.25에서 그침 (중간 정도)
        - 사용한 데이터셋만으로 GRP를 모두 설명해낼 수 없음 (다른 요인이 존재할 것으로 추측)

10. 추가로 하면 좋을 분석 방법
    
        - 광고비와 같은 추가적인 외부 데이터가 있었다면 광고비는 최소화하면서 광고효과를 극대화할 수 있는 방안에 대해 분석해볼 수 있었을 것 같음.  

<br>




--------------------------------------------------------------------------------------------------------------------------------


## Topic: Factors Influencing TV Commercial Viewership
#### Team Members: Ji Min Bok, Joo Eun Jung, Chae Won Lee, Chae Eun Song
#### Introduction to the EDA Project
> * Dataset 
>   * [월별 맛집 음식 지상파 광고 집행 DB 정보](https://www.bigdata-culture.kr/bigdata/user/data_market/detail.do?id=c633755c-6631-4cfd-ab20-b16ff294dc2c) : Contains monthly records of gourmet food commercials aired on terrestrial TV channels
>   * Data period: January to December 2023
> * [EDA 발표자료] (https://github.com/wlalsl/13th-EDA/blob/main/%EB%AF%B8%EB%94%94%EC%96%B4/25_1_DSL_EDA_%EB%AF%B8%EB%94%94%EC%96%B4.pdf) : Slides used for the EDA presentation
> * [EDA 최종 코드] (https://github.com/wlalsl/13th-EDA/blob/main/%EB%AF%B8%EB%94%94%EC%96%B4/code/%E1%84%82%E1%85%A1%E1%84%86%E1%85%AE%2B%E1%84%80%E1%85%A5%E1%86%B7%E1%84%8C%E1%85%A5%E1%86%BC%2B%E1%84%92%E1%85%AC%E1%84%80%E1%85%B1.ipynb) : Code used in the EDA analysis

<br>



## Project Summary

1. Project Objective
        - Analyze factors that contribute to TV commercial viewership using 2023 advertising data
        - Identify key elements to maximize advertising effectiveness in the future

2. Data Preprocessing

        - Merged data from January to December 2023 (merged2023.csv was too large to upload, so only the preprocessing script 데이터전처리.ipynb is provided)
           - Removed duplicate and irrelevant columns
           - Dropped rows where AREA_NM = "전국" (insignificant count)
           - Kept only data from the three major broadcasting networks:`CHNNEL_NM`=`"MBC"`, `"SBS"`, `"KBS"` 
           - Created a frequency variable:
             - Removed rows where all exposure rates (NT01_EXPSR_REACH_RT ~ NT05_EXPSR_REACH_RT) were NaN or 0
             - Added frequency column (calculated exposure frequency)
             - Dropped original NT01 ~ NT05 columns
        - Created datasets for:
           - Visualization (visual.csv)
        - Analysis (dummy.csv, preprocessing script: 더미변수_전처리.ipynb)
           - Converted categorical variables into dummy variables
            
 
4. Analysis Methods & Results
    
        - Target Variable:
             GRP(Gross Rating Points)
   
        - 1. Visualization Analysis
   
           - (i) GRP distribution across different advertising cost classes
           - (ii) GRP distribution across ad types (program, short-form, caption)
           - (iii) GRP distribution by ad type & cost class
           - (iv) GRP distribution by region & target audience
               - Mann-Whitney U test to compare paid vs. free media
           - (v) GRP distribution by time slot & TV channel
   
        - 2. Regression
   
           - Significance Test for Frequency Differences (Mann-Whitney U test)
   
           - (i) Key variable selection based on Random Forest
           - (ii) Regression model development incorporating significant variables & interactions:
                - Model 1: Random Forest-selected variables + interaction terms
                - Model 2: All variables + interaction terms
           - (iii) Elastic-Net regression to address multicollinearity
		    
6. Key Findings

        - Significant variables impacting GRP:
          - Random Forest: CLASS_SA, AD_POS_Mid, ADVRTS_TIME
          - Elastic-Net: CLASS_SA, AD_POS_Mid, TYPE_Program
        - Key Takeaways:
            - Ad placement in SA time slots and mid-program positions had the most substantial effect on GRP.
            - To maximize GRP, advertisements should be placed during SA time slots and within the middle of programs.
    
8.  Limitations
    
        - Regression model had a moderate explanatory power (R² = 0.25)
        - GRP cannot be fully explained by the given dataset, suggesting other influencing factors exist

10. Future Analysis Opportunities
    
        - Incorporating external data, such as advertising costs, could help optimize ad effectiveness while minimizing expenses.

<br>


 
