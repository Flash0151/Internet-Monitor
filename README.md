# 🌐 Internet Monitor - Stop Windows from Eating Your Data!

**One-click app that shows what's using your internet and blocks Windows from wasting it!**

---

## 📥 For Normal Users (Just Want the App)

### Download & Run:
1. Go to the `dist` folder above 👆
2. Download **InternetMonitor.exe**
3. **Right-click → Run as Administrator**
4. App opens - you're protected!

**That's it! No Python, no coding, no installation needed!**

### Video Guide (If confused):
1. Click `dist` folder
2. Click `InternetMonitor.exe`
3. Click "Download" button (or "View raw")
4. Right-click downloaded file → Run as Administrator

---

## 🎯 What This Does (For Everyone)

Windows secretly eats your internet! This app:
- 📊 **Shows EVERY process** using your internet
- 🔴 **Red** = Microsoft (data thieves!)
- 🟢 **Green** = Your apps (safe)
- ⚠️ **Warns you** when Microsoft uses too much data
- 🛑 **Blocks ALL Microsoft** with ONE CLICK
- ✅ **Your apps still work** - Chrome, games, Discord, etc.

---

## 🖥️ How to Use (Normal Users)

1. **Run as Administrator** (right-click EXE)
2. Watch the process list
3. Set your limit (100 MB recommended)
4. Click **BLOCK** when Microsoft eats too much
5. Minimize to tray - runs in background

---

## 💡 Best Settings for Limited Internet

| Your Internet | Set Limit |
|--------------|-----------|
| Mobile Hotspot | 50-100 MB |
| Limited DSL | 200-500 MB |
| Pay-per-GB | 50-100 MB |

---

## ❓ Quick FAQ (Normal Users)

**"Will this break my computer?"**
No! Only blocks Microsoft. Everything else works.

**"Can I still update Windows?"**
Yes! Click UNBLOCK, update, then BLOCK again.

**"Why Run as Administrator?"**
Needed to block Microsoft. Without it, only monitoring works.

**"Is it a virus?"**
No! It's open-source. You can see all the code above.

---

## 🛑 What Gets Blocked

- Windows Update (biggest data eater!)
- Microsoft Store (updates apps you never use)
- OneDrive (even if you never opened it)
- Xbox services (even on non-gaming PCs)
- Telemetry (Microsoft spying)
- Office updates

**Still Working:** Chrome, Firefox, games, Discord, Spotify, everything else!

---

## 📝 Need Help?

If the app won't open:
- Right-click → Run as Administrator
- Temporarily disable antivirus
- Move to a short folder path (like C:\Monitor\)

---

## 👨‍💻 For Developers (Scroll Down)

Want to modify the code? See the developer section below!

## 🏗️ For Developers: How This Magic Works

### The Secret Sauce:

