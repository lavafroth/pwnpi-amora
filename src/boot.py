"""
Disable concurrent write protections on the storage.
This is especially necessary for dev builds since we need to change the files
on the board for hot reloading.
"""

import storage

storage.remount("/", readonly=False, disable_concurrent_write_protection=True)
