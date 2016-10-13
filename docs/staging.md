# Staging

These instructions show how to deploy to a staging server and populate it with test data.

Build the code (see the "Build" section of the [README](../README.md)).

Deploy the code (see the "Deploy" section of the [README](../README.md)):

```sh
fab -H nww.staging.radar.nhs.uk -u root deploy
```

Create the test data:

```sh
fab -H nww.staging.radar.nhs.uk -u root staging
```
