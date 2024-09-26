# Changelog

## v0.5.47

Feature

- Add UI schema for manifest (#439)
- Update balance monitor manifest for supporting us schema (examples/)

## v0.5.46

Feature

- Pass author value during manifest creation (#436)

## v0.5.45

Feature

- Handling non author values in manifest (#434)

## v0.5.44

Feature

- Add ui schema annotations (#432)
- Move author field to metadata model and fix ui schema field name (#431)

## v0.5.43

Feature

- Change logging order for label db (#428)

Fix

- Log exception insufficient data bytes in filter events (#429)


## v0.5.42

Fix

- Add missed args for local monitored contract db (#426)

## v0.5.41

Fix

- Add from_settings method for local monitored contract db (#424)

## v0.5.40

Feature

- Add VeChain transaction input (#421)
- Add VeChain definitions
- Add VeVhain transaction model and tests

## v0.5.39

Testing 

- Add abi event withdrawal filtering (#418)

## v0.5.38

Feature

- Reorg static abi structure (#416)
- Search abi signature by hash (#415)

## v0.5.37

Feature

- Add transparent proxy abi signatures (#412)
- Add connection error handling for http event

## v0.5.36

Fix

- Add missed network tags during manifest registration (#408)

## v0.5.35

Feature

- add pytest-httx to dev requirements
- add http event service and tests
- add tests for http events service
- update dependencies

## v0.5.34

Feature

- Add manifest tag as string type (#404)

## v0.5.33

Feature

- Add financial tag for manifest (#402)
- Generate summary file in docs (#401)

Documentation

- update links to release notes (#400)
- SDK overview update (#396)
- apply gitbook structure and configuration (#395)

## v0.5.32

Feature

- Add tags and network tags for detector manifest

Documentation

- update sentry diagrams

## v0.5.31

Feature

- Manifest get parameters handling

## v0.5.30

Fix

- Error handling for manifest registration

## v0.5.29

Feature

- Add status for failed manifest registration (#387)
- Upgrade versions in pyproject and dev requirements (#374)

Documentation

- Update database details

## v0.5.28

Feature

- Add normalize address util and tests (#372)

## v0.5.27

Feature

- Add default value for receipt effective gas price (#370)

## v0.5.26

Feature

- add shorten ethereum address (#368)

## v0.5.25 (Cumulative release)

Feature

- Add license
- Use requirements files for deployment and dev profiles
- Improve performance of removing outdated blocks (#347)
- Handle missed env vars required for manifest api (#346)
- Use token from env vars instead of generating new ones every time (#344)
- Add transaction log entries filter by ABI signatures (#343)
- Make tx_type and receipt_effective_gas_price fields optional (#341)
- Add telos chain to definition (#339)
- Add concurrency protection for publish and release Github workflows (#338)
- Core sentinel database (#336)
- Add monitoring target command
- Load env vars from SENTINEL_ENV_PROFILE
- Add new logic for handling manifest severity (#330)
- Use numeric severity for manifest (#329)
- Handling manifest status (#326)
- Connection error handling for manifest api (#325)
- Add filtering manifests by status
- increase deps and dev/deployment tools versions
- Add monitored target model (#316)
- Get address conditions return config only (#314)
- Add cid field for event message (#310)

Documentation

- Add data models (#362)
- Re-org documentation structure
- Add templates for detectors (#361)
- Add Obsidian support
- Update documentation for processes, transaction and block detectors (#354)
- Update channel details (#353)
- Update commands details (#352)
- Update bundle description
- Update sentry documentation (#348)

Fix

- Empty topics list issue
- double status in manifest api (#328)
- Fix manifest schema for tags field(#323)
- Increase kafka connection timeout for monitoring  conditions db (#317)
- Remove duplicates in monitoring conditions (#312)

## v0.5.24

Feature

- Add license
- Use requirements files for deployment and dev profiles

Documentation

- Add data models (#362)
- Re-org documentation structure
- Add templates for detectors (#361)
- Add Obsidian support
- Update documentation for processes, transaction and block detectors (#354)
- Update channel details (#353)
- Update commands details (#352)
- Update bundle description

## v0.5.23

Feature

- Improve performance of removing outdated blocks (#347)
- Handle missed env vars required for manifest api (#346)

Docs

- Update sentry documentation (#348)

## v0.5.22

Feature

- Use token from env vars instead of generating new ones every time (#344)
- Add transaction log entries filter by ABI signatures (#343)

## v0.5.21

Feature

- Make tx_type and receipt_effective_gas_price fields optional (#341)

## v0.5.20

Feature

- Add telos chain to definition (#339)
- Add concurrency protection for publish and release Github workflows (#338)

## v0.5.19

Feature

- Core sentinel database (#336)
- Add monitoring target command
- Load env vars from SENTINEL_ENV_PROFILE

Fix

- Empty topics list issue

## v0.5.18

Feature

- Add new logic for handling manifest severity (#330)
- Use numeric severity for manifest (#329)

Fix

- double status in manifest api (#328)

## v0.5.17

Feature

- Handling manifest status (#326)
- Connection error handling for manifest api (#325)

## v0.5.16

Feature

- Add filtering manifests by status

Fix

- Fix manifest schema for tags field(#323)

## v0.5.15

Feature

- increase deps and dev/deployment tools versions

## v0.5.14

Merge conflict release

## v0.5.13

Feature

- Add monitored target model (#316)

Fix

- Increase kafka connection timeout for monitoring  conditions db (#317)

## v0.5.12

Feature

- Get address conditions return config only (#314)

## v0.5.11

Fix

- Remove duplicates in monitoring conditions (#312)

## v0.5.10

Feature

- Add cid field for event message (#310)

## v0.5.9

Fix

- Missed kwargs in remote trace db constructor (#308)

## v0.5.8

Fix

- from settings method for remote trace db (#306)
- from settings method for contract and standard abi signatures db (#305)

## v0.5.7

Fix

- time to run handler in dispatcher (#303)

## v0.5.6

Fix

- from settings method for local address db (#301)

## v0.5.5

Fix

- Pass sentry name and hash parameters to db (#299)
- Update interval for remote monitored contract db (#298)
- Default value for metadata field in events channel (#297)

## v0.5.4

Fix

- Add from_setting method for address dbs (#295)
- Add from_setting method for label and mixer dbs (#294)

## v0.5.3

Fix

- Add from_setting method for inbound/outbound tx channel
- Parameters in remote monitored contract

## v0.5.2

Feature

- Add from_settings method for monitored contract db (#290)

## v0.5.1

Feature

- Monitoring conditions helpers (#288)
- Integrate monitoring conditions with channel (#287)
- Detector configuration from kafka topic (#285)
- Add manifest command for managing sentry schema and metadata

## v0.5.0

Feature

- Group metrics by type and name in formatter (#282)
- Publish dispatcher metrics (#281)
- Add utils for publishing metrics
- Use async publish metrics in outbound metrics channel
- Activate sentries status metrics for dispatcher
- Dispatcher processing status
- Local monitoring env (#280)
- Improve metrics server logging (#278)
- Add connection error handling to metric server
- Implement http interface for outbound metric channel (#276)
- Run web servers (metrics) as async task
- Activate metrics for example tx detector (#272)
- Update tx detector profile to new configuration
- Add from_settings method for inbound kafka transactions channel
- Metrics registry in outbound metrics channel (#269)
- Migrate tx and block detectors to core v2 (#268)
- Upgrade deps versions (#267)
- Integrate telemery with sentry process (#266)
- Add metrics server as sentry
- Add metrics handler
- Inbound and outbound metrics channel (#265)
- Common handler logic for async core sentry (#264)
- Add from_settings and stop_after features for channels
- Sentinel Core v2 features 

Fix

- Prometheus metrics formatter (#279)
- Handling metrics and publishing in prometheus format

Refactoring

- Remove outdated code
- Issue with healtheck and metrics (#273)
- Re-use logger and metrics queue
- Remove prev version of dispatcher
- Remove outdated parameters
- Deprecate load_project_settings()
- Code optimization for core v2 channels
