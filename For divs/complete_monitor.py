import psutil
import time
import subprocess
import os
import sys
import json
from datetime import datetime, timedelta
from collections import defaultdict
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import pystray
from PIL import Image, ImageDraw
import socket

class CompleteInternetMonitor:
    def __init__(self):
        self.limit_mb = 100
        self.limit_bytes = self.limit_mb * 1024 * 1024
        self.total_windows_usage = 0
        self.is_blocked = False
        self.monitoring = True
        self.paused = False
        
        # Track ALL processes
        self.process_usage = defaultdict(lambda: {
            'name': '',
            'sent': 0,
            'recv': 0,
            'total': 0,
            'connections': 0,
            'first_seen': datetime.now(),
            'last_seen': datetime.now(),
            'is_windows': False
        })
        
        # Windows processes to track
        self.windows_processes = [
            'svchost.exe', 'wuauclt.exe', 'TrustedInstaller.exe',
            'TiWorker.exe', 'UsoClient.exe', 'WaaSMedic.exe',
            'SearchApp.exe', 'SearchIndexer.exe', 'OneDrive.exe',
            'FileCoAuth.exe', 'OfficeClickToRun.exe', 'msiexec.exe',
            'taskhostw.exe', 'CompatTelRunner.exe', 'MpCmdRun.exe',
            'NisSrv.exe', 'SecurityHealthService.exe', 'WmiPrvSE.exe',
            'backgroundTaskHost.exe', 'MicrosoftEdge.exe', 'msedge.exe',
            'GameBarPresenceWriter.exe', 'xboxapp.exe',
            'Microsoft.Photos.exe', 'SkypeApp.exe', 'SkypeHost.exe',
            'YourPhone.exe', 'Microsoft.SharePoint.exe',
            'WinStore.App.exe', 'MicrosoftStore.exe',
            'Widgets.exe', 'WidgetService.exe',
            'CrossDeviceService.exe', 'LockApp.exe',
            'StartMenuExperienceHost.exe', 'ShellExperienceHost.exe',
            'TextInputHost.exe', 'SettingSyncHost.exe',
            'SystemSettings.exe', 'ApplicationFrameHost.exe',
            'sihost.exe', 'RuntimeBroker.exe', 'MoUsoCoreWorker.exe',
            'MusNotifyIcon.exe', 'smartscreen.exe',
            'winword.exe', 'excel.exe', 'powerpnt.exe', 'outlook.exe',
            'msaccess.exe', 'mspub.exe', 'onenote.exe',
            'officehub.exe', 'officeapp.exe',
            'Teams.exe', 'teams.exe', 'update.exe',
            'consent.exe', 'DeviceCensus.exe', 'wermgr.exe',
            'WerFault.exe', 'dwm.exe', 'explorer.exe',
            'fontdrvhost.exe', 'LogonUI.exe',
        ]
        
        # Services to disable
        self.services_to_disable = {
            'wuauserv': 'Windows Update',
            'UsoSvc': 'Update Orchestrator',
            'WaaSMedicSvc': 'Windows Update Medic',
            'BITS': 'Background Transfer',
            'DoSvc': 'Delivery Optimization',
            'DiagTrack': 'Diagnostics Tracking',
            'dmwappushservice': 'WAP Push',
            'MapsBroker': 'Maps Download',
            'lfsvc': 'Geolocation',
            'PcaSvc': 'Compatibility Assistant',
            'WSearch': 'Windows Search',
            'SysMain': 'Superfetch',
            'WMPNetworkSvc': 'Media Player Network',
            'XboxNetApiSvc': 'Xbox Networking',
            'XblAuthManager': 'Xbox Live Auth',
            'XblGameSave': 'Xbox Game Save',
            'OneSyncSvc': 'Sync Host',
            'UnistoreSvc': 'User Data Storage',
        }
        
        self.config_file = "complete_monitor_config.json"
        self.load_config()
        
        # For network speed calculation
        self.last_net_io = psutil.net_io_counters()
        self.last_net_time = time.time()
    
    def load_config(self):
        """Load configuration"""
        self.config = {
            'limit_mb': 100,
            'auto_block': False,
            'start_with_windows': False,
            'check_interval': 2,
            'block_all_microsoft': True,
            'show_all_processes': True,
            'notify_warning': True,
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                    self.config.update(loaded)
                    self.limit_mb = self.config['limit_mb']
                    self.limit_bytes = self.limit_mb * 1024 * 1024
            except:
                pass
    
    def save_config(self):
        """Save configuration"""
        self.config['limit_mb'] = self.limit_mb
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def format_bytes(self, bytes_val):
        """Convert bytes to human readable"""
        if bytes_val < 1024:
            return f"{bytes_val:.0f} B"
        elif bytes_val < 1024*1024:
            return f"{bytes_val/1024:.1f} KB"
        elif bytes_val < 1024*1024*1024:
            return f"{bytes_val/(1024*1024):.2f} MB"
        else:
            return f"{bytes_val/(1024*1024*1024):.2f} GB"
    
    def get_all_network_usage(self):
        """Get network usage for ALL processes"""
        current_usage = {}
        
        try:
            # First get all network connections
            all_connections = psutil.net_connections(kind='inet')
            
            # Map connections to PIDs
            pid_connections = defaultdict(list)
            for conn in all_connections:
                if conn.pid:
                    pid_connections[conn.pid].append(conn)
            
            # Now iterate processes
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    proc_info = proc.info
                    pid = proc_info['pid']
                    proc_name = proc_info['name'] or 'Unknown'
                    
                    # Check if this process has connections
                    has_connections = pid in pid_connections
                    established = [c for c in pid_connections.get(pid, []) if c.status == 'ESTABLISHED']
                    
                    # Check if it's a Windows process
                    is_windows = any(
                        win_proc.lower() == proc_name.lower() 
                        for win_proc in self.windows_processes
                    )
                    
                    # Get IO counters as network usage approximation
                    try:
                        io_counters = proc.io_counters()
                        current_io = io_counters.read_bytes + io_counters.write_bytes
                        
                        if pid in self.process_usage:
                            last_io = self.process_usage[pid].get('last_io', current_io)
                            io_diff = current_io - last_io
                        else:
                            io_diff = 0
                            self.process_usage[pid]['first_seen'] = datetime.now()
                        
                        self.process_usage[pid]['last_io'] = current_io
                        
                        # Include if active or has connections
                        if io_diff > 0 or len(established) > 0 or is_windows:
                            current_usage[pid] = {
                                'name': proc_name,
                                'usage': max(0, io_diff),
                                'connections': len(established),
                                'is_windows': is_windows,
                                'pid': pid
                            }
                    except:
                        pass
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except Exception as e:
            print(f"Error getting usage: {e}")
        
        return current_usage
    
    def get_network_speed(self):
        """Get current network speed"""
        try:
            current_net = psutil.net_io_counters()
            time_diff = time.time() - self.last_net_time
            
            if time_diff > 0:
                download_speed = (current_net.bytes_recv - self.last_net_io.bytes_recv) / time_diff
                upload_speed = (current_net.bytes_sent - self.last_net_io.bytes_sent) / time_diff
            else:
                download_speed = 0
                upload_speed = 0
            
            self.last_net_io = current_net
            self.last_net_time = time.time()
            
            return download_speed, upload_speed
        except:
            return 0, 0
    
    def block_everything_microsoft(self):
        """Aggressively block ALL Microsoft internet access"""
        if self.is_blocked:
            return
        
        print("🛑 BLOCKING ALL MICROSOFT INTERNET ACCESS...")
        
        # Microsoft IP ranges
        microsoft_ips = [
            '13.64.0.0/11', '13.96.0.0/13', '13.104.0.0/14',
            '20.0.0.0/11', '20.33.0.0/16', '20.34.0.0/15',
            '20.36.0.0/14', '20.40.0.0/13', '20.48.0.0/12',
            '20.64.0.0/10', '40.64.0.0/10', '40.76.0.0/14',
            '40.80.0.0/12', '40.96.0.0/12', '40.112.0.0/13',
            '52.96.0.0/12', '52.112.0.0/14', '52.120.0.0/14',
            '52.136.0.0/13', '52.160.0.0/11', '52.224.0.0/11',
            '104.40.0.0/13', '131.253.0.0/16', '137.116.0.0/16',
            '157.55.0.0/16', '191.232.0.0/13',
        ]
        
        # Add firewall rules
        for i, ip in enumerate(microsoft_ips):
            try:
                subprocess.run(
                    f'netsh advfirewall firewall add rule '
                    f'name="CompleteMon_Block_MS_{i}" '
                    f'dir=out action=block remoteip={ip} enable=yes',
                    shell=True, capture_output=True, timeout=5
                )
            except:
                pass
        
        # Stop Microsoft services
        for service, desc in self.services_to_disable.items():
            try:
                subprocess.run(['net', 'stop', service], 
                             shell=True, capture_output=True, timeout=5)
                subprocess.run(['sc', 'config', service, 'start=disabled'],
                             shell=True, capture_output=True, timeout=5)
                print(f"✓ Stopped: {desc}")
            except:
                pass
        
        self.is_blocked = True
        print("✅ BLOCKED! Your other apps still work normally")
        
    def unblock_everything(self):
        """Remove all blocks"""
        if not self.is_blocked:
            return
        
        print("🔓 REMOVING ALL BLOCKS...")
        
        # Remove firewall rules
        try:
            result = subprocess.run(
                'netsh advfirewall firewall show rule name=all',
                shell=True, capture_output=True, text=True, timeout=5
            )
            
            if result.stdout:
                for line in result.stdout.split('\n'):
                    if 'CompleteMon_' in line:
                        try:
                            rule_name = line.split(':')[1].strip()
                            subprocess.run(
                                f'netsh advfirewall firewall delete rule name="{rule_name}"',
                                shell=True, capture_output=True, timeout=5
                            )
                        except:
                            pass
        except:
            pass
        
        # Re-enable services
        for service in self.services_to_disable.keys():
            try:
                subprocess.run(['sc', 'config', service, 'start=auto'],
                             shell=True, capture_output=True, timeout=5)
            except:
                pass
        
        self.is_blocked = False
        self.total_windows_usage = 0
        print("✅ UNBLOCKED!")


class CompleteMonitorGUI:
    def __init__(self, monitor):
        self.monitor = monitor
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Complete Internet Monitor - Track Everything")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        self.root.protocol('WM_DELETE_WINDOW', self.on_window_close)
        
        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Colors
        self.bg_color = '#2b2b2b'
        self.fg_color = '#ffffff'
        self.warning_color = '#ff6b6b'
        self.ok_color = '#51cf66'
        
        self.root.configure(bg=self.bg_color)
        
        # Initialize tray icon as None
        self.tray_icon = None
        
        self.create_widgets()
        self.create_tray_icon()
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        # Update GUI
        self.update_gui()
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title and status
        title_frame = tk.Frame(main_frame, bg=self.bg_color)
        title_frame.pack(fill=tk.X, pady=5)
        
        self.status_label = tk.Label(
            title_frame,
            text="🟢 MONITORING - Tracking ALL internet usage",
            font=('Segoe UI', 14, 'bold'),
            bg=self.bg_color, fg=self.ok_color
        )
        self.status_label.pack(anchor=tk.W)
        
        # Speed indicator
        self.speed_label = tk.Label(
            title_frame,
            text="↓ 0 B/s  ↑ 0 B/s",
            font=('Segoe UI', 9),
            bg=self.bg_color, fg='#888888'
        )
        self.speed_label.pack(anchor=tk.W, pady=2)
        
        # Usage counter
        counter_frame = tk.Frame(main_frame, bg=self.bg_color)
        counter_frame.pack(fill=tk.X, pady=10)
        
        self.counter_label = tk.Label(
            counter_frame,
            text="Total Microsoft Usage: 0.0 MB / 100 MB",
            font=('Segoe UI', 12),
            bg=self.bg_color, fg=self.fg_color
        )
        self.counter_label.pack(anchor=tk.W)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            counter_frame,
            length=500,
            mode='determinate',
            maximum=self.monitor.limit_mb
        )
        self.progress.pack(fill=tk.X, pady=5)
        
        # Control buttons
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.block_btn = tk.Button(
            button_frame,
            text="🛑 BLOCK Microsoft Internet",
            command=self.toggle_block,
            bg='#ff6b6b', fg='white',
            font=('Segoe UI', 10, 'bold'),
            relief=tk.FLAT, padx=20, pady=5,
            cursor='hand2'
        )
        self.block_btn.pack(side=tk.LEFT, padx=5)
        
        # MINIMIZE BUTTON
        tk.Button(
            button_frame,
            text="➖ Minimize to Tray",
            command=self.minimize_to_tray,
            bg='#4a4a4a', fg='white',
            font=('Segoe UI', 9),
            relief=tk.FLAT, padx=15, pady=5,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="🔄 Reset Counter",
            command=self.reset_counter,
            bg='#4a4a4a', fg='white',
            font=('Segoe UI', 9),
            relief=tk.FLAT, padx=15, pady=5,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="⏸️ Pause/Resume",
            command=self.toggle_pause,
            bg='#4a4a4a', fg='white',
            font=('Segoe UI', 9),
            relief=tk.FLAT, padx=15, pady=5,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)
        
        # Settings
        settings_frame = tk.LabelFrame(
            main_frame,
            text=" Settings ",
            bg=self.bg_color,
            fg=self.fg_color,
            font=('Segoe UI', 9)
        )
        settings_frame.pack(fill=tk.X, pady=10)
        
        settings_inner = tk.Frame(settings_frame, bg=self.bg_color)
        settings_inner.pack(padx=10, pady=5)
        
        tk.Label(
            settings_inner,
            text="Warning Limit (MB):",
            bg=self.bg_color, fg=self.fg_color
        ).pack(side=tk.LEFT, padx=5)
        
        self.limit_var = tk.StringVar(value=str(self.monitor.limit_mb))
        self.limit_entry = tk.Entry(
            settings_inner,
            textvariable=self.limit_var,
            width=8,
            bg='#3a3a3a', fg='white',
            insertbackground='white'
        )
        self.limit_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            settings_inner,
            text="Apply",
            command=self.apply_limit,
            bg='#4a4a4a', fg='white',
            relief=tk.FLAT, padx=10,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)
        
        # Show filters
        self.show_windows_only_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            settings_inner,
            text="Show Microsoft Only",
            variable=self.show_windows_only_var,
            bg=self.bg_color, fg=self.fg_color,
            selectcolor=self.bg_color,
            activebackground=self.bg_color,
            activeforeground=self.fg_color
        ).pack(side=tk.LEFT, padx=20)
        
        # Process list header
        list_header = tk.Frame(main_frame, bg=self.bg_color)
        list_header.pack(fill=tk.X, pady=5)
        
        tk.Label(
            list_header,
            text="🌐 ALL PROCESSES USING INTERNET",
            font=('Segoe UI', 11, 'bold'),
            bg=self.bg_color, fg=self.fg_color
        ).pack(side=tk.LEFT)
        
        self.process_count_label = tk.Label(
            list_header,
            text="0 processes",
            bg=self.bg_color, fg='#888888'
        )
        self.process_count_label.pack(side=tk.RIGHT)
        
        # Process list
        list_frame = tk.Frame(main_frame, bg=self.bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview
        columns = ('Process', 'Type', 'Data Used', 'Connections', 'Status')
        self.tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show='headings',
            height=20
        )
        
        self.tree.heading('Process', text='Process Name')
        self.tree.heading('Type', text='Type')
        self.tree.heading('Data Used', text='Total Data Used')
        self.tree.heading('Connections', text='Active Connections')
        self.tree.heading('Status', text='Status')
        
        self.tree.column('Process', width=300)
        self.tree.column('Type', width=100)
        self.tree.column('Data Used', width=150)
        self.tree.column('Connections', width=100)
        self.tree.column('Status', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Tags for coloring
        self.tree.tag_configure('windows', background='#3d1f1f', foreground='white')
        self.tree.tag_configure('normal', background='#1f3d1f', foreground='white')
        self.tree.tag_configure('high_usage', background='#3d3d1f', foreground='white')
        
        # Bottom info
        info_frame = tk.Frame(main_frame, bg=self.bg_color)
        info_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            info_frame,
            text="💡 Red = Microsoft processes | Green = Your apps | Yellow = Heavy usage",
            bg=self.bg_color, fg='#888888',
            font=('Segoe UI', 8)
        ).pack(side=tk.LEFT)
        
        self.time_label = tk.Label(
            info_frame,
            text="Last update: --:--:--",
            bg=self.bg_color, fg='#888888',
            font=('Segoe UI', 8)
        )
        self.time_label.pack(side=tk.RIGHT)
    
    def minimize_to_tray(self):
        """Minimize to system tray"""
        self.root.withdraw()
        if self.tray_icon:
            try:
                self.tray_icon.notify(
                    "Internet Monitor",
                    "Minimized to system tray!\nDouble-click icon to restore."
                )
            except:
                pass
    
    def show_window(self, icon=None, item=None):
        """Show window again"""
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        self.root.state('normal')
    
    def on_window_close(self):
        """Handle window close button"""
        self.minimize_to_tray()
    
    def create_tray_icon(self):
        """Create system tray icon"""
        try:
            # Create icon image
            image = Image.new('RGB', (64, 64), '#2b2b2b')
            dc = ImageDraw.Draw(image)
            dc.rectangle([10, 10, 54, 54], fill='#51cf66')
            
            # Create menu with proper callbacks
            menu = pystray.Menu(
                pystray.MenuItem(
                    '📊 Show Window', 
                    self.show_window,
                    default=True  # Double-click to show
                ),
                pystray.MenuItem(
                    '🛑 Toggle Block', 
                    self.toggle_block_from_tray
                ),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem(
                    '❌ Exit', 
                    self.quit_app
                )
            )
            
            self.tray_icon = pystray.Icon(
                "complete_monitor",
                image,
                "Internet Monitor - Double-click to restore",
                menu
            )
            
            # Run in separate thread
            tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
            tray_thread.start()
            
        except Exception as e:
            print(f"Tray icon not available (minimize to taskbar instead): {e}")
            self.tray_icon = None
    
    def toggle_block_from_tray(self, icon=None, item=None):
        """Toggle block from tray menu"""
        self.toggle_block()
    
    def monitor_loop(self):
        """Main monitoring loop"""
        while self.monitor.monitoring:
            try:
                if not self.monitor.paused and not self.monitor.is_blocked:
                    # Get all network usage
                    current_usage = self.monitor.get_all_network_usage()
                    
                    # Update process stats
                    for pid, data in current_usage.items():
                        if data['usage'] > 0:
                            self.monitor.process_usage[pid]['name'] = data['name']
                            self.monitor.process_usage[pid]['connections'] = data['connections']
                            self.monitor.process_usage[pid]['last_seen'] = datetime.now()
                            self.monitor.process_usage[pid]['is_windows'] = data['is_windows']
                            
                            # Add to total if Microsoft
                            if data['is_windows']:
                                self.monitor.process_usage[pid]['total'] += data['usage']
                                self.monitor.total_windows_usage += data['usage']
                    
                    # Check limit
                    if (self.monitor.total_windows_usage >= self.monitor.limit_bytes and
                        not self.monitor.is_blocked and
                        not self.monitor.paused):
                        
                        if self.monitor.config['auto_block']:
                            self.monitor.block_everything_microsoft()
                            self.root.after(0, self.show_block_notification)
                        else:
                            self.root.after(0, self.show_warning)
                            self.monitor.paused = True
                
                time.sleep(self.monitor.config['check_interval'])
                
            except Exception as e:
                print(f"Monitor error: {e}")
                time.sleep(5)
    
    def update_gui(self):
        """Update GUI elements"""
        if not self.monitor.monitoring:
            return
        
        try:
            # Update status
            if self.monitor.is_blocked:
                self.status_label.config(
                    text="🔒 BLOCKED - Microsoft Internet Stopped",
                    fg=self.warning_color
                )
                self.block_btn.config(
                    text="🔓 UNBLOCK Microsoft",
                    bg='#51cf66'
                )
            elif self.monitor.paused:
                self.status_label.config(
                    text="⏸️ PAUSED - Monitoring Paused",
                    fg='#ffa500'
                )
            else:
                self.status_label.config(
                    text="🟢 MONITORING - Tracking ALL internet usage",
                    fg=self.ok_color
                )
            
            # Update speed
            download, upload = self.monitor.get_network_speed()
            self.speed_label.config(
                text=f"↓ {self.monitor.format_bytes(download)}/s  ↑ {self.monitor.format_bytes(upload)}/s"
            )
            
            # Update counter
            usage_mb = self.monitor.total_windows_usage / (1024*1024)
            self.counter_label.config(
                text=f"Total Microsoft Usage: {usage_mb:.2f} MB / {self.monitor.limit_mb} MB"
            )
            self.progress['value'] = min(usage_mb, self.monitor.limit_mb)
            
            # Update process list
            self.update_process_list()
            
            # Update time
            self.time_label.config(text=f"Last update: {datetime.now().strftime('%H:%M:%S')}")
            
        except Exception as e:
            print(f"GUI update error: {e}")
        
        self.root.after(1000, self.update_gui)
    
    def update_process_list(self):
        """Update process list"""
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get processes
        if self.show_windows_only_var.get():
            procs = {pid: data for pid, data in self.monitor.process_usage.items() 
                    if data.get('is_windows', False)}
        else:
            procs = dict(self.monitor.process_usage)
        
        # Sort by total usage
        sorted_procs = sorted(procs.items(), key=lambda x: x[1].get('total', 0), reverse=True)
        
        # Add to treeview
        for pid, data in sorted_procs:
            name = data.get('name', f'PID: {pid}')
            total = self.monitor.format_bytes(data.get('total', 0))
            connections = data.get('connections', 0)
            is_windows = data.get('is_windows', False)
            
            # Type and color
            if is_windows:
                proc_type = '🔴 Microsoft'
                tag = 'windows'
            else:
                proc_type = '🟢 Your App'
                tag = 'normal'
            
            # Status
            if connections > 5:
                status = '🔴 Heavy Use'
                tag = 'high_usage'
            elif connections > 0:
                status = '🟡 Active'
            else:
                status = '⚪ Idle'
            
            self.tree.insert('', 'end', values=(
                name, proc_type, total, connections, status
            ), tags=(tag,))
        
        # Update count
        self.process_count_label.config(text=f"{len(sorted_procs)} processes")
    
    def toggle_block(self):
        """Toggle Microsoft internet block"""
        if self.monitor.is_blocked:
            if messagebox.askyesno("Unblock Microsoft?", "Allow Microsoft internet access again?"):
                self.monitor.unblock_everything()
                self.monitor.paused = False
        else:
            if messagebox.askyesno(
                "Block Microsoft Internet?",
                "⚠️ This will completely block Microsoft from internet!\n\n"
                "What gets blocked:\n"
                "• Windows Update\n"
                "• Microsoft Store\n"
                "• OneDrive\n"
                "• Xbox & Game services\n"
                "• Telemetry & data collection\n"
                "• Office updates\n"
                "• Edge browser syncing\n\n"
                "Your other apps (Chrome, games, etc.) will work!\n\n"
                "Continue?"
            ):
                self.monitor.block_everything_microsoft()
    
    def reset_counter(self):
        """Reset usage counter"""
        self.monitor.total_windows_usage = 0
        self.monitor.process_usage.clear()
        messagebox.showinfo("Reset", "Usage counters have been reset!")
    
    def apply_limit(self):
        """Apply new limit"""
        try:
            new_limit = float(self.limit_var.get())
            if new_limit > 0:
                self.monitor.limit_mb = new_limit
                self.monitor.limit_bytes = new_limit * 1024 * 1024
                self.progress['maximum'] = new_limit
                self.monitor.save_config()
                messagebox.showinfo("Success", f"Limit updated to {new_limit} MB")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number!")
    
    def toggle_pause(self):
        """Toggle pause/resume"""
        self.monitor.paused = not self.monitor.paused
        state = "PAUSED" if self.monitor.paused else "RESUMED"
        messagebox.showinfo("Monitor", f"Monitoring {state}")
    
    def show_warning(self):
        """Show warning when limit exceeded"""
        usage_mb = self.monitor.total_windows_usage / (1024*1024)
        
        result = messagebox.askyesnocancel(
            "⚠️ INTERNET LIMIT REACHED!",
            f"Microsoft has used {usage_mb:.1f} MB!\n"
            f"Your limit: {self.monitor.limit_mb} MB\n\n"
            f"Choose:\n"
            f"• YES - Block Microsoft NOW\n"
            f"• NO - Give 10 more minutes\n"
            f"• CANCEL - Reset counter"
        )
        
        if result is True:
            self.monitor.block_everything_microsoft()
        elif result is False:
            self.monitor.paused = False
            self.monitor.total_windows_usage = 0
            threading.Timer(600, self.reenable_warning).start()
        else:
            self.reset_counter()
            self.monitor.paused = False
    
    def reenable_warning(self):
        """Re-enable warning after delay"""
        pass
    
    def show_block_notification(self):
        """Show auto-block notification"""
        messagebox.showwarning(
            "🔒 AUTO-BLOCKED!",
            "Microsoft internet has been BLOCKED!\n"
            "All Microsoft services are stopped.\n\n"
            "Click 'Unblock' to restore access."
        )
    
    def quit_app(self):
        """Exit application"""
        if messagebox.askyesno("Exit", "Stop monitoring and exit?"):
            self.monitor.monitoring = False
            if self.tray_icon:
                try:
                    self.tray_icon.stop()
                except:
                    pass
            self.root.quit()
            self.root.destroy()
    
    def run(self):
        """Run the GUI"""
        self.root.mainloop()


def main():
    """Main entry point"""
    # Check for admin rights
    try:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        if not is_admin:
            messagebox.showwarning(
                "Admin Rights Recommended",
                "For full blocking features, run as Administrator.\n"
                "Right-click → Run as Administrator"
            )
    except:
        pass
    
    print("Starting Complete Internet Monitor...")
    monitor = CompleteInternetMonitor()
    gui = CompleteMonitorGUI(monitor)
    gui.run()


if __name__ == "__main__":
    main()