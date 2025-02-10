import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from tensorflow.keras.models import Sequential
from keras.layers import Dense

# 1. 데이터 수집 (시뮬레이션)
np.random.seed(42)
data_size = 1000
temperature = np.random.normal(25, 5, data_size)  # 온도 데이터
pressure = np.random.normal(1013, 10, data_size)  # 압력 데이터
vibration = np.random.normal(0.5, 0.1, data_size)  # 진동 데이터
failure = (temperature > 30).astype(int)  # 고장 여부 (온도가 30도 이상일 때)

# 데이터프레임 생성
data = pd.DataFrame({
    'Temperature': temperature,
    'Pressure': pressure,
    'Vibration': vibration,
    'Failure': failure
})

# 2. 데이터 전처리
X = data[['Temperature', 'Pressure', 'Vibration']]
y = data['Failure']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. 모델 학습 (전통적 ML)
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# 3. 모델 학습 (딥러닝)
dl_model = Sequential()
dl_model.add(Dense(10, input_dim=3, activation='relu'))
dl_model.add(Dense(1, activation='sigmoid'))
dl_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
dl_model.fit(X_train, y_train, epochs=50, batch_size=10, verbose=0)

# 4. 예측 및 결과 시각화
rf_predictions = rf_model.predict(X_test)
dl_predictions = dl_model.predict(X_test)

# 결과 시각화
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.scatter(y_test, rf_predictions, alpha=0.5)
plt.title('Random Forest Predictions')
plt.xlabel('True Values')
plt.ylabel('Predictions')

plt.subplot(1, 2, 2)
plt.scatter(y_test, dl_predictions, alpha=0.5)
plt.title('Deep Learning Predictions')
plt.xlabel('True Values')
plt.ylabel('Predictions')

plt.tight_layout()
plt.show()
