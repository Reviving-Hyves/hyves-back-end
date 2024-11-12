import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
    stages: [
        { duration: '30s', target: 10 },
        { duration: '1m', target: 10 },
        { duration: '30s', target: 0 },
    ],
    thresholds: {
        http_req_duration: ['p(95)<500'],
    },
};

const API_TOKEN = 'Bearer [Token]';

export default function () {
    let getResponse = http.get('http://localhost:8003/api/post/list/', {
        headers: {
            Authorization: API_TOKEN,
        },
    });

    check(getResponse, {
        'GET /api/post/list/ status is 200': (r) => r.status === 200,
        'GET /api/post/list/ response time < 500ms': (r) => r.timings.duration < 500,
    });

    let payload = JSON.stringify({ author_id: 1, content: 'Load testing post' });
    let postResponse = http.post('http://localhost:8003/api/post/create/', payload, {
        headers: {
            'Content-Type': 'application/json',
            Authorization: API_TOKEN,
        },
    });

    check(postResponse, {
        'POST /api/posts/create status is 201': (r) => r.status === 201,
        'POST /api/posts/create response time < 500ms': (r) => r.timings.duration < 500,
    });

    sleep(1);
}
