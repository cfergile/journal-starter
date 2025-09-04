import http from 'k6/http';
import { sleep, check } from 'k6';

export const options = {
  vus: 5,
  duration: '30s',
  thresholds: {
    http_req_failed: ['rate==0'],      // no failures
    http_req_duration: ['p(95)<800'],  // p95 under 800ms
  },
};

const BASE_URL = __ENV.BASE_URL || 'https://journal-starter.onrender.com';

export default function () {
  const res = http.get(`${BASE_URL}/healthz`);
  check(res, { 'status is 200': r => r.status === 200 });
  sleep(1);
}
