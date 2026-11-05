# Looking after your site

Choose who in your collective will check backups, apply updates and respond to problems, and make sure someone else can recover access. Keep this guide with your hosting details. Routine work means checking backups, renewing services and applying updates. Restore instructions are under [Recover after a serious failure](#recover-after-a-serious-failure).

With the recommended setup, Coolify and Decidim share one server. Keep the server, Coolify and Decidim updated, and protect both the dashboard settings and your participation data. If you choose [Coolify Cloud](https://coolify.io/docs/core/selfhosted-cloud-comparison), its team maintains the dashboard; you still look after the Decidim server and application.

## Protect your work

We recommend [Hetzner Object Storage](https://www.hetzner.com/storage/object-storage/) for storing backups outside your server. Follow Hetzner's [bucket creation guide](https://docs.hetzner.com/storage/object-storage/getting-started/creating-a-bucket/) and keep the bucket **private**. A bucket is a container for your backup files. Connect it using Coolify's [S3 storage guide](https://coolify.io/docs/core/s3-storage/overview), then select it as the destination for Coolify's own backups.

You need backups of both Coolify and Decidim:

- Follow [Back up Coolify](https://coolify.io/docs/core/backup-and-recovery/instance-backup) to save its settings and recovery key outside the server.
- Follow the [Decidim backup procedure](docs/OPERATIONS.md#backups) for the site's database, uploaded files, queued work and recovery secrets. Keep daily encrypted copies outside the server and check that the backup jobs succeed.

Keep Hetzner's server backups enabled as additional protection. Also keep the complete Decidim backup set: Coolify's own settings backup does not include the application's data.

Connecting storage to Coolify does not automatically back up Decidim. The Decidim backup procedure still requires commands and installation-specific configuration, including transferring its encrypted backup files to storage. A complete guided backup setup is a remaining project gap. A successful backup job confirms that a copy was created; it does not by itself establish that the copy can be restored.

Keep access to Namecheap (or your existing domain provider), Hetzner, Coolify, Resend and recovery credentials in your collective's password manager. Make sure at least two authorised people can access them.

Check that yesterday's backups succeeded. If a backup failed or is missing, follow the error in its log and resolve it before relying on the next backup. This project does not yet automate Decidim backups or failure alerts.

## Keep your domain and email working

Keep the domain's renewal payment details current in Namecheap. Check Resend's sending usage against your plan limits, especially before a large round of invitations or notifications. Keep the sending-domain verification records in DNS when changing other settings.

## Update your site

Choose a time when nobody needs to use the site and take a fresh backup before updating.

For Coolify itself, follow its [update guide](https://coolify.io/docs/core/instance-management/update). For Decidim, read the release notes and follow [Deploying a reviewed upgrade](docs/OPERATIONS.md#deploying-a-reviewed-upgrade), including a trial upgrade using restored data. An application image rollback may not undo database changes.

Afterwards, sign in, open an existing uploaded file and send an administrator invitation. Confirm that the invitation arrives and its link works. Resolve any failure before resuming participation.

## When something goes wrong

| Problem | First check |
| --- | --- |
| The site will not open | Open the address saved in Coolify. Check that its hostname points to your server, uses HTTPS and that the application's components are healthy. |
| An invitation does not arrive | Check spam and the recipient address, then the email delivery status and verified sending domain in Resend. Check worker logs in Coolify if no message appears in Resend. |
| A file is missing | Check the uploads storage and backups before changing settings or redeploying. |
| An update fails | Read the deployment error and follow the [upgrade and recovery procedure](docs/OPERATIONS.md#upgrades-and-rollback). Keep the existing data and volumes. |

When requesting support, record the time, what you tried and the error message. Remove personal data, passwords and recovery keys before sharing logs or screenshots.

## Recover after a serious failure

Recovery means restoring data after a serious incident, such as a lost server, deleted data or an upgrade that cannot be repaired in place. It is not part of initial setup or everyday running. Having backups and saved keys ready is the routine preparation.

If you need to restore, follow [Restore to an isolated application](docs/OPERATIONS.md#restore-to-an-isolated-application). It creates a separate copy so you can check the result before replacing the live site. Keep the original data and volumes until the replacement is verified. For the Coolify dashboard itself, follow [Restore Coolify](https://coolify.io/docs/core/backup-and-recovery/instance-restore).

A planned restore rehearsal is a separate maintenance exercise. The project still needs to validate and simplify this procedure; neither enabling Hetzner backups nor a successful backup job proves that a complete recovery will work.
