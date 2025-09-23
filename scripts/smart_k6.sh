#!/usr/bin/env bash
set -euo pipefail

PORT="${PORT:-8000}"
HOST="${HOST:-0.0.0.0}"
APP_MODULE="${APP_MODULE:-app.main:app}"
BASE_URL_DEFAULT="http://localhost:${PORT}"

# Default & sanitize BASE_URL
BASE_URL="${BASE_URL:-$BASE_URL_DEFAULT}"
if [[ -z "${BASE_URL}" || "${BASE_URL}" == "-e" ]]; then
  BASE_URL="$BASE_URL_DEFAULT"
fi

wait_health() {
  for _ in {1..120}; do
    curl -fsS "${BASE_URL}/healthz" >/dev/null 2>&1 && return 0
    sleep 0.3
  done
  return 1
}

if ! lsof -tiTCP:${PORT} -sTCP:LISTEN >/dev/null 2>&1; then
  echo "▶️  Starting app on ${HOST}:${PORT}"
  uvicorn "${APP_MODULE}" --host "${HOST}" --port "${PORT}" &
  APP_PID=$!
  trap 'kill ${APP_PID}' EXIT
  BASE_URL="$BASE_URL_DEFAULT"
  echo "⏳ Waiting for ${BASE_URL}/healthz ..."
  wait_health || { echo "❌ Server failed health check at ${BASE_URL}/healthz"; exit 1; }
else
  echo "🔁 Reusing existing server on :${PORT}"
  BASE_URL="$BASE_URL_DEFAULT"
  echo "⏳ Waiting for ${BASE_URL}/healthz ..."
  wait_health || { echo "❌ Existing server on :${PORT} failed health check at ${BASE_URL}/healthz"; exit 1; }
fi

echo "🚦 Running k6 (BASE_URL=${BASE_URL}) ..."
BASE_URL="${BASE_URL}" k6 run k6/entries_crud.js
