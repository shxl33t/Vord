#!/bin/bash
# Detector automatico de troca de tela. Rodar em terminal proprio, deixar aberto.
# Salva screenshots em screens/auto-*.png + screens/vord-log.tsv quando a tela muda.
cd "$(dirname "$0")"
exec python3 vord.py "$@"
