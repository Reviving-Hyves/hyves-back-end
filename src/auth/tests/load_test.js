import http from "k6/http";
import { check, sleep } from "k6";

export let options = {
  stages: [
    { duration: "30s", target: 5 },
    { duration: "1m", target: 5 },
    { duration: "30s", target: 0 },
  ],
  thresholds: {
    http_req_duration: ["p(95)<500"],
  },
};

const API_TOKEN = "Bearer [Token here]";
const REMOTE_ADDRESS = "http://localhost:8002"; // Without trailing slash

export default function () {
  let payload_login = JSON.stringify({
    username: "nickw",
    password: "nick",
  });
  let getResponse = http.post(
    REMOTE_ADDRESS + "/api/auth/login",
    payload_login,
    {
      headers: {
        "Content-Type": "application/json",
      },
    },
  );

  check(getResponse, {
    "GET /api/auth/login status is 200": (r) => r.status === 200,
    "GET /api/auth/login response time < 500ms": (r) =>
      r.timings.duration < 500,
  });

  let payload = JSON.stringify({
    first_name: "Nick",
    last_name: "Welles",
  });
  let postResponse = http.put(REMOTE_ADDRESS + "/api/auth/update", payload, {
    headers: {
      "Content-Type": "application/json",
      Authorization: API_TOKEN,
    },
  });

  check(postResponse, {
    "POST /api/auth/update status is 200": (r) => r.status === 200,
    "POST /api/auth/update response time < 500ms": (r) =>
      r.timings.duration < 500,
  });

  sleep(1);
}
