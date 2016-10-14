# Demo

These instructions show you how to update a demo server with the latest version of the code and populate its database with demo data.

Dump data from a live system (creates a `radar.sql` file):

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
