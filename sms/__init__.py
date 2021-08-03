"""Main Package"""

# Official Libraries
import os


# Define Shared Constants
__version__ = "0.0.9-18"
"""str: Application version number."""


__app_name__ = "sms"
"""str: Application name."""


__app_base_dir__ = os.path.dirname(__file__)
"""str: Application directory path."""


__project_path__ = os.getcwd()
"""str: Project base directory path."""


HOME = os.environ['HOME']
"""str: user home directory path."""


USER_CACHE = os.path.join(HOME, '.cache')
"""str: user cache directory path."""
