# Integration Dashboard

This dashboard provides the statuses of ASKEM's TA1 services.
Specifically, the dashboard indicates
- If an operation works with `knowledge-middleare`
- How long that operation takes to complete
- The quality of the outputs (not yet implemented)

Currently, the dashboard is testing `knowledge-middleware` integration
but other services and TAs might be checked in the future.

![TA1 Dashboard Screenshot](https://github.com/DARPA-ASKEM/integration-dashboard/assets/14170067/da57d762-6e22-4130-ad34-ff790ef590e2)


## Usage

To view the current status, start the [Streamlit](https://streamlit.io/) app
by running:
```
make up
```
Upon execution, you can pass the following environment variables (with `docker run` do `-e ENV_NAME='ENV_VAL'` for each variable).

- `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`: Standard credentials for reading and writing to S3
- `BUCKET`: The bucket you'd like to read and write to.


To set up the project for development, run
```
make dev-init  
```

To add a new report, run from [`knowledge-middleware`](https://github.com/DARPA-ASKEM/knowledge-middleware) (NOT THIS REPO)
```
# REMINDER: RUN THIS IN `knowledge-middleware`
poetry run poe report
```
This uploads a `report_{datetime}.json` to S3 which the dashboard reads
off of directly.


