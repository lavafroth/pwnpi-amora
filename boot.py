import storage

storage.remount(
    "/",
    readonly=False,
    disable_concurrent_write_protection=True,  # Change this to False during production
)
