// /non-functional/stress_test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    stages: [
        { duration: '30s', target: 10 },
        { duration: '60s', target: 100 },
        { duration: '20s', target: 100 },
        { duration: '10s', target: 5 },
    ]
};

// 2. Stress Test: High Traffic Endurance
export default () => {
    let res = http.get('https://www.xenonstack.com/');
    check(res, {
        'Stress Test: Status is 200': (r) => r.status === 200,
        'Stress Test: Response time < 10s': (r) => r.timings.duration < 10000,
    });
    sleep(1);
}
