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


def debug_move(event,pokemon=None,move=None,target=None):
    if not DEBUG_ENABLED: return
    print(f'[DEBUG] {event} | {pokemon} | {move} | {target}')


def debug_switch(event, pokemon=None, side=None):
    if not DEBUG_ENABLED:
        return
    print(f"[DEBUG] SWITCH: {event}")
    if pokemon is not None:
        print(f"    pokemon: {getattr(pokemon,'name',pokemon)}")
    if side is not None:
        print(f"    side: {side}")

def debug_status(event, pokemon=None, status=None):
    if not DEBUG_ENABLED:
        return
    print(f"[DEBUG] STATUS: {event}")
    if pokemon is not None:
        print(f"    pokemon: {getattr(pokemon,'name',pokemon)}")
    if status is not None:
        print(f"    status: {status}")


def debug_field(event, **kwargs):
    return debug_event(f'FIELD:{event}', **kwargs)


def debug_damage(attacker=None,target=None,move=None,damage=None):
    if not DEBUG_ENABLED: return
    print(f"[DEBUG] DAMAGE attacker={attacker} target={target} move={move} damage={damage}")

def debug_accuracy(user=None,move=None,result=None):
    if not DEBUG_ENABLED: return
    print(f"[DEBUG] ACCURACY user={user} move={move} result={result}")

def debug_secondary(move=None,effect=None):
    if not DEBUG_ENABLED: return
    print(f"[DEBUG] SECONDARY move={move} effect={effect}")
