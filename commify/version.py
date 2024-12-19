try: # fix a github actions bug
    import requests
except ImportError:
    requests = None

__version__ = "1.5"


def _get_pypi_version(packagename: str):
    if requests is not None: # that also fixes
        try:
            response = requests.get(f"https://pypi.org/pypi/{packagename}/json").json()
            return response["info"]["version"]
        except requests.RequestException as e:
            print(f"Error: Failed to get PyPI version. Detailed error: \n{e}")
    else:
        return 'Error: module "requests" is not installed.'
    
latest_version = _get_pypi_version('Commify')

def _check_version():
        try:
            if __version__ != _get_pypi_version('Commify'):
                print(f'New Commify version available: {latest_version} (current: {__version__})! ‖ pip install -U Commify\n')
        except Exception as e:
            print(f'Error: Failed to check Commify version. Detailed error: \n{e}')
