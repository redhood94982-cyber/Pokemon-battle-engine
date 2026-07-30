"""
Development debug utilities. Safe to import; no gameplay effects.
"""

DEBUG_ENABLED = True

def set_debug(enabled: bool):
    global DEBUG_ENABLED
    DEBUG_ENABLED = enabled

def debug_event(event: str, **context):
    if not DEBUG_ENABLED:
        return
    print(f"[DEBUG] EVENT: {event}")
    for k,v in context.items():
        print(f"    {k}: {v}")

def debug_listener(pokemon, ability, trigger):
    if not DEBUG_ENABLED:
        return
    print(f"[DEBUG] LISTENER: {getattr(pokemon,'name',pokemon)} | {ability} | {trigger}")
