"""
Debug script to test trial quota saving to R2.
Run this to see if quota is being saved correctly.
"""
import os
import json
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Check environment
print("=" * 60)
print("ENVIRONMENT CHECK")
print("=" * 60)
print(f"R2_ACCOUNT_ID: {'✓ Set' if os.getenv('R2_ACCOUNT_ID') else '✗ Not set'}")
print(f"R2_ACCESS_KEY_ID: {'✓ Set' if os.getenv('R2_ACCESS_KEY_ID') else '✗ Not set'}")
print(f"R2_SECRET_ACCESS_KEY: {'✓ Set' if os.getenv('R2_SECRET_ACCESS_KEY') else '✗ Not set'}")
print(f"R2_BUCKET_NAME: {os.getenv('R2_BUCKET_NAME', 'Not set')}")
print()

# Import services
from services.trial_quota import get_trial_quota_service, GLOBAL_DAILY_QUOTA
from services.r2_storage import get_r2_storage

print("=" * 60)
print("QUOTA SERVICE TEST")
print("=" * 60)

# Get service
quota_service = get_trial_quota_service()
print(f"KV Available: {quota_service._kv_available}")
print(f"Using Session Fallback: {quota_service._use_session_fallback}")
print()

# Get current status
print("Current quota status:")
status = quota_service.get_quota_status()
print(json.dumps(status, indent=2, default=str))
print()

# Try to consume quota
print("=" * 60)
print("TESTING QUOTA CONSUMPTION")
print("=" * 60)
print("Attempting to consume 1 quota for basic_1k...")

success = quota_service.consume_quota("basic", "1K", 1)
print(f"Consumption result: {'✓ Success' if success else '✗ Failed'}")
print()

# Check status again
print("Quota status after consumption:")
status_after = quota_service.get_quota_status()
print(json.dumps(status_after, indent=2, default=str))
print()

# Check R2 directly
print("=" * 60)
print("R2 DIRECT CHECK")
print("=" * 60)

r2 = get_r2_storage(user_id=None)
if r2.is_available:
    from datetime import datetime, timezone
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    key = f"quota/trial_quota_{today}.json"

    print(f"Checking R2 for key: {key}")

    try:
        response = r2._client.get_object(
            Bucket=r2.bucket_name,
            Key=key
        )
        data = json.loads(response["Body"].read().decode("utf-8"))
        print("✓ Found in R2:")
        print(json.dumps(data, indent=2))
    except r2._client.exceptions.NoSuchKey:
        print("✗ Not found in R2")
    except Exception as e:
        print(f"✗ Error reading from R2: {e}")
else:
    print("✗ R2 is not available")

print()
print("=" * 60)
print("DEBUGGING COMPLETE")
print("=" * 60)
