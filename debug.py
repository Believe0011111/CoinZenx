import os
import sys

print("=" * 60)
print("🔍 DEBUGGING ENVIRONMENT VARIABLES")
print("=" * 60)

# Check all environment variables
print("\nAll environment variables:")
for key, value in os.environ.items():
    if 'TOKEN' in key.upper() or 'KEY' in key.upper():
        print(f"  {key} = {'*' * len(value)} (hidden)")
    else:
        print(f"  {key} = {value}")

# Check specifically for BOT_TOKEN
token = os.getenv('BOT_TOKEN')
if token:
    print(f"\n✅ BOT_TOKEN found! Length: {len(token)} characters")
    print(f"   First 5 chars: {token[:5]}...")
    print(f"   Last 5 chars: ...{token[-5:]}")
else:
    print("\n❌ BOT_TOKEN NOT FOUND in environment variables!")

print("=" * 60)
