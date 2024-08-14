# Google Cloud Scheduler

## Create job

```sh
gcloud scheduler jobs create http installments-job
--schedule="0 0 * * *"
--uri="https://fsapi/api/job-name/"
--http-method=GET
--headers=Authorization="Bearer {SECRET_TOKEN}"
--location us-east1
```

## Configure timezone

Go to console under `Cloud Scheduler`

Select created job and `EDIT`

Configure your specific `Timezone`
