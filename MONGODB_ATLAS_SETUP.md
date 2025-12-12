# MongoDB Atlas Setup Guide - Complete Instructions

This guide provides **step-by-step instructions** to configure MongoDB Atlas cloud database for the Smart Gesture-Controlled HCI System project.

---

## 📋 Prerequisites

- Email address (for MongoDB account)
- Internet connection
- Project files downloaded/cloned on your computer

---

## 🚀 Complete Setup Process

### Step 1: Create MongoDB Atlas Account

1. **Open your web browser** and navigate to:
   ```
   https://www.mongodb.com/cloud/atlas/register
   ```

2. **Sign Up Options:**
   - Option A: Sign up with **Google account** (fastest)
   - Option B: Sign up with **email address**
   
3. **If using email:**
   - Enter your email address
   - Create a strong password (min 8 characters)
   - Check "I agree to the Terms of Service and Privacy Policy"
   - Click **"Create your Atlas account"**

4. **Verify your email:**
   - Check your inbox for verification email
   - Click the verification link
   - Wait for redirect back to MongoDB Atlas

5. **Welcome Survey (optional):**
   - You can skip this by clicking "Skip" or answer the questions
   - Click "Finish"

---

### Step 2: Create Your First Project

1. **On Atlas Dashboard:**
   - You'll see "Create a project" or "New Project" button
   - Click it

2. **Name Your Project:**
   - Enter project name: **`GestureControlProject`** (or any name you prefer)
   - Click **"Next"**

3. **Add Members (optional):**
   - You can skip this step
   - Click **"Create Project"**

---

### Step 3: Create a FREE Cluster (Database Server)

1. **Build Your Cluster:**
   - Click **"Build a Database"** or **"Create"** button
   - You'll see different deployment options

2. **Choose FREE Tier:**
   - Select **"Shared"** (FREE tier)
   - Click **"Create"** under the FREE M0 option
   - **Important:** M0 tier gives you 512MB storage completely FREE

3. **Configure Cluster:**
   
   **Cloud Provider & Region:**
   - Provider: Choose **AWS**, **Google Cloud**, or **Azure** (all work fine)
   - Region: Choose region **closest to your location** for better performance
     - Example: For India, choose `Mumbai (ap-south-1)` or `Singapore (ap-southeast-1)`
     - For USA, choose any US region
     - For Europe, choose Europe regions
   - Look for regions with **"FREE TIER AVAILABLE"** label

   **Cluster Tier:**
   - Keep **M0 Sandbox** selected (FREE)
   - Shows: "512 MB Storage, Shared RAM"

   **Additional Settings (optional):**
   - Cluster Name: Keep default **`Cluster0`** or change if you want
   - MongoDB Version: Keep default (latest version)

