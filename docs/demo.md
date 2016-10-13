# Demo

These instructions show how to deploy to a demo server and populate it with demo data.

Dump data from a live system (creates a `radar.sql.gz` file):

```sh
fab -H nww.radar.nhs.uk -u root dump
```

Build the code (see the "Build" section of the [README](../README.md)).

Deploy the code (see the "Deploy" section of the [README](../README.md)):

```sh
fab -H demo.radar.nhs.uk -u root deploy
```

Create the demo data:

```sh
fab -H demo.radar.nhs.uk -u root demo
```
