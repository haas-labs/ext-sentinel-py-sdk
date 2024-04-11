# Health check

A web service should answer a health check request with a simple response indicating its current operational status. The purpose of a health check is to provide a quick and easy way to determine if the service is functioning properly. Here are some common practices for how a web service should respond to a health check:

## HTTP Status Codes

Use HTTP status codes to indicate the status of the service. Common status codes include:

- 200 OK: Indicates that the service is healthy and operational.
- 503 Service Unavailable: Indicates that the service is temporarily unavailable or experiencing issues.

## Plain Text or JSON Response

Return a simple plain text or JSON response with a clear indication of the service's health status. For example:

- Plain text: "Service is healthy" or "Service is down".
- JSON: {"status": "healthy"} or {"status": "unhealthy"}.
- Response Time: Optionally, the health check response could include information about response time or other performance metrics. However, this is not strictly necessary for a basic health check.

## Consistent Endpoint

Use a consistent endpoint URL for health checks, such as /health or /status, to make it easy for monitoring tools to find and check the service's health.

## Minimal Dependencies

Ensure that the health check endpoint has minimal dependencies on other services or components to avoid false positives or negatives. The health check should primarily verify the availability and basic functionality of the service itself.

## Custom Checks

Depending on the complexity of the service, custom health checks can be implemented to verify specific components or dependencies (e.g., database connectivity, file system access, etc.).

## Authentication

Consider whether the health check endpoint should be protected by authentication. In many cases, it's left unprotected for ease of monitoring, but in secure environments, authentication may be necessary.

## Monitoring and Logging

Log health check requests and responses for monitoring and troubleshooting purposes. This helps in understanding the historical health of the service and diagnosing any issues that arise.
