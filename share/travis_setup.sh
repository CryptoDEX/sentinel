#!/bin/bash
set -evx

mkdir ~/.cryptodexcore

# safety check
if [ ! -f ~/.cryptodexcore/.cryptodex.conf ]; then
  cp share/cryptodex.conf.example ~/.cryptodexcore/cryptodex.conf
fi
