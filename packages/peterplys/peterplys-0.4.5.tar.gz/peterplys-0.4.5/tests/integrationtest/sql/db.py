from energytt_platform.sql import SqlEngine


db = SqlEngine(
    uri='',  # Patched by tests
    pool_size=1,
)
