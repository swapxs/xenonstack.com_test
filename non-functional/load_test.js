// /non-functional/load_test.js
import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
    executor: 'constant-vus',
    vus: 100,
    duration: '30s',
    thresholds: {
        http_req_duration: ["p(95)<5000"],
        http_req_failed: ["rate<0.01"],
    }
}

export default function () {
    let res = http.get('https://www.xenonstack.com/');

    check(res, {
        'Load Test: Status is 200': (r) => r.status === 200,
        'Load Test: Response time < 10s': (r) => r.timings.duration < 10000,
    });

    sleep(1);
}
