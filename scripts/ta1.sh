#!/usr/bin/env bash

cd services/knowledge-middleware
MOCK_TA1=FALSE poetry run poe report
cd ../..
mkdir -p outputs/ta1
cp services/knowledge-middleware/tests/output/report*.json outputs/ta1
poetry run poe upload-ta1