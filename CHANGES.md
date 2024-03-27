# Change Log

## v0.3.25

Feature

- Optimize sentry channels and databases (#182)
- Split using logger name and process name for sentry

## v0.3.24

Fix

- Multiple imports for channels and databases

## v0.3.23

Feature

- Add common logger for non-sentry processes

## v0.3.22

Feature

- Add new logger for dispatcher and spawned processes

## v0.3.21

Feature

- Use sentinel logger for all components
- Add verification logic for channels and databases activation

## v0.3.20

Fix

- Add name for StandardABISignature database

## v0.3.19

Feature

- vars parameters/file support

## v0.3.18

Feature

- Auto group id for kafka inbound (transaction) channels

Documentation

- remove default kafka parameters for doc

## v0.3.17

Feature

- Apply new channel ids for examples
- Add project profiles
- Add label to project components
- Add inventory feature to track inputs, outputs and databases in a project

Refactoring

- Refactoring example profiles
- Remove outdated profiles

Migration 

- Migrate examples code to sentry code base

## v0.3.16

Feature

- Migrate balance monitor to sentry
- Migrate block detector to sentry
- Migrate transaction detector to sentry
- Migrate examples to new configuration
- Implement new Sentry core + new configuration
- Add dry-run option for launch command

Documentation

- Update docs according to latest changes

## v0.3.15

Feature

- Add core sentry process
- Add async core sentry process
- Remove prefix for main process
- Handle comments in profiles
- Add dry-run option for launch command
- Update balance monitor for eth/bsc
- Add ERC20 for balance monitor

Documentation

- Add article how to get transaction data

Fix

- Handling empty lines in fetch commands (#143)
- Next dev version Github pipeline

## v0.3.14

Feature

- Add detector name as URI in logs
- Add blockchain definitions as part of SDK

Fix

- Release pipeline bump release version automatically
- Fix chain_id in balance monitor

## v0.3.10

Feature

- Migrate to new command line interface for handling commands
- Add Sentinel version command and update documentation
- Add profiles for HAI Bridge in the balance monitor 
- Add local address db details in Sentinel log
- Add project settings and templates
- Add detector templates
- Add handling default Kafka parameters: auto_offset_reset
- Add local address database as part of Sentinel SDK
- Add in-memory address db

Refactoring

- Update/refactor balance monitor code
- Move utils code from different locations to one place utils/

Fix

- Remove auto_offset_reset parameter as it used latest by default + fix event channel definition
- Group id in examples/balance_monitor

## v0.3.9

Feature

- Add import service tokens
- Updates for debugging and error handling Event HTTP Channel

Refactoring

- Remove unused packages in dev scripts

Fix

- dev scripts for working with virtenv

Documentation

- Update installation intructions for prev python versions (Ubuntu 20.04 LTS)

## v0.3.8

Feature

- re-org release and merge pipelines
- automatic bumping version for release and dev merge

## v0.3.7

Feature

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

Refactoring

- remove unused import

## v0.3.5

- Add virtual env support for local development, dev scripts: /scripts
- Decrease required python version to 3.10
- Update Doc and profiles to run quickly 

## v0.3.4

- add websocket channel support, common one + transactions
