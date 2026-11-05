"""Profile settings for the SkillOps demo app.

Seeded with a real bug: saving a profile with an empty optional display
name crashes (the settings page shows a 500 error).
"""


def initials(display_name):
    """Initials shown in the avatar, e.g. "Ada Lovelace" -> "AL"."""
    return "".join(part[0].upper() for part in display_name.split(" "))


def save_profile(store, user_id, email, display_name=""):
    """Save a user's profile settings and return what was stored."""
    name = display_name.strip()
    profile = {"email": email, "display_name": name, "initials": initials(name)}
    store[user_id] = profile
    return profile
