# Changelog

## v0.5.66

Feature

- Add sepolia network in definitions (#489)

## v0.5.65

Fix

- Typos in bytecode hash types (#487)

## v0.5.64

Feature

- Add options to select hash type for bytecode hash calculation (#485)

## v0.5.63

Fix

- Handling async web3 connection due to changes in web3 lib

## v0.5.62

Feature

- Add field validator for block field: total difficulty
- Add verification utils for models

Fix

- Transaction format handling (#481)

Test

- Add test model resources
- Add tests for transaction model
- Add tests for model utils

## v0.5.61

Feature

- Upgrade deps versions (#479)

Refactoring

- Code refactoring for standard abi signatures

## v0.5.60

Feature

- Upgrade aiohttp version to 3.10.11 (#477)
- Add ignore macos specific files
- Add descriptions for utils/address + add tests

Test

- Add tests for leading zero address handling (#476)

Fix

- Normalize_address function to preserve significant leading zeros in Ethereum addresses (#475)


## v0.5.59

Fix

- Fix none proxy address in monitoring config (#473)

Refactoring

- Code refactoring for remote monitoring conditions (#472)

## v0.5.58

Feature

- Make block.total_difficulty field optional in transaction model (#470)

## v0.5.57

Fix

- fix: ignore empty messages when consuming kafka records (#468)

## v0.5.56

Feature

- Support multi format detector schema versions (#465)
- Handling exact and main versions + error handling
- Error handling for incorrect main schema version and detector config version

Fix

- Error handling for corrupted data (#466)

Test

- Fix versioning in monitoring conditions db

## v0.5.55

Feature

- Support manifests with bug versions in one detector (#463)
- Add bugfix version check util
- Monitoring config support bugfix version(-s) for processing)
- Update UI schema automatically with last severity field (#461)
- Update manifest for monitored address tx monitor
- Use severity field in ui order as default behavior
- Add title and icon fields for manifest (#459)
- Update gitbook summary script and summary.md (#457)
- Add manifest fields: title and icon (#450)
- Handling delete events in monitoring configs (#448)
- Handling active/inactive config changes in monitoring config
- Use contact for detector source name
- Update balance monitor manifest for supporting us schema
- Update manifest to support ui schema field
- Add flat transaction models and documentaion (#447)
- Add handling proxy address for monitore contract (#441)
- Add UI schema for manifest (#439)
- Handling non author values in manifest (#434)
- Add ui schema annotations (#432)
- Move author field to metadata model and fix ui schema field name (#431)
- Log exception insufficient data bytes in filter events (#429)
- Change logging order for label db (#428)
- Add vechain transaction input (#421)
- Add vechain definitions
- Add transaction models for different chains
- Add basic test for vechain transaction
- Extend vechain transaction model and tests
- Add vechain transaction detector
- Add inbound vechain transaction channel
- Reorg static abi structure (#416)
- Add transparent proxy abi signatures (#412)
- Monitoring configs command (#411)
- Add abi signature search by hash and name
- Add config dn instead of target db
- Add config command instead of target command
- Add tests for monitoring configs
- Add remote monitoring config db
- Add connection error handling for http event
- Reorg static abi structure
- Remove duplicates
- Search abi signature by hash (#414)
- Sending adhoc events (#406)
- Add abi signature search by hash and name
- Add pytest-httx to dev requirements
- Add http event service
- Add tests for http events service
- Update dependencies
- Add manifest tag as string type (#404)
- Add financial tag for manifest (#402)
- Generate summary file in docs (#401)
- Apply gitbook structure and configuration (#395)
- Add tags and network tags (#393)
- Manifest get parameters handling (#391)
- Upgrade versions in pyproject and dev requirements (#374)
- Add status for failed manifest registration (#387)
- Add normalize address util and tests (#372)
- Add default value for receipt effective gas price (#370)
- Add shorten ethereum address (#368)
- Update sentry diagrams
- Update comments for remote monitoring conditions
- Add tags and network tags for detector manifest
- Add comments for monitoring condition database methods
- Add return type for method all() in local dex db

Test

- Add tests for manifest api to update ui schema (#462)
- Add py 3.12 and 3.13 for tests (#456)
- Support several sqlite versions (#455)
- Add abi event withdrawal filtering (#418)
- Update tests for handling transfer event with empty data
- Comment test filter events withdrawal
- Add tests for monitoring configs

Fix

- Add new sqlite version support (#458)
- Last time handling in monitoring conditions (#454)
- Handle null title field in manifest (#452)
- Handling null proxy address in monitoring contract db (#445)
- Handling empty addresses in monitoting address db (#443)
- Pass author value during manifest creation (#436)
- Handling empty data value in extract_data_from_event_log
- Add missed args for local monitored contract db (#426)
- Add from_settings method for local monitored contract db (#424)
- Versions in change log
- Remove skip 0x data block for event filter
- Versions in change log
- Add missed network tags during manifest registration (#408)
- Error handling during manifest registration (#389)

Refacroting

- Cosmetic changes in remote label db (#438)
- Add comments for evm transaction models
- Remove unused files
- Commit transaction logging
- Handling last time for monitoring conditions
- Change order of filtering monitoring configs

Documentation

- Update links to release notes (#398)
- SDK overview update (#396)
- Update data model details per databases (#386)
- Update trace details (#385)
- Update monitoring contract db (#384)
- Update monitoring contract details
- Update monitoring conditions db (#383)
- Update monitoring conditions database
- Update mixer database (#382)
- Update label database (#381)
- Update dex db (#380)
- Update dex address details
- Update contract db (#379)
- Update blacklist db details (#378)
- Update suspicious account db methods (#377)
- Fix refs to databases (#376)
- Add details about address db (#375)

## v0.5.54

Feature

- Add title and icon fields for manifest (#459)
- Update gitbook summary script and summary.md (#457)

Fix

- Last time handling in monitoring conditions (#454)

Test

- add py 3.12 and 3.13 for tests (#456)
- support several sqlite versions (#455)

## v0.5.53

Fix

- Handle null title field in manifest

## v0.5.52

Feature

- Add manifest fields: title and icon (#450)
- Changes in GitHub CI/CD workflows

## v0.5.51

Feature

- Handling inactive monitoring configs (#448)
- Add flat transaction models and documentaion (#447)

## v0.5.50

Fix

- Handling null proxy address in monitoring contract db (#445)

## v0.5.49

Fix

- Handling empty addresses in monitoting address db (#443)

## v0.5.48

Feature

- Add handling proxy address for monitore contract (#441)

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
