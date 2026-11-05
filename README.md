# Decidim for Coolify

**An easier way to set up and run Decidim for your collective.**

Deploy a ready-built Decidim site through Coolify, with a step-by-step guide written for people without technical experience.

We're working to make Decidim **easy for collectives to run** and **better suited to how collectives organise**.

[Start setting up](#before-you-start) · [Expected cost](#what-it-costs) · [Time estimates](#how-long-to-allow) · [Update an existing site](#updating-an-existing-first-attempt)

> **Pilot release:** the full setup journey still needs testing with first-time users. [See what remains to be checked](CONTRIBUTING.md#help-make-setup-ready).

**Help us shape it:**

- **If you're technical,** [help us develop this](CONTRIBUTING.md): simplify setup, improve the tools and make running a site easier.
- **If you're non-technical,** [try setting up a site](#before-you-start) and [share how it goes](#help-improve-this-project). Tell us what feels clear, where you get stuck and what your collective needs. You don't need to finish setup for your feedback to help.

## What it costs

**About €17 per month before tax**, or **€16 if you already have a domain**.

| Item | Monthly cost |
| --- | --- |
| [Hetzner CX33](https://www.hetzner.com/cloud/), including public IPv4 and server backups | About €11 |
| [Hetzner Object Storage](https://www.hetzner.com/storage/object-storage/) for backups outside the server | €4.99, including 1 TB of storage |
| [Domain from Namecheap](https://www.namecheap.com/domains/registration/gtld/org/) | €0 extra if you already have one. Otherwise, a `.org` costs about €17/year at renewal: €17 ÷ 12 ≈ €1.42/month, paid annually.  |
| [Resend email](https://resend.com/pricing) | Likely €0: the free plan includes up to 3,000 emails a month, with a limit of 100 per day. |

## How long to allow

**Allow about 2½ hours of hands-on work to get the site running and test an administrator invitation.** You can split this into shorter sessions. Each estimate below is our best planning estimate for a first attempt; we have not yet timed a complete walkthrough. Troubleshooting can take longer.

| Stage | Estimated hands-on time |
| --- | --- |
| [Register a domain](#get-a-domain-from-namecheap) and [add its DNS records](#connect-your-domain-to-the-server) | 15 minutes |
| [Create the Hetzner server](#1-get-a-server-from-hetzner) and [activate Coolify](#2-activate-coolify), including dashboard settings and Coolify's own backups | 45 minutes |
| [Add Decidim](#3-add-decidim-to-coolify), deploy it and sign in | 30 minutes |
| [Connect Resend](#connect-email), including its sending-domain records | 30 minutes |
| [Create your organisation](#create-your-organisation) and accept the invitation | 30 minutes |
| **Total hands-on setup time** | **2½ hours** |

**Waiting time is separate.** Provider account checks, server startup, deployment and DNS verification can extend the calendar time. Namecheap says new [A records normally take about 30 minutes](https://www.namecheap.com/support/knowledgebase/article.aspx/319/2237/how-can-i-set-up-an-a-address-record-for-my-domain/) to take effect. Resend says [domain verification can take up to 72 hours](https://resend.com/docs/guides/dns/namecheap), though it is often faster. You do not need to stay at your computer while a provider is processing a request.

Before inviting participants, reserve a separate session for the [remaining launch checks](#before-participants-join) and [Decidim backup setup](OPERATIONS.md#protect-your-work). These are additional to the 2½-hour estimate. Backup setup still involves manual commands and connecting backup storage, so we cannot yet give it a useful first-time estimate. Recovery after a failure is outside these estimates.

## Before you start

**For a small collective, we recommend self-hosting Coolify and Decidim on one Hetzner Cloud server.** This keeps the number of services to organise and pay for down. Coolify Cloud is an alternative if you prefer someone else to maintain the Coolify dashboard.

You will need the following. The first setup step explains how to rent the server.

| What you need | What it is for |
| --- | --- |
| A Hetzner Cloud server | A computer rented by the month that stays online and runs your site. Start with the specification below. |
| A domain from Namecheap, or one you already own | Gives participants an address such as `decidim.example.org`, with `coolify.example.org` for the management dashboard. See the domain steps below. |
| An administrator email address | Used for the first Decidim sign-in and the later organisation invitation. |
| A Resend account | Sends invitations, password resets and notifications. Follow [Connect email](#connect-email) before creating the organisation. |
| A shared password manager | Keeps hosting access and recovery credentials available to the people responsible for the site. |

Use the [cost breakdown](#what-it-costs) to budget for the server, domain, outgoing email and backup storage. If you choose Coolify Cloud, you still provide the Decidim server.

### Get a domain from Namecheap

We recommend [Namecheap](https://www.namecheap.com/domains/) if your collective needs a domain, such as `yourcollective.org`. If you already own one, keep it and use its existing DNS provider; you do not need to transfer it.

1. Follow Namecheap's [domain registration guide](https://www.namecheap.com/support/knowledgebase/article.aspx/10072/35/how-to-register-a-domain-name/). Check both the first-year and renewal price. For this setup, purchase the domain only: hosting is on Hetzner, and outgoing email is through Resend.
2. Complete the [contact verification email](https://www.namecheap.com/support/knowledgebase/article.aspx/9305/5/whois-verification-process/) and save your account details. Enable automatic renewal if you want to keep the domain without renewing it manually each year.
3. For a new Namecheap domain, keep **Namecheap BasicDNS** as its nameserver setting. DNS is the address book that connects names to your server. Once you have the server's IP address, add the two records shown below.

In this guide, replace `example.org` with your own domain. You will use `decidim.example.org` for Decidim, `coolify.example.org` for its management dashboard and `notifications.example.org` for sending email. These are parts of the same domain; you do not buy each one separately.

## Set up

### 1. Get a server from Hetzner

Create an account at [Hetzner Cloud](https://www.hetzner.com/cloud/), complete its account and payment checks, then open the [Hetzner Console](https://console.hetzner.com/). Create a project named after your collective and choose **Add server**. Hetzner's [server creation guide](https://docs.hetzner.com/cloud/servers/getting-started/creating-a-server/) shows the screens; use these choices for this project:

| Setting | Choose |
| --- | --- |
| Location | A location near your participants; Germany or Finland are suitable starting choices for European collectives. |
| Server type | **CX33**: 4 vCPUs, 8 GB RAM and 80 GB SSD storage. |
| Image | Under **Apps**, choose **Coolify**. This includes Ubuntu and Coolify, so you do not need to install them separately. |
| Networking | Include a **public IPv4 address**. This is the address you will use to connect your domain. |
| SSH keys | For the browser-console route below, leave this empty. Hetzner will email you the initial server password. |
| Backups | Enable server backups and include their additional cost in your budget. |
| Name | For example, `collective-decidim`. |

**Our provisional minimum recommendation is 4 vCPUs, 8 GB RAM and 80 GB SSD for a small pilot.** vCPUs provide processing capacity, RAM is working memory, and the SSD stores the application, database and uploads. This is a starting recommendation for Coolify and the complete Decidim stack together, not a measured capacity guarantee. We have not yet benchmarked it or established a supported participant count. More activity or uploaded files may require a larger server.

Check the [current price](https://www.hetzner.com/cloud/) before creating the server. Include IPv4, backups and applicable tax in the total. Server billing continues while a server exists, even when powered off.

Choose **Create & Buy** once you have reviewed the cost. Wait for the server to start, then save its public IPv4 address and emailed password in your password manager. Hetzner server backups are useful additional protection; you still need the [application backup guidance](OPERATIONS.md#protect-your-work).

#### Connect your domain to the server

In Namecheap, open **Domain List → Manage → Advanced DNS → Host Records → Add New Record**. Add these records using the public IPv4 address from Hetzner:

| Type | Host | Value | TTL |
| --- | --- | --- | --- |
| A Record | `coolify` | Your server's public IPv4 address | Automatic |
| A Record | `decidim` | The same public IPv4 address | Automatic |

Save both records. Enter only `coolify` or `decidim` in **Host**, rather than the whole domain. Namecheap's [A record guide](https://www.namecheap.com/support/knowledgebase/article.aspx/319/2237/how-can-i-set-up-an-a-address-record-for-my-domain/) shows the screens. If your domain uses another DNS provider, add the records there. Allow time for DNS changes to become visible.

### 2. Activate Coolify

Hetzner's [Coolify app](https://docs.hetzner.com/cloud/apps/list/coolify/) activates when you first log in to the server. You can do this in your browser:

1. In Hetzner Console, select the server and open the **console icon** at the top right. Follow [Using the console](https://docs.hetzner.com/cloud/servers/getting-started/vnc-console/) for screenshots. This opens a text window connected to your server.
2. At the login prompt, enter `root` (the server administrator account), then the password Hetzner emailed you. Password characters are not shown while you type. If prompted to change the password, save the new one in your password manager.
3. Wait for Coolify activation to finish and display its dashboard address. Open that address in another browser tab and immediately create your Coolify administrator account. Save this login separately from the server password.
4. Use the server named **localhost** in Coolify. It means the Hetzner server running Coolify. In **Servers**, open it and complete connection validation if prompted.
5. Save Coolify's recovery key and configure its own backups using [Back up Coolify](https://coolify.io/docs/core/backup-and-recovery/instance-backup). Follow [Update Coolify](https://coolify.io/docs/core/instance-management/update) to check for updates to the preinstalled version.

If activation does not display an address, follow the [Hetzner Coolify instructions](https://docs.hetzner.com/cloud/apps/list/coolify/) before proceeding. For a server with an SSH key already configured, use Hetzner's [connection guide](https://docs.hetzner.com/cloud/servers/getting-started/connecting-to-the-server/).

With the `coolify` DNS record in place, follow Coolify's [dashboard URL settings](https://coolify.io/docs/core/instance-management/instance-settings#url) to set `https://coolify.example.org`. Keep this separate from the participation site address you will set below.

**Checkpoint:** you can sign in to the Coolify dashboard over HTTPS and select **localhost** for deployments. Continue with this project's settings below.

Already have Coolify? Continue below using your existing installation. For another Linux server, follow Coolify's [automated installation guide](https://coolify.io/docs/start-with-self-hosted#automated-installation).

**Alternative: [Coolify Cloud](https://coolify.io/docs/start-with-cloud).** Its team maintains the dashboard; you still provide the Decidim server and look after its application and backups. Follow the Cloud guide to connect your server, then continue below. [Separate self-hosted servers](docs/OPERATIONS.md#hosting-arrangements) are an advanced option.

### 3. Add Decidim to Coolify

Create or open a project and environment in Coolify, then add an **Application from a public Git repository**. Use these settings:

| Setting | Value |
| --- | --- |
| Repository | `https://github.com/jokroese/decidim-coolify` |
| Branch | `main` |
| Server | **localhost** for the recommended one-server setup; your connected server if using Cloud or a separate server |
| Build strategy | **Docker Compose** |
| Base directory | `/` |
| Compose file | `compose.yaml` |
| Raw Compose, Auto Deploy and production previews | **Off** |

Save and load the configuration. Coolify will pull the project's published image; you do not need to fork the repository or supply registry credentials. Updates are deployed deliberately, so a repository change does not interrupt your collective's work.

Coolify's labels vary by version. Its [Compose guide](https://coolify.io/docs/applications/builds/docker-compose) shows the repository and configuration screens.

### 4. Set your site address and deploy

Use the participation address from the [DNS records you added earlier](#connect-your-domain-to-the-server), replacing `decidim.example.org` with your actual hostname.

In Coolify, under **Access → Public access**, add a domain for **web**:

| Field | Value |
| --- | --- |
| Protocol | `https` |
| Domain | `decidim.example.org` |
| Port | `3000` |
| Path | Empty |

Save the domain. If your version uses a single domain field, enter `https://decidim.example.org:3000`. Participants will use `https://decidim.example.org`, without the port. This is the only public-URL setting you need to enter.

In **Environment Variables**, set **`SYSTEM_ADMIN_EMAIL`** to your email address. Keep Coolify's generated credentials unchanged and save them securely for recovery. Leave the three `SMTP_` settings in [Connect email](#connect-email) empty together until you have completed the Resend steps below.

Select **Deploy**. In the application in Coolify, wait until all five components are healthy: web, worker, scheduler, database and Redis. Then open `https://decidim.example.org/system` and sign in as described below.

**Checkpoint:** the Decidim sign-in page opens over HTTPS. If it does not, use [setup troubleshooting](#if-you-get-stuck) before continuing.

### Find your setup credentials

This first account is the **system administrator**, created during deployment. It sets up the organisation; the organisation administrator account for day-to-day participation management comes later. Your Coolify login is separate from both.

1. Open this application in Coolify and select **Environment Variables**.
2. At `/system`, sign in with the address you entered as `SYSTEM_ADMIN_EMAIL` and the generated **`SERVICE_PASSWORD_64_ADMIN`** value. If you have already changed the account password, use your current password instead.
3. Change the initial password and save it in your password manager.

Changing these variables later does not update an existing account or reset its password. Never paste credentials into an issue, screenshot or support message.

## Connect email

We recommend [Resend](https://resend.com/) for invitations, password resets and notifications. Complete this before creating your organisation so its administrator receives the invitation. Use your existing inbox as the administrator email address; these steps configure outgoing site email and do not create an inbox at the sending address. Coolify's own notification settings are separate.

1. Create a Resend account and check its [current sending limits and pricing](https://resend.com/pricing) for your expected usage.
2. In Resend, add **`notifications.example.org`** as a sending domain, replacing `example.org` with your domain. Follow Resend's [Namecheap verification guide](https://resend.com/docs/guides/dns/namecheap) to add the sending DNS records it displays. Use the values from your Resend account. In Namecheap's **Host** fields, omit the final `.example.org`: for example, `send.notifications.example.org` becomes `send.notifications`. If you switch Namecheap to **Custom MX**, retain all MX records used by your existing mailbox provider. Skip the guide's optional receiving-email section.
3. Select **Verify DNS Records** in Resend and wait for the domain to be verified before continuing.
4. In Resend's **API Keys**, create a key named `Decidim` with sending access restricted to `notifications.example.org`. An API key is the secret password your site uses to send email. Copy it into your password manager when it is shown; see [Resend's key guide](https://resend.com/docs/dashboard/api-keys/introduction).

In this application's **Environment Variables** in Coolify, enter:

| Setting | Value |
| --- | --- |
| `SMTP_ADDRESS` | `smtp.resend.com` |
| `SMTP_USERNAME` | `resend` |
| `SMTP_PASSWORD` | The Resend API key you just created |
| `DECIDIM_MAILER_SENDER` | `no-reply@notifications.example.org`, using your verified sending domain |

Keep **`SMTP_PORT=587`** and **`SMTP_TLS=false`**, the project's defaults. These use an encrypted STARTTLS connection supported by [Resend's SMTP service](https://resend.com/docs/send-with-smtp). The SMTP password is your API key, not your Resend account login password.

Save and redeploy. The email setup notice disappears once the three required SMTP settings are present. The administrator invitation in the next step checks actual delivery: confirm it arrives and its link works.

If you already use another email provider, follow the [email configuration reference](docs/CONFIGURATION.md#email-settings) with that provider's settings.

## Create your organisation

Return to `https://decidim.example.org/system` and create an organisation. This is your collective's participation site.

Enter your collective's name and languages. Choose a short name of 3–12 characters and a reference prefix for content identifiers, such as `RCG` for Riverside Community Garden. Use `decidim.example.org` as its hostname, without `https://`, a port or a path.

Enter the organisation administrator's display name and email. They can use the same email address as the system administrator, but these remain separate accounts.

Leave organisation-specific SMTP server credentials blank to use the installation's email settings. If the form asks for a sender address, use the address authorised by your provider.

Create the organisation, then open the administrator invitation email and follow its link to set a password. Use that account at `https://decidim.example.org/admin` for day-to-day administration. Keep `/system` for installation and organisation setup.

**Checkpoint:** the invitation arrives, its link opens your site's HTTPS address and the organisation administrator can sign in. If any part fails, resolve it before inviting participants.

The forthcoming [simpler setup forms](docs/ORGANISATION-SETUP.md) add name suggestions and allow the initial invitation to wait for email setup. Installing the currently pinned image does not yet enable those improvements.

## Before participants join

Complete these checks before opening the site to participants:

- [ ] Receive and accept a real administrator invitation, then sign in.
- [ ] Upload an organisation logo and confirm it remains available after a restart.
- [ ] Check that background jobs and scheduled tasks run successfully.
- [ ] Set up [routine backups](OPERATIONS.md#protect-your-work), save the necessary keys and confirm the backup jobs succeed.
- [ ] Agree who handles updates and problems, and who can recover access if the person who set up the site is unavailable.

Keep [Looking after your site](OPERATIONS.md) as your guide for routine backups and updates. Restoring a site is a separate procedure for serious failures, not an initial setup step.

## If you get stuck

| What you see | What to do next |
| --- | --- |
| The site will not open | Confirm the hostname points to the Decidim server. Check the saved web domain and component health in Coolify. If the browser reports a certificate error, check that the domain points to this server and uses `https`. |
| Deployment stops | Read the configuration error or web runtime log for the setting needing attention. Look up the named setting in the [configuration reference](docs/CONFIGURATION.md). |
| Sign-in fails | Use the [setup credentials](#find-your-setup-credentials) for `/system`. Use the invited organisation account for `/admin`. |
| An invitation does not arrive | Check spam and the recipient address. Check the sending domain and email delivery status in Resend, then the worker logs in Coolify before trying again. |

For help, record what you tried, the time and the error message. Remove passwords, recovery keys and personal data before sharing logs.

## Updating an existing first attempt

Follow [the earlier-pilot upgrade procedure](docs/OPERATIONS.md#updating-an-earlier-pilot), including the Rails secret check **before reloading the configuration**. Keep your existing domain, credentials and stored data. Follow the [release notes](https://github.com/jokroese/decidim-coolify/releases) for what changes in each published image.

## Help improve this project

Tried the setup guide? [Share your experience in an issue](https://github.com/jokroese/decidim-coolify/issues). Tell us what you wanted to do, how far you got, what was confusing and roughly how long it took. We'd also like to hear what would make Decidim more useful for your collective. Plain language is welcome; no technical diagnosis is needed. Leave out passwords and personal data.

[Contributing](CONTRIBUTING.md) covers development and the remaining setup checks. Broader research and experiments live in [Decidim Lab](https://github.com/jokroese/decidim-lab).
