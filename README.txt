🌐 INTERNET MONITOR - Stop Windows from Eating Your Data!

One-click app that shows what's using your internet and blocks Windows!


==========================================
📥 FOR NORMAL USERS (JUST WANT THE APP)
==========================================

1. Go to the "dist" folder
2. Download InternetMonitor.exe
3. Right-click → Run as Administrator
4. App opens - you're protected!

That's it! No Python, no coding, no installation needed!

If confused:
- Click "dist" folder above
- Click "InternetMonitor.exe"
- Click "Download" button
- Right-click downloaded file → Run as Administrator


==========================================
🎯 WHAT THIS DOES
==========================================

- Shows EVERY process using your internet
- Red = Microsoft (data thieves!)
- Green = Your apps (safe)
- Warns when Microsoft uses too much data
- Blocks ALL Microsoft with ONE CLICK
- Your apps still work - Chrome, games, Discord, etc.


==========================================
🖥️ HOW TO USE
==========================================

1. Run as Administrator (right-click EXE)
2. Watch the process list
3. Set your limit (100 MB recommended)
4. Click BLOCK when Microsoft eats too much
5. Minimize to tray - runs in background


==========================================
💡 BEST LIMITS FOR YOUR INTERNET
==========================================

Mobile Hotspot: 50-100 MB
Limited DSL: 200-500 MB
Pay-per-GB: 50-100 MB


==========================================
❓ QUICK FAQ (NORMAL USERS)
==========================================

Q: Will this break my computer?
A: No! Only blocks Microsoft. Everything else works.

Q: Can I still update Windows?
A: Yes! Click UNBLOCK, update, then BLOCK again.

Q: Why Run as Administrator?
A: Needed to block Microsoft. Without it, only monitoring works.

Q: Is it a virus?
A: No! Open-source. You can see all code in the files.

Q: How do I restore from tray?
A: Double-click the icon near clock, or right-click → Show Window.


==========================================
🛑 WHAT GETS BLOCKED
==========================================

When you click BLOCK:
- Windows Update (biggest data eater!)
- Microsoft Store (updates apps you never use)
- OneDrive (even if never opened)
- Xbox services (even on non-gaming PCs)
- Telemetry (Microsoft spying)
- Office updates
- Edge browser syncing

Still Working After Block:
- Chrome, Firefox, Brave
- Discord, Zoom, Slack
- Steam, Epic Games
- Spotify, Netflix
- All your games
- All your apps


==========================================
📊 WHAT WINDOWS WASTES (MONTHLY)
==========================================

Windows Update: 1-5 GB per update
Microsoft Store: 100-500 MB
OneDrive: 100+ MB
Telemetry: 30-200 MB
Office Updates: 200-800 MB
Edge Browser: 50-200 MB
Xbox Services: 50-300 MB

Total: 500 MB - 5+ GB per month without you knowing!


==========================================
📝 TROUBLESHOOTING (NORMAL USERS)
==========================================

App won't open:
- Right-click → Run as Administrator
- Temporarily disable antivirus
- Move to short folder path (C:\Monitor\)

Blocking doesn't work:
- Must Run as Administrator
- Windows Firewall must be enabled

Tray icon missing:
- Click ^ arrow near clock (hidden icons)
- Restart the app


==========================================
👨‍💻 FOR DEVELOPERS (WANT TO MODIFY?)
==========================================


🛠️ SETUP FOR DEVELOPMENT

Requirements:
- Python 3.7 or higher
- Windows 10 or 11

Install dependencies:
pip install -r requirements.txt

Or install manually:
pip install psutil pystray pillow pyinstaller


🚀 RUN IN DEVELOPMENT MODE

python complete_monitor.py


🏗️ BUILD YOUR OWN EXE

Option 1 - Simple build:
pyinstaller --onefile --windowed --noconsole --name "InternetMonitor" complete_monitor.py

Option 2 - Use build script:
Double-click build_exe.bat

Option 3 - Debug build (shows errors):
pyinstaller --onefile --console --name "InternetMonitor_debug" complete_monitor.py


📁 PROJECT STRUCTURE

complete_monitor.py     - Main application code
requirements.txt        - Python dependencies
build_exe.bat           - Automatic EXE builder
README.md              - Full documentation (Markdown)
README.txt             - This file
LICENSE                - MIT License
dist/                  - Compiled EXE output folder
build/                 - Temporary build files
For divs/              - Source code for developers


🔧 CODE OVERVIEW

Main Classes:
- CompleteInternetMonitor  - Core monitoring & blocking logic
- CompleteMonitorGUI       - GUI interface & system tray

Key Features:
- Real-time process monitoring using psutil
- Windows Firewall integration for blocking
- System tray minimization with pystray
- Dark theme GUI with tkinter
- Configurable data limits
- Auto-save settings to JSON


🎨 CUSTOMIZATION

Change default limit:
In complete_monitor.py, find:
self.limit_mb = 100  # Change this number

Add new Microsoft processes to track:
In self.windows_processes list, add process names

Change theme colors:
self.bg_color = '#2b2b2b'  # Background
self.fg_color = '#ffffff'  # Text
self.ok_color = '#51cf66'  # Green
self.warning_color = '#ff6b6b'  # Red

Modify check interval:
self.config['check_interval'] = 2  # Seconds


🐛 KNOWN ISSUES (FOR DEVS)

- Process IO counters used as network approximation
  (Windows doesn't expose per-process network easily)
- Some Microsoft processes may restart after being killed
- Firewall rules may need Admin refresh occasionally
- Tray icon may not appear on some Windows configurations
- Large number of processes may slow GUI updates


🔨 TO DO (FUTURE FEATURES)

- Per-process blocking (block specific apps)
- Usage history graphs and statistics
- Daily/weekly/monthly data reports
- Export data usage to CSV
- Email/SMS alerts when limit reached
- Dark/Light theme toggle
- Portable version for USB drives
- Multi-language support


📚 TECHNICAL NOTES

How Blocking Works:
1. Adds Windows Firewall outbound rules for Microsoft IPs
2. Stops Windows services (wuauserv, UsoSvc, etc.)
3. Disables service startup to prevent restart
4. Kills active Microsoft processes using network

How Monitoring Works:
1. Uses psutil to iterate all running processes
2. Checks network connections per process
3. Uses IO counters to estimate data transfer
4. Compares current vs previous readings for delta
5. Flags Windows processes by name matching

Limitations:
- Cannot get exact per-process network bytes (Windows limitation)
- IO counters include disk operations as well
- Some system processes are protected and can't be killed
- Requires Admin for firewall modifications


🤝 CONTRIBUTING

Feel free to:
- Fork the repository
- Submit pull requests
- Report bugs and issues
- Suggest new features
- Improve documentation
- Share with others!


📄 LICENSE

MIT License - Free for everyone!
See LICENSE file for details.


🙏 CREDITS

Built with:
- psutil - Process and system monitoring
- pystray - System tray functionality
- Pillow - Image processing for icons
- tkinter - Graphical user interface
- PyInstaller - EXE compilation

Special thanks:
- Stack Overflow community
- Limited internet users worldwide
- Everyone fighting against Windows data waste!


📞 CONTACT

GitHub: https://github.com/Flash0151/Internet-Monitor
Issues: https://github.com/Flash0151/Internet-Monitor/issues


==========================================
Stop Windows from eating your data! 🌐🚫
==========================================