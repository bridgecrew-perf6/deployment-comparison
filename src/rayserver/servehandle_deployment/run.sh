#!/bin/bash
ray stop
ray start --head
python deploy.py
python router_client.py
ray stop
