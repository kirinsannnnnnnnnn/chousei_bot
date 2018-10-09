from flaskr import app
from repository import repository

### for test
import os
os.remove("./repository/sqlite.db")
### for test

repository.create_table("./repository/sqlite.db")
app.run(host='127.0.0.1', port=8080, debug=True)