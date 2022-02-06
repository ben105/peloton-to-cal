# Peloton to Google Calendar

## Getting Started

This script makes the assumption that it'll be running in Google Cloud, with an authorized service account making changes to your Google Calendar. The way I set this up myself is by deploying this script as a Cloud Function, and run Cloud Scheduler at a certain cadence to update my calendar.

Once you have a service account in GCP, **make sure you give this service account permission to edit events on your Google Calendar**. Navigate to your calendar, tap the 3 dots next to your calendar on the left (you may have to hover the mouse over the calendar name), and choose "Settings and sharing". In the "Share with specific people" section, add your service account's email address (e.g. xxx@appspot.gserviceaccount.com) and give it the "Make changes to events" permissions.

Additionally, create a private key (JSON) for your service account. Move the downloaded key into this folder so it can be referenced by this script. It is referenced as `service_account_key.json` in the `google_cal.py` module.

## Fill in Secrets

You can then fill in the missing details in this script:

- The `SERVICE_ACCOUNT` email address in the `google_cal.py` module.
- Your Peloton username and password in `main.py`
- Your calendar ID in `main.py` (most likely your gmail address)
- And most difficult of all, your Peloton user ID, which I'll explain how to get in the next section.

## Peloton User ID

There is no supported/documented Peloton API, but that doesn't mean you can't copy the same type of network requests that their website makes. It turns out that their website uses an `api.peloton.com` subdomain, so the APIs will have some level of stability to them... famous last words.

Peloton also currently uses GraphQL to fetch data from the backend. The GraphQL query for getting your schedule for the day is in the `peloton.py` module. This is where the user ID is utilized.

To observe what your user ID is, you will have to find this GraphQL query while monitoring the network traffic in your browser's inspector.

What I did was navigate to onepeloton.com and then went to my membership -> profile. Then I clicked on Schedule. I opened the inspector, and then opened the network tab. I cleared the current logs. I then turned on "preserve logs" and clicked on "Your Schedule".

There will be a couple of network jobs named "GraphQL" in the farmost left column. You can look at their payloads, and find the one that has `operationName: "UserScheduledClasses"`. It looks like the browser sometimes sends multiple GraphQL requests for your schedule, and I believe this to be a bug. You should be able to pick any of the "UserScheduledClasses" operations.

In the `variables` section, you can see the `id` variable which is the user ID you need for the `main.py` module.

