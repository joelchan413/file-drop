#!/usr/bin/env sh
set -eu

CERT_DIR="${SSL_CERT_DIR:-/app/certs}"
CERT_FILE="${SSL_CERT_FILE:-$CERT_DIR/cert.pem}"
KEY_FILE="${SSL_KEY_FILE:-$CERT_DIR/key.pem}"
CERT_HOST="${SSL_CERT_HOST:-localhost}"
EXTRA_SANS="${SSL_EXTRA_SANS:-}"

mkdir -p "$CERT_DIR"

if [ ! -f "$CERT_FILE" ] || [ ! -f "$KEY_FILE" ]; then
  SAN_LIST="DNS:localhost,IP:127.0.0.1,DNS:${CERT_HOST}"

  if [ -n "$EXTRA_SANS" ]; then
    OLD_IFS="$IFS"
    IFS=','
    for san in $EXTRA_SANS; do
      trimmed="$(echo "$san" | sed 's/^ *//;s/ *$//')"
      [ -z "$trimmed" ] && continue
      case "$trimmed" in
        *[!0-9.]* ) SAN_LIST="${SAN_LIST},DNS:${trimmed}" ;;
        * ) SAN_LIST="${SAN_LIST},IP:${trimmed}" ;;
      esac
    done
    IFS="$OLD_IFS"
  fi

  openssl req -x509 -nodes -newkey rsa:2048 \
    -keyout "$KEY_FILE" \
    -out "$CERT_FILE" \
    -days 3650 \
    -subj "/CN=${CERT_HOST}" \
    -addext "subjectAltName=${SAN_LIST}"
fi

exec uvicorn main:app \
  --host 0.0.0.0 \
  --port "${PORT:-8000}" \
  --ssl-keyfile "$KEY_FILE" \
  --ssl-certfile "$CERT_FILE"
