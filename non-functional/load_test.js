import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
    executor: 'constant-vus',
    vus: 100,
    duration: '30s',
}

export default function () {
    let res = http.get('https://www.xenonstack.com/');

    check(res, {
        'Load Test: Status is 200': (r) => r.status === 200,
        'Load Test: Response time < 3s': (r) => r.timings.duration < 3000,
    });

    sleep(1);
}
