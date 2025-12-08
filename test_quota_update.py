"""
Test if quota updates work correctly in sequence.
This simulates multiple image generations.
"""
import os
import json
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

from services.trial_quota import get_trial_quota_service
from services.r2_storage import get_r2_storage

def check_r2_file():
    """Check current R2 file content."""
    r2 = get_r2_storage(user_id=None)
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    key = f'quota/trial_quota_{today}.json'

    try:
        response = r2._client.get_object(Bucket=r2.bucket_name, Key=key)
        data = json.loads(response['Body'].read().decode('utf-8'))
        return data
    except:
        return None

print("=" * 60)
print("TESTING SEQUENTIAL QUOTA UPDATES")
print("=" * 60)

qs = get_trial_quota_service()

# Check initial state
print("\n1. Initial state in R2:")
r2_data = check_r2_file()
if r2_data:
    print(f"   global_used: {r2_data.get('global_used', 0)}")
    print(f"   basic_1k: {r2_data.get('mode_usage', {}).get('basic_1k', 0)}")
else:
    print("   No file found")

# Simulate 5 generations
for i in range(1, 6):
    print(f"\n{i+1}. Simulating generation #{i}...")

    # Check quota before
    can_gen, reason, info = qs.check_quota("basic", "1K", 1)
    print(f"   Can generate: {can_gen}")
    if not can_gen:
        print(f"   Reason: {reason}")
        break

    # Consume quota
    success = qs.consume_quota("basic", "1K", 1)
    print(f"   Consume success: {success}")

    # Check R2 immediately after consume
    r2_data = check_r2_file()
    if r2_data:
        print(f"   R2 after consume: global_used={r2_data.get('global_used', 0)}, basic_1k={r2_data.get('mode_usage', {}).get('basic_1k', 0)}")

    # Small delay
    import time
    time.sleep(0.5)

print("\n" + "=" * 60)
print("FINAL STATE")
print("=" * 60)

# Final check
status = qs.get_quota_status()
print(f"Service says: global_used={status['global_used']}, basic_1k={status['modes']['basic_1k']['used']}")

r2_data = check_r2_file()
if r2_data:
    print(f"R2 file says: global_used={r2_data.get('global_used', 0)}, basic_1k={r2_data.get('mode_usage', {}).get('basic_1k', 0)}")
