from Analytics.Analyzer import Analyzer

## THIS IS FOR ANALYZING DATA FROM SQL
## Route for getting data for dongleID
@app.post("/{dongleID}")
def get_data() -> None:
    return None