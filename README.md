# MiniLink_cli

> FC Firmware는 다음 [[Github] STM32-FC](https://github.com/NARAE-INHA-UNIV/STM32-FC)를 참고하세요.

STM32-FC 데이터 읽기 & 파라미터 수정을 위한 CLI 프로그램

## How to install

#### Requirement

- Python >= 3.10

### 1. Project Clone

```bash
git clone --recurse-submodules https://github.com/NARAE-INHA-UNIV/MiniLink_cli
cd MiniLink_cli
```

### 2. 패키지 설치 (최초 1회만)

```bash
pip install pyserial questionary pynput numpy
```

## How to run

### 1. 실행

```bash
python main.py
```

### 2. FC가 연결된 포트 선택

```bash
# 아래에 나오는 포트 목록은 컴퓨터마다 다를 수 있습니다.
 ? Choose Serial Port : (Use arrow keys)
 » COM3 - STMicroelectronics Virtual COM Port(COM3)
   a) EXIT
```

화살표 키로 이동, Enter로 선택

### 3. Baud rate 선택

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

```bash
[COM3 57600] Connected!
[MiniLink] loading messages list
```

문구가 나오면 연결되어 동작하고 있는 것이다.<br>
기본 값은 log 폴더에 로그가 생성된다.

### 4. 메뉴 선택

- `m` : 메뉴 열기
- `s` : message 변경
- `q` : 종료

```bash
? Choose MSG : (Use arrow keys)
 » 26 : SCALED_IMU
   27 : RAW_IMU
   29 : SCALED_PRESSURE
   36 : SERVO_OUTPUT_RAW
   65 : RC_CHANNELS
   116 : SCALED_IMU2
```

### 5. 결과 확인

```bash
$ python main.py
? Choose Serial Port : COM3 - STMicroelectronics Virtual COM Port(COM3)
? Choose baudrate : 57600
[COM3 57600] Connected!
[MiniLink] loading messages list
? MENU : s) Change message
? Choose MSG : 26 : SCALED_IMU
['time_boot_ms', 'xacc', 'yacc', 'zacc', 'xgyro', 'ygyro', 'zgyro', 'xmag', 'ymag', 'zmag', 'temperature']
[352085, -62, 308, 972, 60, -274, -60, 0, 0, 0, 0]
[352187, -62, 307, 969, 121, -274, -60, 0, 0, 0, 0]
[352287, -62, 306, 972, 152, -213, -60, 0, 0, 0, 0]
[352388, -65, 305, 970, 152, -243, -60, 0, 0, 0, 0]
[352489, -60, 305, 969, 182, -335, -60, 0, 0, 0, 0]
```

## How to update

```bash
git pull
git submodule update --remote
```
 
