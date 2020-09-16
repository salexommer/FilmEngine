# Initial filmengine script that will be split into separate modules later
from kaggle.api.kaggle_api_extended import KaggleApi
api = KaggleApi()
api.authenticate()

 Download all files of a dataset
# Signature: dataset_download_files(dataset, path=None, force=False, quiet=True, unzip=False)
api.dataset_download_files('avenn98/world-of-warcraft-demographics')

# downoad single file
#Signature: dataset_download_file(dataset, file_name, path=None, force=False, quiet=True)
api.dataset_download_file('avenn98/world-of-warcraft-demographics','WoW Demographics.csv')