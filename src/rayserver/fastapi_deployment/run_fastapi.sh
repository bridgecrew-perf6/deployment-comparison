#!/bin/bash
ray stop
ray start --head
python deploy_fastapi.py
python fastapi_client.py
ray stop