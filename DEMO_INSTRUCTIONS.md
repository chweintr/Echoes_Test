# 🎭 Indiana Oracle Demo Instructions

## Quick Demo Setup (5 minutes)

### Step 1: Start the Oracle App
1. Go to folder: `E:\Interactive\interactive_project\indiana-oracle-main`
2. **Double-click** `start_oracle_interface.bat`
3. **Keep this window open!** (Oracle is running)

### Step 2: Make it Public with ngrok
1. Press **Windows Key + R**
2. Type `cmd` and press Enter (opens new terminal)
3. Copy and paste this EXACT command:
   ```
   ngrok config add-authtoken 30hCuJRkIj2CIfDX3NSBgQJf2K0_6vcwvyok3v84xF26fHDNM
   ```
4. Press Enter
5. Copy and paste this EXACT command:
   ```
   ngrok http 8500
   ```
6. Press Enter

### Step 3: Get Your Demo URL
1. Look for line that says: `Forwarding https://[something].ngrok-free.app`
2. **Copy that URL**
3. Share it with stakeholders!

### Step 4: Demo Script
Tell stakeholders:
1. "Visit this URL: [paste ngrok URL]"
2. "Click 'Visit Site' on the ngrok warning page"
3. "Enter password: `vonnegut1922`"
4. "Try asking: 'Tell me about the Granfalloon Festival'"

## When Demo is Over
- Close both windows
- URL stops working automatically

## 🚨 Emergency Backup
If ngrok fails, demo locally:
- Share screen in Zoom/Teams
- Visit `http://localhost:8500`
- Demo on your screen

---
**Save this file to your phone/notes for presentations!**