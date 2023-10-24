import json
from functools import reduce
from collections import defaultdict

import streamlit as st

"""
# Integration Dashboard

This dashboard tracks the status of TA1-TA4 and TA3-TA4 integration by viewing
reports generated by TA4's [`knowledge-middleware`](https://github.com/DARPA-ASKEM/knowledge-middleware/)
and [`simulation-integration`](https://github.com/DARPA-ASKEM/simulation-integration).

Terarium regularly uploads new reports to S3. See [here](https://github.com/DARPA-ASKEM/simulation-integration) 
to add TA1 scenarios and [here](https://github.com/DARPA-ASKEM/simulation-integration) for TA3.
"""
    
