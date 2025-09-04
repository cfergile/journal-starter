import http from 'k6/http';
import { check, group, sleep, fail } from 'k6';
import { Rate } from 'k6/metrics';

export const options = {
  vus: 3,
  iterations: 3, // one CRUD cycle per VU
  thresholds: {
    unexpected_error_rate: ['rate==0'], // no unexpected HTTP statuses
    http_req_duration: ['p(95)<1000'],  // p95 < 1s
  },
};

// ------- Safety: default to NON-PROD; refuse prod unless allowed -------
const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';
const ALLOW_PROD = ( __ENV.ALLOW_PROD || 'false' ).toLowerCase() === 'true';
if (BASE_URL.includes('onrender.com') && !ALLOW_PROD) {
  throw new Error(
    `Refusing to run against production (${BASE_URL}). ` +
    `Set ALLOW_PROD=true if you really intend to run on prod.`
  );
}

const CLEAN_OLD = ( __ENV.CLEAN_OLD || 'true' ).toLowerCase() === 'true';
const jsonHeaders = { headers: { 'Content-Type': 'application/json' } };

// custom metric: only count statuses we *didn't* expect as errors
const unexpected_error_rate = new Rate('unexpected_error_rate');
function record(res, okStatuses = [200]) {
  const ok = okStatuses.includes(res.status);
  unexpected_error_rate.add(ok ? 0 : 1);
  return ok;
}

function marker() {
  return `k6-smoke-${__VU}-${__ITER}-${Date.now()}`;
}

export default function () {
  const mk = marker();
  let createdId = null;

  group('entries CRUD', () => {
    // CREATE
    const createRes = http.post(
      `${BASE_URL}/entries/`,
      JSON.stringify({ work: `k6 create ${mk}`, struggle: 'testing with k6', intention: 'verify CRUD' }),
      jsonHeaders
    );
    check(createRes, {
      'create: 2xx': (r) => record(r, [200, 201]),
      'create: has id': (r) => (r.json('id') ?? null) !== null,
    }) || fail(`Create failed: ${createRes.status} ${createRes.body}`);
    createdId = createRes.json('id');

    // READ (GET by id)
    const getRes = http.get(`${BASE_URL}/entries/${createdId}`);
    check(getRes, {
      'get: 200': (r) => record(r, [200]),
      'get: id matches': (r) => r.json('id') === createdId,
      'get: work contains marker': (r) => String(r.json('work') || '').includes(mk),
    });

    // UPDATE
    const putRes = http.put(
      `${BASE_URL}/entries/${createdId}`,
      JSON.stringify({ work: `k6 update ${mk}`, struggle: 'testing with k6 (updated)', intention: 'verify update' }),
      jsonHeaders
    );
    check(putRes, {
      'update: 200': (r) => record(r, [200]),
      'update: work updated': (r) => String(r.json('work') || '').includes('k6 update'),
    });

    // LIST
    const listRes = http.get(`${BASE_URL}/entries/`);
    check(listRes, {
      'list: 200': (r) => record(r, [200]),
      'list: array': (r) => Array.isArray(r.json()),
      'list: contains our id': (r) => (r.json() || []).some((e) => e.id === createdId),
    });

    // DELETE
    const delRes = http.del(`${BASE_URL}/entries/${createdId}`);
    check(delRes, {
      'delete: 200/204': (r) => record(r, [200, 204]),
    });

    // VERIFY DELETED (404 is EXPECTED here)
    const getGone = http.get(`${BASE_URL}/entries/${createdId}`);
    check(getGone, {
      'get after delete: 404': (r) => record(r, [404]),
    });

    // Optional cleanup of any stale k6 entries from earlier failed runs
    if (CLEAN_OLD) {
      const all = listRes.status === 200 ? (listRes.json() || []) : [];
      for (const e of all) {
        if (typeof e?.work === 'string' && e.work.startsWith('k6 ')) {
          const r = http.del(`${BASE_URL}/entries/${e.id}`);
          record(r, [200, 204, 404]);
        }
      }
    }
  });

  sleep(0.5);
}
