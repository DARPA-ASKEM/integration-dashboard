def custom_title(s):
    # List of words you want to fully capitalize
    FULL_CAPS = ['pdf', 'amr']

    words = s.replace('_', ' ').split()
    capitalized_words = [word.upper() if word.upper() in FULL_CAPS else word.title() for word in words]
    return ' '.join(capitalized_words)