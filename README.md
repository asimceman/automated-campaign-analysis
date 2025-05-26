# Automated Campaign Analysis

**Automated Campaign Analysis** is a full-stack application for auditing digital ad campaigns using custom thresholds and AI-generated insights. It includes a modern Vue 3 frontend powered by PrimeVue and a FastAPI backend with SQLAlchemy ORM and alembic for migrations, and it provides OpenAI/OpenRouter integration.

# Demo

Short demo can be found in the [Google Drive](https://drive.google.com/drive/folders/1Kze3J8I4-f6RA1Gwh2NDdkZldDtG5UWX?usp=drive_link)

# Dataset

The dataset being used in the POC version is [Marketing Campaign Performance Dataset](https://www.kaggle.com/datasets/manishabhatt22/marketing-campaign-performance-dataset?resource=download) with a couple of tweaks and different assumptions. We took the subset of 200 rows from the mentioned dataset and removed the columns 'Company', 'Campaign_Type', 'Duration', 'Customer_Segment'. With those modifications we are treating every row as a daily report for the campaign.

We are analyzing the dataset against the manually sent thresholds that can be found in the `Backend/app/analyzers/campaign_thresholds.json` file. For the purpose of this POC we are analyzing the campaign data against 4 threshold fields: conversion_rate, roi, engagement_score and acquisition_cost. We are checking the values of those fields and comparing them to the threshold with 2 operations:

1. gt -> Rows that exceed the threshold value will be flagged
2. lt -> Rows that have the value less than the threshold will be flagged.

When running the campaign analysis the whole dataset is fed to the LLM (we are using `mistralai/devstral-small:free` model) and the agent returns us the insights and recommendations for the campaign if atleast one threshold is broken.

Using Mailgun we then send an email to the specified recipient. In the email we send insights, link to the UI dashboard and recommendations that were created by the LLM.

## Acquiring API keys and installing needed utilities

### OpenRouter

This application integrates the [OpenRouter](https://openrouter.ai/) LLM in order to provide recommendations and insights about the campaign that is being analyzed. In order for application to run successfully you need to obtain the API Key on their webpage.

1. Create an account on their website
2. Create an API key [here](https://openrouter.ai/settings/keys)
3. Store the generated API key in the `Backend/.env.sample` file in the field `OPENAI_API_KEY`

### Mailgun

This application integrates the [Mailgun](https://app.mailgun.com/) service. When the analysis finds significant results, it will send the notification to the specified email. In order for application to work you need to do the following steps:

1. Create an account on their website
2. Activate your account in the `Get started section`
3. Create an API key [here](https://app.mailgun.com/settings/api_security?onboardingTask=api-key)
4. Store the generated API key in the ` Backend/.env.sample`` file in the field  `MAILGUN_API_KEY`
5. Copy the [domain](https://app.mailgun.com/mg/sending/domains) on the website and store it in the ` Backend/.env.sample`` file in the field  `MAILGUN_DOMAIN`
6. In the Domain settings add authorized recipient (the one to whom you will send an insight email) and store the email address in the in the ` Backend/.env.sample`` file in the field  `RECIPIENT_EMAIL`

### Docker

The web application is dockerized so in order to streamline the process and not having to run multiple commands explicitly, please install the [Docker desktop](https://www.docker.com/products/docker-desktop/).

### Make

In order to run the Makefile commands, that will run the application from one command, you need to install `make`.
If you are running the Git Bash or if you are running the terminal on Linux or MacOS, it is possible that you already have `make` installed. Please check it using the command:

```shell
make --version
```

If the version is logged you can skip the installation in the next step.

The easiest way to install `make` is using [Chocolatey](https://chocolatey.org/install) and then running

```shell
choco install make
```

### npm

We need to install node and npm. The installation can be found on the [site](https://nodejs.org/en). Run the installer — it will install both Node.js and npm.

## Running the app

To get a local version running with Docker Compose do the following:

1. Position your terminal in the /Backend folder:

   ```shell
   cd Backend
   ```

2. Copy `.env.sample` (that you have populated with your API keys like described in the previous section) to `.env`

   ```shell
   cp .env.sample .env
   ```

3. Position your terminal back on the main level:

   ```shell
   cd ..
   ```

4. Now we want to run the Makefile command that is going to:
   1. Compose the fastAPI backed and Postgresql database in Docker
   2. Run the migrations on the database
   3. Seed the data in the database
   4. Run the frontend app

Run the application by using the command:

```shell
make start
```

5. Now you can access the UI on port `http://localhost:5173/` (if you haven't changed it in the environment variables)
