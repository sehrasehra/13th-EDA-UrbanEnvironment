
# 필요한 패키지 로드
#install.packages(c("readxl","ggplot2", "glmnet"))
#if (!requireNamespace("dplyr", quietly = TRUE)) {
#  install.packages("dplyr")
#}
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


# 병상포화지수 변수 추출 및 시각화
data$병상포화지수 <- as.numeric(data$병상포화지수)
ggplot(data, aes(x = 병상포화지수)) +
  geom_density(fill = "blue", alpha = 0.5) +
  labs(title = "병상포화지수 밀도 그래프", x = "병상포화지수", y = "밀도") +
  theme_minimal()

# 병상포화지수 로그 변환
data$log_병상포화지수 <- log(data$병상포화지수)

# log_병상포화지수 정규성 검정
shapiro_test <- shapiro.test(data$log_병상포화지수)
print(shapiro_test)
# 결과적으론 정규성을 안띰!!
# 그렇다면 box-cox 변환 적용해보자.


#if (!requireNamespace("MASS", quietly = TRUE)) {
#  install.packages("MASS")
#}
library(MASS)

# 병상포화지수에서 0 또는 음수가 없는지 확인
if (any(data$병상포화지수 <= 0)) {
  stop("Box-Cox 변환을 적용하려면 병상포화지수 값이 모두 양수여야 합니다.")
}

# 종속변수를 병상포화지수로 설정한 선형 모델
model <- lm(병상포화지수 ~ 1, data = data)

# Box-Cox 변환 실행
boxcox_result <- boxcox(model, lambda = seq(-2, 2, by = 0.1))

# 최적의 lambda 값 선택
best_lambda <- boxcox_result$x[which.max(boxcox_result$y)]
cat("최적의 lambda 값:", best_lambda, "\n")

# Box-Cox 변환 적용
data$병상포화지수_boxcox <- (data$병상포화지수^best_lambda - 1) / best_lambda

# 최적 lambda 값이 0에 가까운 경우 로그 변환으로 처리
if (abs(best_lambda) < 1e-5) {
  data$병상포화지수_boxcox <- log(data$병상포화지수)
}

# 변환된 변수 확인
head(data$병상포화지수_boxcox)

shapiro_test <- shapiro.test(data$병상포화지수_boxcox)
print(shapiro_test)
# 정규성 띰!!! -> 이대로 분석진행.






# 종속변수와 독립변수 설정
y <- data$병상포화지수_boxcox
x <- as.matrix(data[, !(names(data) %in% c("연도", "병상포화지수", "병상포화지수_boxcox","log_병상포화지수", "지역"))])
head(x)

# 라소 회귀분석 수행
lasso_model <- cv.glmnet(x, y, alpha = 1, standardize = TRUE)

# 최적 람다 값과 계수 확인
print(lasso_model$lambda.min)
coef(lasso_model, s = "lambda.min")




# 라소 회귀 결과에서 유의한 변수 선택
# 라소 회귀의 계수 확인
lasso_coefficients <- as.matrix(coef(lasso_model, s = "lambda.min"))
selected_variables <- rownames(lasso_coefficients)[lasso_coefficients != 0][-1]  # 상수항 제거

# 선택된 변수로 데이터 필터링
filtered_data <- data[, c("병상포화지수_boxcox", selected_variables)]
head(filtered_data)

# 문자형 변수를 숫자형으로 변환
numeric_data <- filtered_data %>% mutate(across(where(is.character), as.numeric))

# 다중회귀 분석
multi_reg_model <- lm(병상포화지수_boxcox ~ ., data = numeric_data)

# 회귀 분석 결과 출력
summary(multi_reg_model)


# 잔차 플롯
par(mfrow = c(2, 2))
plot(multi_reg_model)







