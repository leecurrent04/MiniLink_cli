# NALDA_backend_serial_cli

> FC Firmware는 다음 [[Github] STM32-FC](https://github.com/NARAE-INHA-UNIV/STM32-FC)를 참고하세요.

STM32-FC 데이터 읽기 & 파라미터 수정을 위한 CLI 프로그램

## 실행 방법

### 1. 패키지 설치 (최초 1회만)

```bash
pip isntall pyserial questionary keyboard numpy
```

### 2. 실행

```bash
python main.py
```

### 3. FC가 연결된 포트 선택 

```bash
# 아래에 나오는 포트 목록은 컴퓨터마다 다를 수 있습니다.
 ? Choose Serial Port : (Use arrow keys)
 » COM3 - STMicroelectronics Virtual COM Port(COM3)
   a) EXIT
```
화살표 키로 이동, Enter로 선택

### 4. Baud rate 선택

```bash
? Choose baudrate : (Use arrow keys)
   9600
 » 57600
   115200
   a) MANNUAL INPUT
   b) ../
```

- USB CDC 연결인 경우, 아무 값 입력
- Telem 단자인 경우 설정한 값 입력. 일반적으로 **57600**(MAVLink), 115200(Others)임.
- 보기 외에 값을 입력하고 싶은 경우, `MANNUAL INPUT`를 선택 후 입력.


### 5. 확인할 msg 선택

```bash
? Choose MSG : (Use arrow keys)
 » 26 : SCALED_IMU
   27 : RAW_IMU
   29 : SCALED_PRESSURE
   36 : SERVO_OUTPUT_RAW
   65 : RC_CHANNELS
   116 : SCALED_IMU2
```

### 6. 결과 확인

```bash
[COM3 57600] Connected!
[11785992, -56, 305, 987, -1006, -487, 518, 0, 0, 0, 0]
[11786093, -65, 300, 973, 365, -152, -121, 0, 0, 0, 0]
[11786194, -62, 301, 973, 182, -243, -91, 0, 0, 0, 0]
[11786295, -60, 299, 972, 213, -213, -30, 0, 0, 0, 0]
[11786397, -63, 299, 970, 182, -182, -121, 0, 0, 0, 0]
[11786497, -64, 300, 970, 60, -182, -213, 0, 0, 0, 0]
[11786598, -63, 302, 974, 60, -274, -152, 0, 0, 0, 0]
[11786699, -62, 299, 972, 152, -152, -91, 0, 0, 0, 0]
```

- `s`를 눌러 msg 변경 가능
- `q`를 눌러 종료

log 폴더에 로그가 생성됨.