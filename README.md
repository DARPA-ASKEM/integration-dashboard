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
cp sample.env .env
# Change `.env` as needed
make up
```

### Options
- `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`: Standard credentials for reading and writing to S3
- `BUCKET`: The bucket you'd like to read and write to.
- `USE_LOCAL`: Read from the gitignore files in `output/ta*` instead of S3.

## Developing
To set up the project for development, run
```
make dev-init  
```

