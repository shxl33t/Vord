# vord — TODO melhorias

## Suporte iOS (iPhone/iPad)
- [ ] Captura via `idevicescreenshot` (libimobiledevice) ou `xcrun simctl` (simulador)
- [ ] Deteccao automatica: se serial parece UDID (40 hex) usa iOS, senao Android
- [ ] Fallback: `pymobiledevice3` (Python puro, sem dependencia de brew/apt)
- [ ] Tratar tela preta do iOS (equivalente ao FLAG_SECURE — apps bancarios usam `UIScreen.isCaptured`)

## Multi-device
- [ ] Aceitar lista de serials (Android + iOS misturados)
- [ ] Uma thread por device, screenshots em subpastas `screens/{serial}/`
- [ ] Log unificado com coluna de device

## Captura inteligente
- [ ] OCR basico (pytesseract) pra logar texto visivel da tela (titulos, botoes, erros)
- [ ] Detectar e ignorar telas de transicao/loading (hamming instavel por >3 ciclos)
- [ ] Modo burst: quando detecta tela nova, capturar 3x rapido (0.5s) pra pegar animacoes
- [ ] Agrupar screenshots por app/activity (usar `dumpsys activity` no Android, `idevicesyslog` no iOS)

## Correlacao com proxy
- [ ] Gravar epoch no nome do arquivo (ex: `auto-1720540800-143022.png`) pra match exato com o history do proxy
- [ ] Flag `--proxy-history` que consulta a REST API do proxy e anota no log qual request HTTP ocorreu no mesmo segundo
- [ ] Gerar timeline HTML com screenshots + requests lado a lado

## Qualidade de evidencia
- [ ] Redimensionar pra resolucao padrao (ex: 1080px largura) pra reports
- [ ] Adicionar borda + timestamp + device info como watermark automatico
- [ ] Modo `--annotate` que abre cada screenshot pra o operador adicionar caption antes de salvar
- [ ] Export em PDF (um screenshot por pagina, com caption e timestamp)

## Usabilidade
- [ ] `--duration 5m` pra rodar por tempo limitado e sair
- [ ] `--poll 1.0` pra customizar intervalo (default 2.5s)
- [ ] `--sensitivity low|medium|high` em vez de DIST_NEW/DIST_SETTLE numericos
- [ ] Notificacao sonora quando detecta tela SECURE (alerta pro operador)
- [ ] `--diff` mode: salvar tambem a imagem diff (highlight do que mudou entre telas)

## Resiliencia
- [ ] Reconectar automatico se adb/idevice desconecta (retry com backoff)
- [ ] Tratar rotacao de tela (landscape vs portrait) sem gerar falso positivo
- [ ] Watchdog: se nenhuma tela nova em X minutos, alertar (device travou? tela apagou?)
