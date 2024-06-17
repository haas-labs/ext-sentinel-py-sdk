# Changelog

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
