from script import spell1, spell2, get_mode, set_mode

# Toggle checker
if spell1.get(user_id, True):  # Enabled by default
    # do spell check
    pass

# Change search mode
set_mode(chat_id, "inline")
