// /non-functional/spike_test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
    stages: [
        { duration: '5s', target: 10 },
        { duration: '10s', target: 300},
        { duration: '10s', target: 300 },
        { duration: '5s', target: 10 },
    ],
};

export default () => {
    let res = http.get('https://www.xenonstack.com/');

    check(res, {
        'Spike Test: Status is 200': (r) => r.status === 200,
        'Spike Test: Response time < 10s': (r) => r.timings.duration < 10000,
    });
    sleep(1);
}
