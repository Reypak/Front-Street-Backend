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

## Schedule Format

### Every day at 9AM

`0 9 * * *`

```
0: This specifies the minute (0-59). In this case, it's the 0th minute of the hour.
9: This specifies the hour (0-23). In this case, it's 9 AM.
*: This represents any day of the month (1-31).
*: This represents any month (1-12).
*: This represents any day of the week (0-6, where 0 is Sunday).
```
