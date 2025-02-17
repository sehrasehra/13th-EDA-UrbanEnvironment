# 프로젝트 요약
- 구성원:신영군(팀장 12기),김민규(12기),이유주(13기),박수빈(13기),조지성(13기)
- 프로젝트 목적: 
## 1. 데이터 출처
- **선수 데이터**는 2014년 소치 올림픽, 세계선수권, 유럽 및 4대륙 선수권, 그랑프리 파이널 대회 등의 경기 기록을 기반으로 수집. 
이 데이터는 선수들의 성적과 점수 변화 패턴을 분석하는 데 사용.

- **미디어 데이터**는 GOOGLE API를 통해 수집된 경기 영상의 댓글을 분석하여 팬들의 반응을 조사.

- **심판 임명제 데이터**는 2002년 올림픽 심판 매수 논란 이후 도입된 익명 심판제와 2018년 평창 올림픽에서 도입된 실명 심판제를 비교 분석하는 데 사용. 이 데이터는 심판의 국가적 배경과 점수 부여 패턴을 분석하는 데 활용.

- **국가적 데이터**국가별로 역대 올림픽 피겨 점수 데이터, 메달리스트 수 데이터를 활용해 피겨 스케이팅 강국과 중견국으로 전처리.
1. **미디어 기반 감정 분석**:
   - 구글 API를 활용해 경기 영상의 댓글을 수집하고 감정 분석을 실시하여 팬들의 반응을 조사.
   - 워드 클라우드를 통해 주요 키워드를 시각화하고, 감정 점수를 계산하여 판정 논란이 글로벌 이슈였음을 확인.

2. **LLM 기반 인과 관계 분석**:
   - 사전 학습된 언어 모델(LLM)을 활용하여 선수들의 성적과 경기 관련 리뷰 데이터를 분석.
   - LLM은 점수와 관련된 핵심 요소들을 자동으로 추출하고 수치화하여, 여자 싱글 경기에서 공정성 요소가 중요한 변수로 작용했음을 확인.

3. **선수 점수 예측**:
   - 선수들의 이전 경기 데이터를 기반으로 시계열 분석을 통해 소치 올림픽 점수를 예측.
   - ARIMA 모델을 사용하여 점수 변화 패턴을 분석하고, 소트니코바의 점수가 이례적으로 높았음을 확인.

4. **심판과 국가적 요인 분석**:
   - 심판 명단을 분석하여 러시아 심판이 특정 선수들에게 유리한 점수를 부여했는지 확인.
   - t-test 및 점수 변화량 비교를 통해 러시아 선수들이 PCS에서 유의미하게 높은 점수를 받았음을 확인.
   - 익명 심판제와 실명 심판제를 비교하여, 익명 심판제가 특정 국가 선수들에게 유리한 판정을 했을 가능성을 시사함.

5. **강대국 어드밴티지 분석**:
   - 강대국과 중견국의 PCS 점수를 비교하여, 강대국 선수들이 PCS에서 유리한 점수를 받는 경향이 있음을 확인.
   - 익명 심판제가 강대국 어드밴티지에 영향을 미쳤음을 데이터로 검증.

#### 4. 결론
- **미디어 데이터 분석**을 통해 2014년 소치 올림픽에서 판정 논란이 세계적으로 확산되었음을 확인.
- **LLM 분석**을 통해 점수 판정에서 공정성 요소가 중요한 영향을 미쳤음을 확인.
- **선수 개인 기록 분석**을 통해 소트니코바 선수의 점수 상승이 이례적으로 급격한 패턴을 보였음을 확인.
- **국가 수준 분석**을 통해 강대국 출신 선수들이 PCS에서 상대적으로 높은 점수를 받는 경향이 있음을 확인.
- **익명 심판제**가 판정 편향에 영향을 미쳤음을 데이터로 검증됨됨.
- **공정한 경기 환경**을 유지하기 위해서는 심판 판정의 투명성을 보장하는 시스템 개선이 필요함을 시사함함.

이 연구는 판정 논란이 단순한 주관적 의견이 아니라, 데이터로도 검증될 수 있음을 보임.
----
# Project Summary
- Team Members: 신영군(team lead 12기),김민규(12기),이유주(13기),박수빈(13기),조지성(13기)
- Project Purpose:
## 1. Data Sources
- **Athlete Data** was collected based on competition records from the 2014 Sochi Olympics, World Championships, European and Four Continents Championships, and Grand Prix Finals. This data was used to analyze athletes' performance and score change patterns.

- **Media Data** was collected through the Google API, analyzing comments on competition videos to investigate fan reactions.

- **Judge Appointment System Data** was used to compare the anonymous judging system introduced after the 2002 Olympic judging scandal with the real-name judging system introduced at the 2018 Pyeongchang Olympics. This data was utilized to analyze judges' national backgrounds and scoring patterns.

- **National Data** included historical Olympic figure skating score data and medalist counts by country, which were preprocessed to categorize countries into figure skating powerhouses and mid-tier nations.

1. **Media-Based Sentiment Analysis**:
   - Collected comments on competition videos using the Google API and conducted sentiment analysis to investigate fan reactions.
   - Visualized key keywords through word clouds and calculated sentiment scores, confirming that judging controversies were a global issue.

2. **LLM-Based Causal Relationship Analysis**:
   - Utilized a pre-trained language model (LLM) to analyze athletes' performance and competition-related review data.
   - The LLM automatically extracted and quantified key factors related to scores, confirming that fairness elements were significant variables in women's singles competitions.

3. **Athlete Score Prediction**:
   - Predicted Sochi Olympic scores based on athletes' previous competition data using time series analysis.
   - Used the ARIMA model to analyze score change patterns, confirming that Sotnikova's scores were unusually high.

4. **Judge and National Factor Analysis**:
   - Analyzed judge lists to determine if Russian judges favored certain athletes.
   - Used t-tests and score change comparisons to confirm that Russian athletes received significantly higher PCS scores.
   - Compared anonymous and real-name judging systems, suggesting that the anonymous system may have favored athletes from specific countries.

5. **Powerhouse Advantage Analysis**:
   - Compared PCS scores between powerhouse and mid-tier nations, confirming that athletes from powerhouse nations tended to receive higher PCS scores.
   - Verified through data that the anonymous judging system influenced the powerhouse advantage.

#### 4. Conclusion
- **Media Data Analysis** confirmed that the judging controversy at the 2014 Sochi Olympics spread globally.
- **LLM Analysis** confirmed that fairness elements significantly influenced score judgments.
- **Athlete Performance Analysis** confirmed that Sotnikova's score increase followed an unusually sharp pattern.
- **National-Level Analysis** confirmed that athletes from powerhouse nations tended to receive higher PCS scores.
- **Anonymous Judging System** was verified to have influenced judging bias.
- Suggested that **ensuring transparency in judging systems** is necessary to maintain a fair competition environment.

This study demonstrated that judging controversies are not merely subjective opinions but can be verified through data.