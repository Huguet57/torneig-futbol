# Error Handling Guide

This document outlines the standard error responses in the Soccer Tournament Management System API and provides guidance on handling and recovering from these errors.

## Error Response Format

All API errors follow a consistent format:

```json
{
  "detail": {
    "message": "Human-readable error message",
    "code": "ERROR_CODE",
    "params": {
      "param1": "value1",
      "param2": "value2"
    }
  }
}
```

## Common Error Codes

### Authentication Errors (4xx)
- `UNAUTHORIZED` (401): Missing or invalid authentication token
- `FORBIDDEN` (403): Insufficient permissions for the requested operation

### Resource Errors (4xx)
- `NOT_FOUND` (404): The requested resource does not exist
- `CONFLICT` (409): Resource state conflict (e.g., duplicate entry)
- `VALIDATION_ERROR` (422): Invalid input data

### Server Errors (5xx)
- `INTERNAL_ERROR` (500): Unexpected server error
- `SERVICE_UNAVAILABLE` (503): Service temporarily unavailable

## Error Recovery Strategies

### Authentication Errors
1. **Token Expiration (401)**
   - Automatically refresh the access token using the refresh token
   - If refresh fails, redirect to login

2. **Permission Issues (403)**
   - Check user roles and permissions
   - Request necessary permissions if possible

### Resource Errors
1. **Not Found (404)**
   - Verify the resource ID or parameters
   - Refresh the data to ensure latest state
   - Create the resource if appropriate

2. **Conflict (409)**
   - Refresh the resource to get the latest state
   - Merge changes if possible
   - Present conflict resolution UI if needed

3. **Validation (422)**
   - Check input data against schema
   - Display specific validation errors to user
   - Provide guidance on correct input format

### Server Errors
1. **Internal Error (500)**
   - Implement exponential backoff retry
   - Log error details for debugging
   - Display user-friendly error message

2. **Service Unavailable (503)**
   - Implement circuit breaker pattern
   - Queue requests for retry
   - Monitor service health endpoints

## Retry Strategies

### Exponential Backoff
For transient errors, implement exponential backoff:

```javascript
async function retryWithBackoff(operation, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await operation();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      const waitTime = Math.pow(2, i) * 1000;
      await new Promise(resolve => setTimeout(resolve, waitTime));
    }
  }
}
```

### Circuit Breaker
For service health management:

```javascript
class CircuitBreaker {
  constructor(failureThreshold = 5, resetTimeout = 60000) {
    this.failureCount = 0;
    this.failureThreshold = failureThreshold;
    this.resetTimeout = resetTimeout;
    this.state = 'CLOSED';
  }

  async execute(operation) {
    if (this.state === 'OPEN') {
      throw new Error('Circuit breaker is OPEN');
    }

    try {
      const result = await operation();
      this.failureCount = 0;
      return result;
    } catch (error) {
      this.failureCount++;
      if (this.failureCount >= this.failureThreshold) {
        this.state = 'OPEN';
        setTimeout(() => {
          this.state = 'CLOSED';
          this.failureCount = 0;
        }, this.resetTimeout);
      }
      throw error;
    }
  }
}
```

## Error Logging

All errors should be logged with the following information:
- Timestamp
- Error code
- Request details (URL, method, parameters)
- Stack trace (in development)
- User context (if available)
- Correlation ID

Example log format:
```json
{
  "timestamp": "2024-03-04T10:00:00Z",
  "level": "error",
  "error_code": "NOT_FOUND",
  "message": "Tournament not found",
  "request": {
    "method": "GET",
    "url": "/api/tournaments/123",
    "params": {"id": "123"}
  },
  "user_id": "user_abc",
  "correlation_id": "req_xyz"
}
```

## Monitoring and Alerts

Set up monitoring for:
1. Error rate by endpoint
2. Error rate by type
3. Average response time
4. Circuit breaker state changes
5. Authentication failure rate

Configure alerts for:
- Error rate exceeding threshold
- Multiple 5xx errors in short period
- Circuit breaker trips
- Authentication spike failures

## Best Practices

1. **Graceful Degradation**
   - Implement fallback behavior when possible
   - Cache previous successful responses
   - Show partial data when full data unavailable

2. **User Communication**
   - Display user-friendly error messages
   - Provide clear recovery actions
   - Indicate system status clearly

3. **Security Considerations**
   - Sanitize error messages in production
   - Don't expose internal system details
   - Log sensitive information securely 