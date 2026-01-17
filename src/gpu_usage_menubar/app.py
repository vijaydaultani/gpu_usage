"""
Main menu bar application for GPU monitoring using PyObjC.
Displays dual GPU utilization from remote server in macOS menu bar.
"""

import objc
import threading
import time
import tempfile
import os
import logging

# Set process name for Bartender and other menu bar managers
try:
    import setproctitle
    setproctitle.setproctitle("GPU Monitor")
except ImportError:
    pass
from Foundation import NSObject, NSTimer, NSDate
from typing import Optional

# Optional debug logging - set DEBUG_LOGGING=1 environment variable to enable
DEBUG_LOGGING = os.environ.get('DEBUG_LOGGING', '0') == '1'

if DEBUG_LOGGING:
    logging.basicConfig(
        filename='/tmp/gpu-usage-menubar-debug.log',
        level=logging.INFO,
        format='%(asctime)s - %(message)s'
    )
else:
    logging.basicConfig(level=logging.CRITICAL)

from AppKit import (
    NSApplication, NSStatusBar, NSMenu, NSMenuItem,
    NSAttributedString, NSMutableAttributedString, NSColor, NSFont, NSImage,
    NSVariableStatusItemLength, NSImageInterpolationHigh,
    NSForegroundColorAttributeName, NSFontAttributeName,
    NSApplicationActivationPolicyAccessory
)
from Foundation import NSWorkspace, NSNotificationCenter
from .gpu_fetcher import fetch_gpu_data, GPUData
from .icon_generator import create_dual_gpu_icon, create_single_gpu_icon, create_error_icon


def create_colored_progress_bar(percent: float, width: int = 25, label: str = "") -> NSAttributedString:
    """
    Create a colored horizontal progress bar using NSAttributedString.

    Args:
        percent: Percentage filled (0-100)
        width: Total width of the bar in characters
        label: Optional label prefix

    Returns:
        NSAttributedString with colored progress bar
    """
    percent = max(0, min(100, percent))
    filled_width = int(width * percent / 100)
    empty_width = width - filled_width

    filled_bar = "▓" * filled_width
    empty_bar = "░" * empty_width
    percentage_text = f" {int(percent)}%"

    # Color based on utilization level
    if percent < 50:
        bar_color = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.0, 1.0, 0.0, 1.0)  # Green
    elif percent < 80:
        bar_color = NSColor.colorWithCalibratedRed_green_blue_alpha_(1.0, 0.67, 0.0, 1.0)  # Orange
    else:
        bar_color = NSColor.colorWithCalibratedRed_green_blue_alpha_(1.0, 0.2, 0.2, 1.0)  # Red

    # Create attributed string
    attributed_string = NSMutableAttributedString.alloc().init()

    # Label (if provided)
    if label:
        # Use monospace font for alignment
        label_attrs = {
            NSForegroundColorAttributeName: NSColor.secondaryLabelColor(),
            NSFontAttributeName: NSFont.monospacedSystemFontOfSize_weight_(13.0, 0.0)
        }
        # Use fixed width of 6 characters for alignment
        formatted_label = f"{label:<6}"
        label_string = NSAttributedString.alloc().initWithString_attributes_(
            formatted_label, label_attrs
        )
        attributed_string.appendAttributedString_(label_string)

    # Filled portion (colored)
    if filled_bar:
        filled_attrs = {
            NSForegroundColorAttributeName: bar_color,
            NSFontAttributeName: NSFont.monospacedSystemFontOfSize_weight_(13.0, 0.0)
        }
        filled_string = NSAttributedString.alloc().initWithString_attributes_(
            filled_bar, filled_attrs
        )
        attributed_string.appendAttributedString_(filled_string)

    # Empty portion (gray)
    if empty_bar:
        empty_attrs = {
            NSForegroundColorAttributeName: NSColor.colorWithCalibratedWhite_alpha_(0.5, 1.0),
            NSFontAttributeName: NSFont.monospacedSystemFontOfSize_weight_(13.0, 0.0)
        }
        empty_string = NSAttributedString.alloc().initWithString_attributes_(
            empty_bar, empty_attrs
        )
        attributed_string.appendAttributedString_(empty_string)

    # Percentage text
    percent_attrs = {
        NSForegroundColorAttributeName: NSColor.labelColor(),
        NSFontAttributeName: NSFont.monospacedSystemFontOfSize_weight_(13.0, 0.0)
    }
    percent_string = NSAttributedString.alloc().initWithString_attributes_(
        percentage_text, percent_attrs
    )
    attributed_string.appendAttributedString_(percent_string)

    return attributed_string