```python
# 1. We spy on EVERY process (shhh, don't tell Windows)
processes = "Give me all your internet users!" 

# 2. We judge them
if process == "Microsoft":
    paint_it_red()  # GUILTY!
    add_to_naughty_list()
else:
    paint_it_green()  # You may pass

# 3. When limit exceeded:
if microsoft_data_used > your_limit:
    scream_at_user()  # "WARNING! WARNING!"
    
# 4. User clicks BLOCK:
block_everything_microsoft()  # TAKE THAT!
# But keep Chrome running because... memes.
The "How We Block" Magic:
We don't just stop services (that's too easy). We:

Firewall Kung-Fu 🥋 - Block Microsoft IPs like a ninja

Service Sleep Spell 😴 - Put Windows Update to bed

Process Karate Chop ✋ - Kill data-hungry processes

Registry Wizardry 🧙 - Disable sneaky startup services

Architecture (or "How The Spaghetti Works"):

User Clicks App
    ↓
GUI Opens (Dark theme because we're cool 😎)
    ↓
Monitor Thread Starts (The Spy)
    ↓
psutil Watches Everything (The Informant)
    ↓
"Hey, svchost.exe is downloading something!"
    ↓
"Is it Microsoft?" → YES → Paint it RED 🔴
    ↓
"Is limit exceeded?" → YES → SHOW WARNING ⚠️
    ↓
User Clicks BLOCK (The Hero Moment)
    ↓
Firewall Rules Deploy (The Shield)
    ↓
Microsoft Services Stop (The Sleep)
    ↓
VICTORY! Chrome Still Works! 🎉
🛠️ How to Hack This (I Mean, Modify)
Prerequisites:

# You need these magic ingredients
pip install psutil    # Process spy
pip install pystray   # Hide in tray like a ninja
pip install pillow    # Make pretty icons
pip install pyinstaller  # Turn into EXE (final form)
Run in Dev Mode:

 complete_monitor.py
# Appears in all its dark-themed glory
Build Your Own EXE:

pyinstaller --onefile --windowed --noconsole --name "WindowsDataPolice" complete_monitor.py
# Now you have an EXE to share with your data-suffering friends
🎮 The Code - Where the Fun Begins
Adding New Microsoft Processes to Spy On:
Found another Microsoft process eating data? Add it here:


self.windows_processes = [
    'svchost.exe',      # The data eating monster
    'OneDrive.exe',     # The thing you never use
    'YourNewEnemy.exe', # ← ADD YOUR ENEMY HERE
]
Changing Default Limit:

# In CompleteInternetMonitor.__init__:
self.limit_mb = 100  # Change to whatever you want
# 50 = "I'm on mobile hotspot"
# 100 = "I'm careful"
# 500 = "I'm generous"
# 9999 = "I trust Microsoft" (why are you here?)
Customizing Colors:

# Make it YOUR theme:
self.bg_color = '#2b2b2b'  # Current: Cool dark
# Try: '#ff00ff' for "I love the 90s" pink
# Try: '#00ff00' for "Matrix mode"
# Try: '#ffffff' for "My eyes! My eyes!" light mode
Adding Sound Effects:

# In show_warning method, add:
import winsound
winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
# Now Windows screams at you when limit reached!
Easter Egg Ideas:

# When limit exceeded 10 times:
if block_count >= 10:
    messagebox.showinfo(
        "Achievement Unlocked!",
        "🏆 'Microsoft's Worst Nightmare'\n"
        "You've blocked Windows 10 times!\n"
        "Satya Nadella is crying somewhere."
    )
🐛 Known Bugs (Features?)
"It shows 0 connections" - Process is being sneaky, watching in 2 seconds

"Tray icon disappeared" - Windows ate it (ironic), restart app

"Block didn't work" - You didn't run as Admin! Windows laughs at non-admins

"App crashed" - Probably psutil having an existential crisis, restart

"Chrome also blocked?" - Impossible! We only block Microsoft. Check if Google got bought by Microsoft overnight

🎯 TODO (Maybe, If We Feel Like It)
Add "Angry Mode" - Blocks Microsoft aggressively with firewall nukes

Add "Paranoid Mode" - Blocks everything except whitelist

Add funny error messages ("Windows Update.exe has been sent to the Shadow Realm")

Achievement system ("Data Saver: Saved 1GB", "Microsoft Hater: 100 blocks")

Sound effects (Windows error sound when blocking)

Monthly report ("You saved 5GB this month! Buy yourself a coffee")

Auto-tweet at Microsoft when limit exceeded

Confetti when you block successfully 🎉

🤣 Fun Facts About Windows Data Usage
Windows Update downloads are bigger than most AAA games

OneDrive syncs even when you've NEVER opened it. How? WHY?

Telemetry sends data even on "Basic" setting. "Basic" means "All of it"

Xbox services run on work laptops. For "business"

Microsoft Store updates apps you uninstalled 2 years ago

Edge runs in background even if you use Chrome. It's watching you.

🙏 Credits
psutil - For being our spy inside Windows

Stack Overflow - For answering "how do I...?" at 3AM

Coffee - The real hero behind this code

Limited Internet Users - You inspired this fight!

Microsoft - For being the villain we needed 😂

⚠️ Warning
This app may cause:

Sudden increase in available data

Confusion when Windows stops downloading

Happiness from saving internet

Microsoft to send you a concerned email (not really, we blocked that too)

🎤 Final Words
Remember: With great power comes great data savings!

Now go forth and BLOCK THAT WINDOWS DATA!

"Ask not what your internet can do for Windows, ask what Windows is doing to your internet!" - JFK (probably, if he had limited data)

Made with ❤️ and 😡 at Microsoft's data habits

P.S. If you work at Microsoft: This is a joke. We love you. Please stop eating our data. 😘