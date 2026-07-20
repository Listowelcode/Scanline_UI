from services.pipeline import run_pipeline
from jobs.manager import update_job



def process_scan(job_id, youtube_url):

    try:

        update_job(
            job_id,
            {
                "status": "processing",
                "progress": 10,
                "message": "Starting ScanLine pipeline"
            }
        )


        print("WORKER STARTED")


        zip_file = run_pipeline(
            youtube_url
        )


        print(
            "PIPELINE COMPLETE:",
            zip_file
        )



        update_job(
            job_id,
            {
                "status": "completed",
                "progress": 100,
                "message": "Project generated successfully",
                "file": zip_file
            }
        )


        print(
            "JOB UPDATED SUCCESSFULLY"
        )



    except Exception as e:


        print(
            "WORKER ERROR:",
            e
        )


        update_job(
            job_id,
            {
                "status": "failed",
                "progress": 0,
                "message": str(e)
            }
        )