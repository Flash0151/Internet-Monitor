# 🌐 Internet Monitor - Because Windows is a Data Thief! 🕵️

[![Windows](https://img.shields.io/badge/Fights-Windows%20Data%20Theft-blue)]()
[![Python](https://img.shields.io/badge/Python-3.7%2B-yellow)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()
[![Mood](https://img.shields.io/badge/Mood-Hungry%20for%20Data%20Justice-red)]()

## 🎭 The Drama

**Windows:** "Hey, you have internet? Let me just quietly download 5GB of updates, sync OneDrive (that you never use), update the Store (that you forgot existed), send telemetry about your cat pictures, and oh - Xbox services need updating too even though you don't own an Xbox!"

**You:** "I have 10GB for the whole month..."

**Windows:** "WAS THAT A CHALLENGE?!" *downloads aggressively*

**This App:** "NOT TODAY, MICROSOFT!" 🛑

---

## 🦸‍♂️ What This Hero Does

- 👀 **Watches Windows like a hawk** - Every process, every connection
- 🚨 **Screams when data limit hit** - "HEY! Windows ate 100MB!"
- 🔨 **BONKS Windows** - One click and BAM! No more Microsoft internet!
- 🟢 **Spares the innocent** - Chrome? Safe. Games? Safe. Discord? Safe.
- 🔴 **Marks the guilty** - Red for Microsoft (booo!), Green for your apps (yaaay!)

---

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