# vord

[English](#english) · [Português (pt-BR)](#português-pt-br)

---

## English

Automatic screen change detector for mobile pentesting. Captures a screenshot whenever the device screen changes, detects FLAG_SECURE/isCaptured protected screens, and logs everything with timestamps so you can correlate screens with proxy traffic (Burp, mitmproxy) afterwards.

### Features

- Automatic screenshot on screen change (perceptual hash + Hamming distance)
- FLAG_SECURE detection (Android): logs protected screens without crashing
- TSV log with timestamps, dhash, window focus, and file paths
- Lightweight polling (2.5s default)
- Timestamped log for correlation with a proxy's HTTP history

### Requirements

```
pip install Pillow
```

ADB must be installed and the device connected (USB or WiFi).

### Usage

```bash
# Uses the single connected device
./run-vord.sh

# Specific device serial (adb devices)
./run-vord.sh SERIAL

# Device over WiFi (replace DEVICE_IP)
./run-vord.sh DEVICE_IP:5555

# Direct Python
python3 vord.py [SERIAL]
```

Screenshots are saved to `screens/auto-HHMMSS.png` and logged in `screens/vord-log.tsv`.

### Output

```
[*] vord ativo (serial=auto). Ctrl-C pra sair.
[11:49:01] NOVA TELA -> auto-114901.png  com.example.app/.LoginActivity
[11:50:15] tela SECURE (sem captura)  com.example.app/.PaymentActivity
[11:51:03] NOVA TELA -> auto-115103.png  com.example.app/.HomeActivity
```

### Roadmap

See [TODO.md](TODO.md) for planned improvements (iOS support, multi-device, OCR, proxy correlation, etc).

---

## Português (pt-BR)

Detector automático de troca de tela para pentest mobile. Captura um screenshot sempre que a tela do device muda, detecta telas protegidas por FLAG_SECURE/isCaptured, e registra tudo com timestamp pra você correlacionar as telas com o tráfego de um proxy (Burp, mitmproxy) depois.

### Funcionalidades

- Screenshot automático na troca de tela (perceptual hash + distância de Hamming)
- Detecção de FLAG_SECURE (Android): registra as telas protegidas sem quebrar
- Log TSV com timestamp, dhash, foco da janela e caminho dos arquivos
- Polling leve (2.5s por padrão)
- Log com timestamp pra correlacionar com o histórico HTTP de um proxy

### Requisitos

```
pip install Pillow
```

ADB instalado e o device conectado (USB ou WiFi).

### Uso

```bash
# Usa o único device conectado
./run-vord.sh

# Serial específico (adb devices)
./run-vord.sh SERIAL

# Device por WiFi (troque DEVICE_IP)
./run-vord.sh DEVICE_IP:5555

# Python direto
python3 vord.py [SERIAL]
```

Os screenshots vão pra `screens/auto-HHMMSS.png` e o log pra `screens/vord-log.tsv`.

### Saída

```
[*] vord ativo (serial=auto). Ctrl-C pra sair.
[11:49:01] NOVA TELA -> auto-114901.png  com.example.app/.LoginActivity
[11:50:15] tela SECURE (sem captura)  com.example.app/.PaymentActivity
[11:51:03] NOVA TELA -> auto-115103.png  com.example.app/.HomeActivity
```

### Roadmap

Veja o [TODO.md](TODO.md) pros próximos passos (suporte iOS, multi-device, OCR, correlação com proxy, etc).
