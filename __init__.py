from .track_manager import TrackManager
from .collection_manager import CollectionManager

# set the database file paths
track_db_file = "data/track_data.db"
#collection_db_file = "data/collection_database.db"

# create and initialize the managers
track_manager = TrackManager(track_db_file)
#collection_manager = CollectionManager(collection_db_file)