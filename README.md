# STP Decision Lab

Streamlit teaching lab for BSAD 350. Monday mode is a fictional, deterministic four-round exercise; Wednesday mode is a simple user-entered planning workspace. All scenarios stay in session memory; there is no shared database, analytics, login, or submission system. Download before refreshing or disconnecting. Do not enter sensitive information.

## Run locally

Python 3.10–3.12 recommended. In this folder:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the address printed in the terminal. Run tests with `python -m unittest discover -s tests`.

## Deploy for Moodle

Put this folder in a GitHub repository, then create a Streamlit Community Cloud app pointing to `app.py` and the repository's branch. Set access to public if appropriate; copy the verified app URL into a Moodle URL resource. Students need only a browser, not a ChatGPT account. Hosting and account policies may change; verify accessibility in a private browser before class. No deployment or live URL is included here.

## Classroom operation and limitations

Each browser connection has independent Streamlit session state, with no server-side shared writes. A refresh, disconnect, host restart, or reset can lose decisions; downloads are local to the student. Scaling depends on host capacity, network and concurrent sessions. Before class, exercise the deployed URL from multiple devices, including the intended class size, and verify downloads; the included automated isolation test does not substitute for host load testing. Keep a backup discussion activity. The workspace has no automatic citation verification, persistence, authentication, grading, shared instructor dashboard, or actual market data. Wednesday comparisons require comparable units and periods and credible research. Extend the separate `model.py` and mode navigation to add labs or a future portal.
