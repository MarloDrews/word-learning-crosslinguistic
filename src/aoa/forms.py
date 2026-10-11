"""CDI forms per language. Which forms count, and which one sets the word list."""

# Full forms only. The short forms are separate instruments with around 100 items, Braginsky leave them out too
# Dutch has more forms in Wordbank, the others besides WG and WS are different instruments.
FORMS = {
    "eng": ("WG", "WS"),
    "spa": ("WG", "WS"),
    "fra": ("WG", "WS"),
    "ita": ("WG", "WS"),
    "hrv": ("WG", "WS"),
    "nld": ("WG", "WS"),
    "fin": ("WGProd", "WS"),
    "deu": ("WS",),
    "hun": ("WS",),
    "est": ("WS",),
}

# None keeps every word item, these languages have no WG form
WORD_LIST_FORM = {
    "eng": "WG",
    "spa": "WG",
    "fra": "WG",
    "ita": "WG",
    "hrv": "WG",
    "nld": "WG",
    "fin": "WGProd",
    "deu": None,
    "hun": None,
    "est": None,
}