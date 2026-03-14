# Judge Task — Loop 1

## Score: 6.5/10

## Task

Implement a working perceive→decide→act loop in the backend (apps/api/) with at least one endpoint that demonstrates autonomy. Write test cases for this endpoint and ensure they pass. Also, implement real Airia platform integration with webhook/export functionality.

## Blocking Issues

- [CRITICAL] Backend not running, no endpoints available — Fix: Check the backend setup in apps/api/ and ensure it's properly configured to run on http://127.0.0.1:8090
- [CRITICAL] No tests are being executed — Fix: Add test cases in the backend (apps/api/) and ensure they can be run with pytest. Fix any syntax errors in the test command.
- [HIGH] No evidence of Airia platform integration beyond README mention — Fix: Implement real webhook/export functionality that Airia can call in the backend (apps/api/). Add test cases to verify this.
- [HIGH] No evidence of a working perceive→decide→act loop — Fix: Implement and document an autonomous agent loop in the backend (apps/api/). Add test cases to verify this functionality.
