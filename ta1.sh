#!/usr/bin/env bash

cd services/knowledge-middleware

make init

poetry run poe report

cd ../..

mkdir -p outputs/ta1

cp services/knowledge-middleware/tests/output/report*.json outputs/ta1