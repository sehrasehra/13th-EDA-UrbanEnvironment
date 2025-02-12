library(dplyr)
library(readxl)
library(ggplot2)
library(glmnet)

# 데이터 불러오기
setwd("C:/Users/dolly/OneDrive/바탕 화면/DSL/DSL EDA 25-1")
getwd()
raw_data <- read_excel("data_standardized.xlsx",sheet = 1, col_names = FALSE)
head(raw_data)

# 첫 두 행 삭제
data <- raw_data[-c(1, 2), ]

# 세 번째 행을 열 이름으로 설정
colnames(data) <- raw_data[3, ]

# 세 번째 행 삭제
data <- data[-1, ]

# 데이터 구조 확인
head(data)
colnames(data)
dim(data)








########## 다중회귀 Stepwise(-병상수, -도착소요시간, -교통, +화재)
##########
########## forward, backward, hybrid 모두 같은 결과 도출.
########## selected: 미충족,중증,응급의,스트레스,비만율,일인가구,출산율,사망률(8개).
########## 이중 유의변수: 응급의,비만율,일인가구,출산율
##################################################################
y <- data$병상포화지수
x <- as.matrix(data[, !(names(data) %in% c("연도", "병상포화지수", "지역","병상수", "응급실도착소요시간","교통사고발생건수"))])
head(x)
dim(x)
summary(x)

x_df <- as.data.frame(x)
numeric_data <- x_df %>% mutate(across(where(is.character), as.numeric))
summary(numeric_data)

# y를 데이터프레임의 열로 추가
full_data <- cbind(병상포화지수 = y, numeric_data)

# 결과 확인
dim(full_data)
head(full_data)

######### Backward ##########
# 기본 모델 (모든 변수를 포함한 모델)
full_model <- lm(병상포화지수 ~ ., data = full_data)
summary(full_model)

# Backward Stepwise Selection
backward_model <- step(full_model, direction = "backward")

# 결과 요약
summary(backward_model)

######### Forward ##########
# 기본 모델 (변수가 없는 모델)
null_model <- lm(병상포화지수 ~ 1, data = full_data)

# 전체 모델 (모든 변수를 포함한 모델)
full_model <- lm(병상포화지수 ~ ., data = full_data)

# Forward Stepwise Selection
forward_model <- step(null_model, 
                      scope = formula(full_model), 
                      direction = "forward")

# 결과 요약
summary(forward_model)


######### Hybrid ##########
# 기본 모델 (모든 변수를 포함한 모델)
full_model <- lm(병상포화지수 ~ ., data = full_data)

# Stepwise Selection (Both)
stepwise_model <- step(full_model, direction = "both")

# 결과 요약
summary(stepwise_model)





########## 다중회귀 Stepwise(-병상수, +도착소요시간, -교통, -화재)
##########
########## 3개 다 같은 결과.
########## selected: 미충족,중증,응급의학,스트레스,비만율,일인가구,츨산율,사망률(8개).
########## 8개 중 유의한 변수: 응급의학, 비만율, 일인가구비율, 출산율.
##################################################################
y <- data$병상포화지수
x <- as.matrix(data[, !(names(data) %in% c("연도", "병상포화지수", "지역","교통사고발생건수", "병상수","화재발생건수"))])
head(x)
dim(x)
summary(x)

x_df <- as.data.frame(x)
numeric_data <- x_df %>% mutate(across(where(is.character), as.numeric))
summary(numeric_data)

# y를 데이터프레임의 열로 추가
full_data <- cbind(병상포화지수 = y, numeric_data)

# 결과 확인
dim(full_data)
head(full_data)

######### Backward ##########
# 기본 모델 (모든 변수를 포함한 모델)
full_model <- lm(병상포화지수 ~ ., data = full_data)
summary(full_model)

# Backward Stepwise Selection
backward_model <- step(full_model, direction = "backward")

# 결과 요약
summary(backward_model)

######### Forward ##########
# 기본 모델 (변수가 없는 모델)
null_model <- lm(병상포화지수 ~ 1, data = full_data)

# 전체 모델 (모든 변수를 포함한 모델)
full_model <- lm(병상포화지수 ~ ., data = full_data)

# Forward Stepwise Selection
forward_model <- step(null_model, 
                      scope = formula(full_model), 
                      direction = "forward")

# 결과 요약
summary(forward_model)


######### Hybrid ##########
# 기본 모델 (모든 변수를 포함한 모델)
full_model <- lm(병상포화지수 ~ ., data = full_data)

# Stepwise Selection (Both)
stepwise_model <- step(full_model, direction = "both")

# 결과 요약
summary(stepwise_model)

