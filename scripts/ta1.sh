#!/usr/bin/env bash

cd services/knowledge-middleware
MOCK_TA1=FALSE poetry run poe report
cd ../..
poetry run poe upload-ta1