4. **Create Cluster:**
   - Click **"Create Cluster"** button at bottom
   - Wait 3-5 minutes for cluster creation (you'll see a progress bar)
   - ☕ Take a coffee break!

---

### Step 4: Setup Database Security

#### 4.1: Create Database User

1. **Security Quickstart appears automatically** (if not, go to Security → Database Access)

2. **Authentication Method:**
   - Keep **"Password"** selected (default)

3. **Create User Credentials:**
   - **Username:** Enter a username (e.g., `admin`, `gestureuser`, `yourname`)
     - Remember this - you'll need it later!
   - **Password:** Click **"Autogenerate Secure Password"** button
     - **CRITICAL:** Click the **"Copy"** button to copy password
     - **Paste it somewhere safe** (Notepad, text file) - you'll need it!
   - Or manually create a password (at least 8 characters, mix of letters/numbers/symbols)

4. **Database User Privileges:**
   - Keep default: **"Built-in Role"** - **"Read and write to any database"**
   - This allows your app to read and write data

5. **Create User:**
   - Click **"Create User"** button
   - User appears in the list below

#### 4.2: Configure Network Access (IP Whitelist)

1. **Add IP Address:**
   - In the same quickstart modal, scroll down to "Where would you like to connect from?"
   - Or go to: Security → Network Access

2. **Choose Access Type:**
   
   **Option A: Allow from Anywhere (Recommended for Development)**
   - Click **"Add IP Address"** button
   - Click **"Allow Access from Anywhere"** button
   - Shows: `0.0.0.0/0` (allows all IPs)
   - **Pros:** Works from any computer/network
   - **Cons:** Less secure (but still password protected)
   - Click **"Confirm"**

   **Option B: Add Your Current IP (More Secure)**
   - Click **"Add IP Address"**
   - Click **"Add Current IP Address"**
   - Shows your current IP automatically
   - **Pros:** More secure
   - **Cons:** Won't work if your IP changes or from other locations
   - Click **"Confirm"**

3. **Status:**
   - Wait for status to change from "Pending" to "Active" (10-20 seconds)

---

### Step 5: Create Database and Collection

1. **Go to Database:**
   - Click **"Database"** in left sidebar (under Deployment)
   - You should see your Cluster0

2. **Browse Collections:**
   - Click **"Browse Collections"** button on Cluster0
   - You'll see "No databases available"

3. **Add Database:**
   - Click **"Add My Own Data"** button (or "+ Create Database")

4. **Create Database Form:**
   - **Database name:** Enter **`hci`** (exactly as shown, lowercase)
     - ⚠️ Important: Must be exactly `hci` for the project to work
   - **Collection name:** Enter **`user-config`** (exactly as shown)
     - ⚠️ Important: Must be exactly `user-config` for the project to work
   - Click **"Create"**

5. **Verify:**
   - You should now see database `hci` with collection `user-config` in the list
   - The collection will be empty (that's normal - app will add data when you run it)

---

### Step 6: Get Your Connection String

1. **Connect to Cluster:**
   - Go to **"Database"** in left sidebar
   - Find your **Cluster0**
   - Click **"Connect"** button

2. **Choose Connection Method:**
   - Select **"Connect your application"**
   - (Not "Compass" or "Shell")

3. **Select Driver:**
   - **Driver:** Select **"Python"**
   - **Version:** Select **"3.6 or later"** (any version shown is fine)

4. **Copy Connection String:**
   - You'll see a connection string like:
     ```
     mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
     ```
   - Click the **"Copy"** button
   - Paste it in Notepad/text editor for now

5. **Important Placeholders to Replace:**
   - `<username>` - Replace with the username you created in Step 4.1
   - `<password>` - Replace with the password you saved in Step 4.1
   
   **Example:**
   - Original: `mongodb+srv://<username>:<password>@cluster0.abc123.mongodb.net/?retryWrites=true&w=majority`
   - Your actual: `mongodb+srv://admin:MyP@ssw0rd123@cluster0.abc123.mongodb.net/?retryWrites=true&w=majority`

---

### Step 7: Configure Your Project

1. **Open Project Folder:**
   - Navigate to your project folder where you downloaded/cloned the code
   - Path example: `C:\Users\YourName\Desktop\VTU_Major_Project`

2. **Locate .env File:**
   - Look for a file named **`.env`** (dot env) in the root folder
   - **If you don't see it:** Enable "Show hidden files" in File Explorer
     - Windows: File Explorer → View tab → Check "Hidden items"
     - Or create it in next step

3. **Edit .env File:**

   **Option A: File exists**
   - Right-click `.env` → Open with Notepad (or any text editor)
   
   **Option B: Create new file**
   - Open Notepad
   - Type the following (then save as `.env` in next step)

4. **Add Connection String:**
   - In the `.env` file, you should see:
     ```
     MONGODB.URI=
     ```
   
   - Paste your MongoDB Atlas connection string after the `=` sign:
     ```
     MONGODB.URI=mongodb+srv://admin:MyP@ssw0rd123@cluster0.abc123.mongodb.net/?retryWrites=true&w=majority
     ```
   
   - **Make sure:**
     - NO spaces around the `=` sign
     - NO quotes around the connection string
     - You replaced `<username>` with your actual username
     - You replaced `<password>` with your actual password

5. **Save the File:**
   - File → Save (or Ctrl+S)
   - **Critical:** Save as **`.env`** (with the dot at the start)
   - File type: **All Files** (not .txt)
   - Encoding: **UTF-8** (if option available)

---

### Step 8: Verify Your Configuration

#### Test 1: Check .env File Format

Open `.env` file and verify:
```env
MONGODB.URI=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

**Common Mistakes to Avoid:**
- ❌ `MONGODB.URI = mongodb+srv://...` (space around =)
- ❌ `MONGODB.URI="mongodb+srv://..."` (quotes)
- ❌ `MONGODB.URI='mongodb+srv://...'` (single quotes)
- ❌ `MONGODB.URI=mongodb://localhost:27017/` (local MongoDB, not Atlas)
- ❌ Still has `<username>` or `<password>` placeholders
- ✅ `MONGODB.URI=mongodb+srv://admin:Pass123@cluster0.abc.mongodb.net/?retryWrites=true&w=majority` (correct)

#### Test 2: Check Database in Atlas

1. Go to Atlas → Database → Browse Collections
2. Verify you see:
   - Database: `hci`
   - Collection: `user-config`

#### Test 3: Check Network Access

1. Go to Atlas → Security → Network Access
2. Verify:
   - At least one IP address listed
   - Status: "Active" (not "Pending")

---

### Step 9: Run Your Project

1. **Open Terminal/Command Prompt:**
   
   **Windows:**
   - Press `Win + R`
   - Type `powershell`
   - Press Enter

   **macOS/Linux:**
   - Open Terminal app

2. **Navigate to Project Folder:**
   ```bash
   cd path\to\your\project
   ```
   Example:
   ```bash
   cd C:\Users\YourName\Desktop\VTU_Major_Project
   ```

3. **Activate Virtual Environment:**

   **Windows:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   
   **macOS/Linux:**
   ```bash
   source .venv/bin/activate
   ```

   - You should see `(.venv)` at the start of your command prompt

4. **Run the Application:**
   ```bash
   python main.py
   ```

5. **Expected Output:**
   - Console shows: `<unique-device-id>`
   - Console shows: `✓ Gesture control program started`
   - GUI window opens
   - No error messages about MongoDB connection

---

## 🔍 Troubleshooting

### Issue 1: "Authentication Failed" or "Invalid Username/Password"

**Cause:** Wrong username or password in connection string

**Solution:**
1. Go to Atlas → Security → Database Access
2. Delete old user, create new user
3. Copy new password carefully
4. Update `.env` file with correct credentials
5. Make sure password doesn't contain special characters like `@`, `:`, `/`, `?`, `#`, `[`, `]`
   - If it does, you need to URL-encode them:
     - `@` → `%40`
     - `:` → `%3A`
     - `/` → `%2F`
     - `?` → `%3F`

### Issue 2: "Connection Timeout" or "No route to host"

**Cause:** IP address not whitelisted

**Solution:**
1. Go to Atlas → Security → Network Access
2. Click "Add IP Address"
3. Choose "Allow Access from Anywhere" (0.0.0.0/0)
4. Wait for status to become "Active"

### Issue 3: "Database 'hci' not found" or "Collection 'user-config' not found"

**Cause:** Database or collection not created with exact names

**Solution:**
1. Go to Atlas → Database → Browse Collections
2. Verify database is named exactly **`hci`** (lowercase)
3. Verify collection is named exactly **`user-config`** (with hyphen)
4. If wrong, delete and recreate with correct names

### Issue 4: ".env file not found"

**Cause:** File not in correct location or has wrong extension

**Solution:**
1. Create `.env` file in project **root folder** (same level as `main.py`)
2. Make sure it's named `.env` (not `.env.txt` or `env`)
3. Windows: View → Show "File name extensions" to verify

### Issue 5: "No module named 'pymongo'"

**Cause:** Dependencies not installed

**Solution:**
```bash
pip install -r requirements_windows.txt
# or for macOS
pip install -r requirements_apple_silicon.txt
```

### Issue 6: Connection string visible in error messages

**Cause:** Connection error showing full string with password

**Solution:**
- This is normal for debugging
- Never share error messages publicly
- Rotate (change) password in Atlas if exposed:
  - Security → Database Access → Edit user → Edit Password

---

## 📊 Verify Data Storage

After running the project and creating custom gestures:

1. **Go to Atlas Dashboard:**
   - Database → Browse Collections
   - Click on `hci` database
   - Click on `user-config` collection

2. **You should see documents:**
   - Each document represents a user's custom gesture configuration
   - Document ID (`_id`): Your unique device ID
   - Fields: Custom gesture definitions

3. **This confirms:**
   - Connection is working
   - Data is being saved to cloud
   - Your configuration will persist across sessions

---

## 🔒 Security Best Practices

1. **Never commit .env file to Git:**
   - Already in `.gitignore`
   - Double-check: `git status` should NOT show `.env`

2. **Never share your connection string:**
   - Contains password
   - Don't post in Discord/forums/GitHub issues

3. **Rotate credentials if exposed:**
   - Atlas → Security → Database Access
   - Edit user → Edit Password
   - Update `.env` file with new password

4. **Use IP whitelist in production:**
   - "Allow from Anywhere" is OK for development
   - For production/deployment, specify exact IPs

5. **Use environment variables:**
   - Never hardcode connection string in Python files
   - Always use `os.getenv("MONGODB.URI")` to read from `.env`

---

## 🌐 MongoDB Atlas Dashboard Overview

**Key Sections:**

1. **Database (Deployment):**
   - View your clusters
   - Browse collections
   - Check storage usage

2. **Security:**
   - Database Access: Manage users
   - Network Access: Manage IP whitelist

3. **Data Services:**
   - Charts: Create visualizations
   - Triggers: Automate actions

4. **Metrics:**
   - Monitor connection count
   - Query performance
   - Storage stats

---

## 📱 Access from Multiple Devices

**Your friend wants to run the project:**

1. **Share the repository** (GitHub link)
2. **DO NOT share your `.env` file**
3. **Your friend should:**
   - Follow this guide to create their own MongoDB Atlas account
   - OR use the SAME connection string (you share it privately)
     - Recommended: Same cluster for data consistency
     - Both of you can use same `MONGODB.URI`
     - Custom gestures will sync between devices

**Option A: Shared Database (Recommended)**
- You create MongoDB Atlas cluster
- Share connection string with team members privately (Signal/WhatsApp, not GitHub)
- Everyone uses same `.env` configuration
- Data syncs across all devices
- Each device gets unique ID in database

**Option B: Individual Databases**
- Each person creates their own MongoDB Atlas account
- Each person follows this guide independently
- Data stored separately
- No data sharing between instances

---

## ❓ FAQ

**Q: Is MongoDB Atlas really free?**  
A: Yes! M0 tier (512MB) is completely free forever. No credit card required.

**Q: What happens if I exceed 512MB?**  
A: For this project, you won't. Custom gesture data is tiny (~1KB per user). You can store thousands of configurations.

**Q: Can I use local MongoDB instead?**  
A: Yes, but requires MongoDB installation on every computer. Atlas is easier for multi-device access.

**Q: Is my data secure?**  
A: Yes! MongoDB Atlas uses encryption, authentication, and secure connections (TLS/SSL).

**Q: Can I delete the cluster later?**  
A: Yes. Atlas → Database → Cluster0 → ... (three dots) → Terminate.

**Q: Do I need to keep my laptop running?**  
A: No! Atlas is cloud-hosted. Your data is always available even when your laptop is off.

**Q: Can I change username/password later?**  
A: Yes. Atlas → Security → Database Access → Edit user → Change password → Update `.env` file.

---

## 📚 Additional Resources

- **MongoDB Atlas Documentation:** https://docs.atlas.mongodb.com/
- **MongoDB Python Driver (PyMongo):** https://pymongo.readthedocs.io/
- **Connection String Format:** https://docs.mongodb.com/manual/reference/connection-string/
- **MongoDB University (Free Courses):** https://university.mongodb.com/

---

## ✅ Setup Checklist

Before running your project, verify:

- [ ] MongoDB Atlas account created
- [ ] Project created in Atlas
- [ ] FREE M0 cluster created and active (Status: Active)
- [ ] Database user created with username and password saved
- [ ] Network access configured (IP whitelisted or 0.0.0.0/0)
- [ ] Database `hci` created
- [ ] Collection `user-config` created
- [ ] Connection string copied from Atlas
- [ ] Connection string modified (replaced `<username>` and `<password>`)
- [ ] `.env` file created in project root folder
- [ ] `MONGODB.URI=` line added with full connection string
- [ ] No spaces around `=` sign in `.env`
- [ ] No quotes around connection string in `.env`
- [ ] Virtual environment activated (`(.venv)` visible in prompt)
- [ ] Dependencies installed (`pip install -r requirements_*.txt`)
- [ ] Project runs without MongoDB connection errors

---

## 🎉 Success Indicators

**You've successfully configured MongoDB Atlas when:**

1. ✅ Running `python main.py` shows NO MongoDB errors
2. ✅ GUI window opens successfully
3. ✅ Console shows unique device ID
4. ✅ Creating custom gestures in app → saves without errors
5. ✅ Atlas → Browse Collections shows data in `user-config`
6. ✅ Custom gestures persist after closing and reopening app
7. ✅ Same gesture config appears on different devices (if using shared cluster)

---

**🎯 You're now ready to use the Smart Gesture-Controlled HCI System with cloud database storage!**

**💡 Tip:** Bookmark this guide for future reference or share with team members.
