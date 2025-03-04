// /non-functional/resileience_test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
    vus: 50,
    duration: '2m',
};


export default () => {
    let res = http.get('https://www.xenonstack.com/', { timeout: '10s' });
    check(res, {
        'Resilience Test: Status is 200': (r) => r.status === 200,
        'Resilience Test: Response time < 10s': (r) => r.timings.duration < 10000,
    });
    sleep(2);
}


