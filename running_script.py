from datetime import datetime, timedelta
from src.pipeline.pipeline_manager import PipelineManager

pipeline = PipelineManager()

# Get articles from the last 30 days
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

df = pipeline.run_pipeline(start_date, end_date, num_pages=3)