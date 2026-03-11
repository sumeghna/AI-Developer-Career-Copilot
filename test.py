
import os
from github import Github

token = os.environ.get('GITHUB_TOKEN')
print(f"Token found: {bool(token)}")
if token:
    print(f"Token length: {len(token)}")
    print(f"First 4 chars: {token[:4]}...")
    try:
        g = Github(token)
        user = g.get_user()
        print(f"✅ Success! Authenticated as: {user.login}")
    except Exception as e:
        print(f"❌ GitHub error: {e}")
else:
    print("❌ GITHUB_TOKEN environment variable is not set.")