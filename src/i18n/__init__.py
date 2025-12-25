"""
Internationalization (i18n) Manager for AviCut
"""
import json
import os
from typing import Dict, Optional

class I18nManager:
    """Manages language translations for the application."""

    _instance: Optional['I18nManager'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._current_lang = "en"
        self._translations: Dict[str, Dict[str, str]] = {}
        self._load_translations()

    def _load_translations(self):
        """Load all translation files."""
        i18n_dir = os.path.dirname(os.path.abspath(__file__))

        for lang in ["en", "ko"]:
            file_path = os.path.join(i18n_dir, f"{lang}.json")
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    self._translations[lang] = json.load(f)

    @property
    def current_lang(self) -> str:
        return self._current_lang

    def set_language(self, lang: str):
        """Set the current language."""
        if lang in self._translations:
            self._current_lang = lang

    def get(self, key: str, default: str = "") -> str:
        """Get a translated string by key."""
        keys = key.split(".")
        value = self._translations.get(self._current_lang, {})

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, {})
            else:
                return default

        return value if isinstance(value, str) else default

    def t(self, key: str, default: str = "") -> str:
        """Alias for get()."""
        return self.get(key, default)

    def available_languages(self) -> list:
        """Return list of available language codes."""
        return list(self._translations.keys())


# Global instance
_i18n = I18nManager()

def t(key: str, default: str = "") -> str:
    """Convenience function for translation."""
    return _i18n.t(key, default)

def set_language(lang: str):
    """Set current language."""
    _i18n.set_language(lang)

def get_current_lang() -> str:
    """Get current language code."""
    return _i18n.current_lang

def get_manager() -> I18nManager:
    """Get the i18n manager instance."""
    return _i18n
