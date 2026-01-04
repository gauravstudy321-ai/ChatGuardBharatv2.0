from database import init_db, register_user, login_user, save_scan, get_user_history
import os

# Clean up old db if exists
if os.path.exists("chatguard.db"):
    os.remove("chatguard.db")

print("1. Initializing DB...")
init_db()

print("2. Registering User...")
success = register_user("testuser", "password123")
if not success:
    print("❌ Registration failed")
    exit(1)

print("3. Logging in...")
user_id = login_user("testuser", "password123")
if not user_id:
    print("❌ Login failed")
    exit(1)
print(f"✓ User ID: {user_id}")

print("4. Saving Scan...")
save_scan(user_id, "GPT-4o", 4.5, 90.0, [{"test": "data"}])

print("5. Retrieving History...")
history = get_user_history(user_id)
if len(history) == 1:
    print("✓ History retrieved successfully")
    print(history)
else:
    print("❌ History lookup failed")

print("✅ ALL SYSTEMS GO")
