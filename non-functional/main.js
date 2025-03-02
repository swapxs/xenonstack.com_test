import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
    scenarios: {
        load_test: {
            executor: 'constant-vus',
            vus: 100,
            duration: '1m',
            exec: 'loadTest',
        },

        stress_test: {
            executor: 'ramping-vus',
            stages: [
                { duration: '2m', target: 50 },
                { duration: '3m', target: 500 },
                { duration: '2m', target: 50 },
            ],
            exec: 'stressTest',
            startTime: '1m',
        },

        spike_test: {
            executor: 'ramping-vus',
            stages: [
                { duration: '30s', target: 10 },
                { duration: '10s', target: 1000 },
                { duration: '1m', target: 1000 },
                { duration: '30s', target: 10 },
            ],
            exec: 'spikeTest',
            startTime: '6m',
        },

        api_load_test: {
            executor: 'constant-vus',
            vus: 200,
            duration: '1m',
            exec: 'apiLoadTest',
            startTime: '9m',
        },

        resilience_test: {
            executor: 'constant-vus',
            vus: 50,
            duration: '2m',
            exec: 'resilienceTest',
            startTime: '11m',
        },
    },
};

// -------------------- TEST CASE FUNCTIONS --------------------

// 1. Load Test: Home Page Performance
export function loadTest() {
    let res = http.get('https://www.xenonstack.com/');
    check(res, {
        'Load Test: Status is 200': (r) => r.status === 200,
        'Load Test: Response time < 3s': (r) => r.timings.duration < 3000,
    });
    sleep(1);
}

// 2. Stress Test: High Traffic Endurance
export function stressTest() {
    let res = http.get('https://www.xenonstack.com/');
    check(res, {
        'Stress Test: Status is 200': (r) => r.status === 200,
        'Stress Test: Response time < 5s': (r) => r.timings.duration < 5000,
    });
    sleep(1);
}

// 3. Spike Test: Sudden Traffic Surge
export function spikeTest() {
    let res = http.get('https://www.xenonstack.com/');
    check(res, {
        'Spike Test: Status is 200': (r) => r.status === 200,
        'Spike Test: Response time < 7s': (r) => r.timings.duration < 7000,
    });
    sleep(1);
}

// 4. API Load Test: Form Submission Load Handling
export function apiLoadTest() {
    let payload = JSON.stringify({
        firstname: "Test",
        lastname: "User",
        email: "test@example.com",
        contact: "1234567890",
        company: "XenonStack",
    });

    let params = {
        headers: { 'Content-Type': 'application/json' },
    };

    let res = http.post('https://www.xenonstack.com/api/form-submit', payload, params);
    check(res, {
        'API Load Test: Status is 200': (r) => r.status === 200,
        'API Load Test: Response time < 2s': (r) => r.timings.duration < 2000,
    });
    sleep(1);
}

// 5. Resilience Test: Network Failure Simulation
export function resilienceTest() {
    let res = http.get('https://www.xenonstack.com/', { timeout: '10s' });
    check(res, {
        'Resilience Test: Status is 200': (r) => r.status === 200,
        'Resilience Test: Response time < 10s': (r) => r.timings.duration < 10000,
    });
    sleep(2);
}

