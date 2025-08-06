# Redis Cloud Setup Guide for AI Challenge

## Step 1: Create Redis Cloud Instance

1. Visit: https://redis.com/try-free/
2. Sign up for free Redis Cloud account
3. Create new subscription (Free tier available)
4. Create database with these specifications:

### Required Configuration:
- **Cloud Provider**: AWS/GCP/Azure (your choice)
- **Region**: Choose closest to your location
- **Memory**: 30MB (free tier) or higher
- **Modules Required**:
  - ✅ RedisSearch
  - ✅ RedisTimeSeries
  - ✅ RedisJSON (optional but recommended)

### After Creation:
- Note down: Host, Port, Password
- Default username is usually 'default'
- SSL is enabled by default

## Connection Details Format:
```
Host: redis-12345.c1.us-east-1-1.ec2.cloud.redislabs.com
Port: 12345
Password: your-generated-password
Username: default
SSL: True
```
