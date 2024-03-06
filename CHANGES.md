# Change Log

## v0.3.8

Features:

- re-org release and merge pipelines
- automatic bumping version for release and dev merge

## v0.3.7

Fetures:

- Githib integration with AWS Code Artifact
- Sending events from process init
- Impovements for balance monitor
- Dev script `install`: split installation part on deployment, dev-tools, sentinel
- Disable file channel buffering (by default)

Documentation

- Add settings section
- Update installation instructions
- Update deployment instructions

Fix

- Update dev scripts to deploy new dev environment 
- Handling a connection close issue for websocket channel
- Timestamp issue during migration to new transaction data source

Refactoring

- Tests refactoring for common process
- Code changes related to channel, output and database types

## v0.3.6

Feature

- http events publishing verification
- add event publishing verification
- service tokens detection
- add sentinel sdk version handling
- remove requirements to import service tokens
- add services.service_account as standalone command
- events http/rest channel
- add decimals to see full Eth values in balance monitor
- detect incomplete blocks in block detectors
- workaround for macos with multiprocessing issue
- add default values for transaction format
- support new transaction format
- add scripts/wscat for debugging websocket interface
- add user-defined init process per detector
- add docker image for balance monitor
- update dev scripts for cleaning repo

Fix

- timestamp issue for event in balance monitor
- addr to monitored contract for balance monitor event
- typos in profiles
- update metadata propertry
- profile parameters renaming
- handling empty and case-sensitive addresses in balance monitor
- fix web3 multiprocessing issue

Documentation

- update senitinel command arguments
- add detectors details
- update installation instructions
- add details about local dev setup 

Refactoring:

- remove unused import

## v0.3.5

- Add virtual env support for local development, dev scripts: /scripts
- Decrease required python version to 3.10
- Update Doc and profiles to run quickly 

## v0.3.4

- add websocket channel support, common one + transactions
