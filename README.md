# NALDA_backend_serial_cli

> FC Firmware는 다음 [[Github] STM32-FC](https://github.com/NARAE-INHA-UNIV/STM32-FC)를 참고하세요.

STM32-FC 데이터 읽기 & 파라미터 수정을 위한 CLI 프로그램

## 실행 방법

1. 패키지 설치 (최초 1회만)

```bash
pip isntall pyserial questionary keyboard
```

2. 실행

```bash
python main.py
```

3. FC가 연결된 포트 선택 (화살표 키로 이동, Enter로 선택)

```bash
# 아래에 나오는 포트 목록은 컴퓨터마다 다를 수 있습니다.
Choose Serial Port: (Use arrow keys)
   /dev/cu.debug-console - n/a
   /dev/cu.wlan-debug - n/a
 » /dev/cu.Bluetooth-Incoming-Port - n/a
```

4. Baud rate 선택

```bash
Choose baudrate : (Use arrow keys)
   9600
 » 57600
   115200
   (input)
```


- USB CDC 연결인 경우, 아무 값 입력
- Telem 단자인 경우 설정한 값 입력. 일반적으로 **57600**(MAVLink), 115200(Others)임.

5. 확인할 msg 선택


6. 결과 확인

- `s`를 눌러 msg 변경 가능
- `q`를 눌러 종료
