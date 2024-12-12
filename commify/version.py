import requests
__version__ = "1.4"


def get_pypi_version(packagename: str):
    try:
        response = requests.get(f"https://pypi.org/pypi/{packagename}/json").json()
        return response["info"]["version"]
    except requests.RequestException as e:
        print(f"Error: Failed to get PyPI version. Detailed error: \n{e}")
    
latest_version = get_pypi_version('Commify')

def check_version():
        try:
            if __version__ != get_pypi_version('Commify'):
                print(f'New Commify version available: {latest_version} (current: {__version__})! ‖ pip install -U Commify\n')
        except Exception as e:
            print(f'Error: Failed to check Commify version. Detailed error: \n{e}')