class GPUMonitorApp(NSObject):
    """
    Menu bar application to monitor GPU utilization from remote server.
    Displays dual GPU bars in menu bar icon and detailed stats in dropdown.
    """

    def init(self):
        """Initialize the menu bar application."""
        self = objc.super(GPUMonitorApp, self).init()
        if self is None:
            return None

        # Configuration - can be overridden by config file
        self.hostname = os.environ.get('GPU_SERVER_HOST', 'ganesha')
        self.ssh_user = os.environ.get('GPU_SERVER_USER', None)
        self.refresh_interval = float(os.environ.get('GPU_REFRESH_INTERVAL', '300'))  # 5 minutes default
        self.show_percentages = os.environ.get('GPU_SHOW_PERCENTAGES', 'false').lower() == 'true'

        # Create status bar item
        self.statusbar = NSStatusBar.systemStatusBar()
        self.statusitem = self.statusbar.statusItemWithLength_(NSVariableStatusItemLength)

        # Create menu
        self.menu = NSMenu.alloc().init()
        self.menu.setAutoenablesItems_(False)

        # Menu items - Header
        self.header = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            f"GPU Monitor - {self.hostname}", None, ""
        )
        self.header.setEnabled_(False)

        self.timestamp_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "Loading...", None, ""
        )
        self.timestamp_item.setEnabled_(False)

        # GPU 0 items
        self.gpu0_title = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "GPU 0", None, ""
        )
        self.gpu0_title.setEnabled_(False)

        self.gpu0_util_bar = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "Loading...", None, ""
        )
        self.gpu0_util_bar.setEnabled_(False)

        self.gpu0_memory_bar = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "Loading...", None, ""
        )
        self.gpu0_memory_bar.setEnabled_(False)

        self.gpu0_info = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "", None, ""
        )
        self.gpu0_info.setEnabled_(False)

        # GPU 1 items
        self.gpu1_title = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "GPU 1", None, ""
        )
        self.gpu1_title.setEnabled_(False)

        self.gpu1_util_bar = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "Loading...", None, ""
        )
        self.gpu1_util_bar.setEnabled_(False)

        self.gpu1_memory_bar = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "Loading...", None, ""
        )
        self.gpu1_memory_bar.setEnabled_(False)

        self.gpu1_info = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "", None, ""
        )
        self.gpu1_info.setEnabled_(False)

        # Control items
        self.refresh_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "Refresh Now", "manualRefresh:", ""
        )
        self.refresh_item.setTarget_(self)

        # Check current LSUIElement setting
        self.is_hidden_from_cmdtab = self._check_lsuielement_setting()

        # Visibility toggle
        visibility_text = "Show in Cmd+Tab" if self.is_hidden_from_cmdtab else "Hide from Cmd+Tab"
        self.visibility_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            visibility_text, "toggleVisibility:", ""
        )
        self.visibility_item.setTarget_(self)

        self.quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "Quit GPU Monitor", "quitApplication:", ""
        )
        self.quit_item.setTarget_(self)

        # Add items to menu
        self.menu.addItem_(self.header)
        self.menu.addItem_(self.timestamp_item)
        self.menu.addItem_(NSMenuItem.separatorItem())
        self.menu.addItem_(self.gpu0_title)
        self.menu.addItem_(self.gpu0_util_bar)
        self.menu.addItem_(self.gpu0_memory_bar)
        self.menu.addItem_(self.gpu0_info)
        self.menu.addItem_(NSMenuItem.separatorItem())
        self.menu.addItem_(self.gpu1_title)
        self.menu.addItem_(self.gpu1_util_bar)
        self.menu.addItem_(self.gpu1_memory_bar)
        self.menu.addItem_(self.gpu1_info)
        self.menu.addItem_(NSMenuItem.separatorItem())
        self.menu.addItem_(self.refresh_item)
        self.menu.addItem_(self.visibility_item)
        self.menu.addItem_(NSMenuItem.separatorItem())
        self.menu.addItem_(self.quit_item)

        # Set the menu
        self.statusitem.setMenu_(self.menu)

        # State
        self._lock = threading.Lock()
        self._icon_path = None
        self._is_sleeping = False
        self._last_gpu_data = None

        # Register for sleep/wake notifications
        workspace = NSWorkspace.sharedWorkspace()
        notification_center = workspace.notificationCenter()

        notification_center.addObserver_selector_name_object_(
            self, "systemWillSleep:", "NSWorkspaceWillSleepNotification", None
        )
        notification_center.addObserver_selector_name_object_(
            self, "systemDidWake:", "NSWorkspaceDidWakeNotification", None
        )

        # Initial refresh
        logging.info(f"Application started, monitoring {self.hostname}")
        self.refreshData_(None)

        # Set up timer for auto-refresh
        self.timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            self.refresh_interval, self, "refreshData:", None, True
        )
        logging.info(f"Timer started with {self.refresh_interval} second interval")

        return self

    def systemWillSleep_(self, notification):
        """Handle system sleep notification."""
        logging.info("System going to sleep - pausing refresh")
        self._is_sleeping = True
        if self.timer:
            self.timer.invalidate()
            self.timer = None

    def systemDidWake_(self, notification):
        """Handle system wake notification."""
        logging.info("System woke up - resuming refresh")
        self._is_sleeping = False
        self.refreshData_(None)
        if not self.timer:
            self.timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
                self.refresh_interval, self, "refreshData:", None, True
            )

    def refreshData_(self, timer):
        """Refresh GPU data from remote server."""
        if self._is_sleeping:
            logging.info("Skipping refresh - system is sleeping")
            return

        with self._lock:
            # Fetch GPU data
            gpu_data = fetch_gpu_data(self.hostname, self.ssh_user, timeout=10)

            if gpu_data is None or not gpu_data.gpus:
                # Error state
                self._show_error_state()
                return

            self._last_gpu_data = gpu_data

            # Update icon
            try:
                if len(gpu_data.gpus) >= 2:
                    icon_bytes = create_dual_gpu_icon(
                        gpu_data.gpus[0].utilization,
                        gpu_data.gpus[1].utilization
                    )
                elif len(gpu_data.gpus) == 1:
                    icon_bytes = create_single_gpu_icon(gpu_data.gpus[0].utilization)
                else:
                    icon_bytes = create_error_icon()

                # Save icon to temporary file
                if self._icon_path:
                    try:
                        os.unlink(self._icon_path)
                    except:
                        pass

                fd, self._icon_path = tempfile.mkstemp(suffix='.png')
                os.write(fd, icon_bytes)
                os.close(fd)

                # Load and set image
                image = NSImage.alloc().initWithContentsOfFile_(self._icon_path)
                if image:
                    image.setTemplate_(False)
                    image.setSize_((18, 18))
                    self.statusitem.setImage_(image)
                    # Show percentages if enabled (optional)
                    if self.show_percentages:
                        label = f" {int(gpu_data.gpus[0].utilization)}%/{int(gpu_data.gpus[1].utilization if len(gpu_data.gpus) > 1 else 0)}%"
                        self.statusitem.setTitle_(label)
                    else:
                        self.statusitem.setTitle_("")
            except Exception as e:
                logging.error(f"Error creating icon: {e}")
                self.statusitem.setTitle_("GPU")

            # Update menu items
            self.timestamp_item.setTitle_(f"Updated: {gpu_data.timestamp}")

            # GPU 0
            if len(gpu_data.gpus) >= 1:
                gpu0 = gpu_data.gpus[0]
                self.gpu0_title.setTitle_(f"GPU 0")
                self.gpu0_util_bar.setAttributedTitle_(
                    create_colored_progress_bar(gpu0.utilization, label="Util:")
                )
                self.gpu0_memory_bar.setAttributedTitle_(
                    create_colored_progress_bar(gpu0.memory_percent, label="Mem:")
                )
                # Convert MB to GB
                memory_used_gb = gpu0.memory_used / 1024
                memory_total_gb = gpu0.memory_total / 1024
                self.gpu0_info.setTitle_(
                    f"  {memory_used_gb:.1f}GB/{memory_total_gb:.1f}GB | {gpu0.temperature}°C | {gpu0.power_draw:.1f}W"
                )

            # GPU 1
            if len(gpu_data.gpus) >= 2:
                gpu1 = gpu_data.gpus[1]
                self.gpu1_title.setTitle_(f"GPU 1")
                self.gpu1_util_bar.setAttributedTitle_(
                    create_colored_progress_bar(gpu1.utilization, label="Util:")
                )
                self.gpu1_memory_bar.setAttributedTitle_(
                    create_colored_progress_bar(gpu1.memory_percent, label="Mem:")
                )
                # Convert MB to GB
                memory_used_gb = gpu1.memory_used / 1024
                memory_total_gb = gpu1.memory_total / 1024
                self.gpu1_info.setTitle_(
                    f"  {memory_used_gb:.1f}GB/{memory_total_gb:.1f}GB | {gpu1.temperature}°C | {gpu1.power_draw:.1f}W"
                )
            else:
                # Hide GPU 1 items if only one GPU
                self.gpu1_title.setTitle_("GPU 1: Not available")
                self.gpu1_util_bar.setTitle_("")
                self.gpu1_memory_bar.setTitle_("")
                self.gpu1_info.setTitle_("")

    def _show_error_state(self):
        """Show error state in menu when data fetch fails."""
        try:
            icon_bytes = create_error_icon()
            if self._icon_path:
                try:
                    os.unlink(self._icon_path)
                except:
                    pass

            fd, self._icon_path = tempfile.mkstemp(suffix='.png')
            os.write(fd, icon_bytes)
            os.close(fd)

            image = NSImage.alloc().initWithContentsOfFile_(self._icon_path)
            if image:
                image.setTemplate_(False)
                image.setSize_((18, 18))
                self.statusitem.setImage_(image)
                self.statusitem.setTitle_("")
        except:
            self.statusitem.setTitle_("⚠️")
            self.statusitem.setImage_(None)

        self.timestamp_item.setTitle_("⚠️  Failed to connect to GPU server")
        self.gpu0_util_bar.setTitle_(f"Check SSH access to {self.hostname}")
        self.gpu0_memory_bar.setTitle_("")
        self.gpu0_info.setTitle_("")
        self.gpu1_util_bar.setTitle_("")
        self.gpu1_memory_bar.setTitle_("")
        self.gpu1_info.setTitle_("")

    def _check_lsuielement_setting(self):
        """Check if LSUIElement is set to true (hidden from Cmd+Tab)."""
        try:
            import subprocess
            # Find the app bundle
            result = subprocess.run(
                ['defaults', 'read', '/Applications/GPU Monitor.app/Contents/Info.plist', 'LSUIElement'],
                capture_output=True,
                text=True
            )
            return result.stdout.strip() == '1'
        except:
            return False

    def _update_lsuielement_setting(self, hide_from_cmdtab):
        """Update the LSUIElement setting in Info.plist."""
        try:
            import subprocess
            value = 'true' if hide_from_cmdtab else 'false'

            # Update the app bundle in Applications folder
            app_path = '/Applications/GPU Monitor.app/Contents/Info.plist'
            if os.path.exists(app_path):
                subprocess.run([
                    '/usr/libexec/PlistBuddy',
                    '-c', f'Set :LSUIElement {value}',
                    app_path
                ], capture_output=True)
            return True
        except Exception as e:
            logging.error(f"Failed to update LSUIElement: {e}")
            return False

    def manualRefresh_(self, sender):
        """Handle manual refresh button click."""
        logging.info("Manual refresh triggered")
        self.refreshData_(None)

    def toggleVisibility_(self, sender):
        """Toggle visibility in Cmd+Tab and Launchpad."""
        logging.info("Toggle visibility requested")

        # Current state
        currently_hidden = self.is_hidden_from_cmdtab
        new_hidden_state = not currently_hidden

        # Update the setting
        if self._update_lsuielement_setting(new_hidden_state):
            # Show dialog
            from AppKit import NSAlert, NSAlertFirstButtonReturn
            alert = NSAlert.alloc().init()
            alert.setMessageText_("Restart Required")

            if new_hidden_state:
                alert.setInformativeText_(
                    "The app will be hidden from Cmd+Tab and Launchpad after restart.\n\n"
                    "Click OK to quit and restart the app."
                )
            else:
                alert.setInformativeText_(
                    "The app will appear in Cmd+Tab, Dock, and Launchpad after restart.\n\n"
                    "Click OK to quit and restart the app."
                )

            alert.addButtonWithTitle_("OK")
            alert.addButtonWithTitle_("Cancel")

            response = alert.runModal()

            if response == NSAlertFirstButtonReturn:
                # Restart the app
                import subprocess
                script_path = os.path.expanduser('~/work/github/gpu_usage/scripts/restart.sh')
                subprocess.Popen([script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                # Quit this instance
                self.cleanup()
                NSApplication.sharedApplication().terminate_(self)
        else:
            # Show error
            from AppKit import NSAlert
            alert = NSAlert.alloc().init()
            alert.setMessageText_("Error")
            alert.setInformativeText_("Failed to update visibility setting. Check permissions.")
            alert.addButtonWithTitle_("OK")
            alert.runModal()

    def quitApplication_(self, sender):
        """Handle quit menu item - properly terminate the application."""
        logging.info("Quit requested by user")
        self.cleanup()
        NSApplication.sharedApplication().terminate_(self)

    def cleanup(self):
        """Clean up resources."""
        workspace = NSWorkspace.sharedWorkspace()
        notification_center = workspace.notificationCenter()
        notification_center.removeObserver_(self)

        if self.timer:
            self.timer.invalidate()

        if self._icon_path:
            try:
                os.unlink(self._icon_path)
            except:
                pass


def main():
    """Entry point for the application."""
    app = NSApplication.sharedApplication()
    app.setActivationPolicy_(NSApplicationActivationPolicyAccessory)

    # Create and initialize our app
    delegate = GPUMonitorApp.alloc().init()

    # Run the application
    from PyObjCTools import AppHelper
    AppHelper.runEventLoop()


if __name__ == "__main__":
    main()
