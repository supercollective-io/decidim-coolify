# Contributing

Help collectives set up and maintain Decidim with less technical work. Keep the [setup guide](README.md) focused on their actions; put implementation details here or in the linked technical references.

## Project boundaries

This repository owns the maintained deployment, editable development environment, build tools and regression tests. [Decidim Lab](https://github.com/supercollective-io/decidim-lab) owns research, comparative benchmarks and experiments. The lab records the product commit or image under investigation and reuses `bin/dev` and `bin/check`; it does not maintain a second product development stack.

When an experiment becomes maintained behaviour, keep its implementation and regression tests here. Keep the investigation and comparative results in the lab. Workshop facilitation materials remain in decidim-fest-2026.

## Help make setup ready

Public images are available, but public routing, real email delivery and backup/recovery still need verification on a target Coolify installation. Passing local or CI tests does not establish deployment readiness. Before describing setup as self-service:

1. Publish an image, test its digest and pin it in the deployment configuration.
2. Follow the README on a clean installation with self-hosted Coolify and Decidim on one server. Start with the provisional Hetzner specification in the README. Record the Coolify version, server specification, architecture and combined resource usage; validate or revise the recommendation and correct missing or misleading steps.
3. Complete organisation setup, real email delivery, upload persistence and background-job checks on that installation.
4. Provide and verify a repeatable backup schedule, failure reporting and secret export. Separately rehearse isolated recovery as a maintainer readiness check. Document routine backup setup for collectives and keep restore procedures in incident and maintenance guidance; do not make a recovery rehearsal part of every new installation.
5. Ask a non-technical person outside the development team to follow the setup guide without a technical helper, including its links to Hetzner, Coolify, Namecheap and Resend documentation. Check that they can find the right upstream section, understand their next action and return to the Decidim instructions. Record hands-on time and unattended waiting separately for each stage, including routine backup setup, and revise the README's planning estimates from those observations. Treat any need for undocumented assistance as a gap to fix in the product or instructions.

## Keep setup guidance maintainable

Write for collective members setting up and maintaining their own site without assuming server administration experience. Prefer links to the recommended providers' own setup and maintenance instructions when they are accurate, concise and understandable for the intended reader. Link to the relevant section and say when to return to this guide. Keep this project's choices, Decidim settings and success checks here. Separate initial setup and routine backup checks from recovery after serious failures.

Review linked instructions for assumed knowledge, competing setup paths and unexplained terms. If they are insufficient for a non-technical reader, add the smallest plain-language explanation or procedure needed to complete that part. Explain unfamiliar terms and provide concrete choices and completion checks. Where the product still lacks a guided procedure, record that gap and the work needed to close it; do not make an external expert a permanent prerequisite. Avoid copying upstream commands or entire guides that we would then need to maintain separately. A documentation review does not replace trying the route with its intended users.

## Find the code

| Change | Start here |
| --- | --- |
| Images, installed tools and asset compilation | [Dockerfile](Dockerfile) |
| Coolify settings, roles, storage and startup order | [compose.yaml](compose.yaml) |
| Process startup and administrator creation | [entrypoint](docker/entrypoint), [prepare.rb](docker/prepare.rb) |
| Readiness, worker and scheduler checks | [healthcheck.rb](docker/healthcheck.rb) |
| Recurring jobs | [crontab](docker/crontab), [maintenance.rb](docker/maintenance.rb) |
| Rails configuration and dependency versions | [app/](app/) |
| Editable development environment | [bin/dev](bin/dev), [compose.development.yaml](compose.development.yaml) |
| Check entry points and image selection | [bin/check](bin/check), [tools/image_checks.py](tools/image_checks.py) |
| Deployment validation and runtime checks | [validate.py](validate.py), [tests/](tests/) |
| CI and image publication | [images.yml](.github/workflows/images.yml), [reusable image checks](.github/workflows/verify-image.yml) |

`app/` is the Rails application hosting Decidim. Decidim itself comes from locked upstream gems and frontend packages. Normal builds use the committed application; they do not regenerate it. Ruby and Node base images are pinned by digest. Node and compilation tools are excluded from the production runtime image; the development image includes them.

## Local development

Install Python 3, Git and Docker with Compose 2.32 or later. Start Docker before running these commands from the repository root. Ruby, Node and application dependencies run in containers; the first build needs network access and disk space. macOS with Docker Desktop and Linux Docker hosts are supported.

```sh
bin/dev up
```

This builds the development image, prepares isolated databases and starts Rails, PostgreSQL, Redis, Sidekiq and the asset watcher. It prints the local browser URL and synthetic administrator login. It does not run Decidim's application upgrade task or seed example organisations.

Open the reported URL with `/system` to sign in. Create an organisation for hostname `localhost`. Development email is captured at `/letter_opener`; no real SMTP credentials are needed. The production-only email-pending behaviour is covered by the production image smoke tests, not by development email capture.

Compose Watch synchronises source changes. Refresh the browser after editing a template or after the asset watcher recompiles JavaScript/CSS. Configuration changes restart affected processes; dependency manifest changes rebuild the development image. Installed dependencies remain inside the container. The scheduler is not part of the development stack.

Each worktree has its own Compose project, database, uploads and generated credentials. The browser listens on loopback port 3000. Set `DEV_PORT=3001 bin/dev up` to run a second worktree on a different port. Development credentials live in the ignored `.local/dev/` directory and remain stable across restarts. Do not copy production settings into that directory.

| Command | Result |
| --- | --- |
| `bin/dev up` | Prepare and start the editable environment, then watch source changes |
| `bin/dev logs` | Follow this worktree's service logs |
| `bin/dev logs web` | Follow one service's logs |
| `bin/dev down` | Stop this worktree's environment and keep its data |
| `bin/dev reset --yes` | Delete this worktree's development data and generated credentials |

Reset is destructive only to this development project. Use it deliberately; a normal restart does not require resetting data. Never use production volumes for development.

### Verify a browser change

1. Sign in at `/system`, including an unsuccessful attempt before the successful one.
2. Create an organisation, check validation messages and follow its administrator invitation from `/letter_opener`.
3. Use the keyboard to reach and operate the changed controls. Repeat organisation creation with JavaScript disabled, using another disposable organisation.
4. Edit a template and a JavaScript/CSS source file; confirm the changes appear after refresh without rebuilding the production image.
5. Restart the stack and confirm the organisation and an uploaded logo remain. Record any unverified step in the contribution.

If startup fails, read the named service's logs. An occupied browser port requires a different `DEV_PORT`; a Docker connection error requires starting Docker. Fix the failing source or configuration before retrying. `bin/dev --help` lists the supported commands. The generated application-level setup helpers are not a second supported development workflow.

## Build and check a change

Run checks from the repository root. The same entry points are used locally and in CI:

```sh
bin/check quick
bin/check full
```

`quick` checks internal documentation links and anchors, Compose configuration, Python contracts, Ruby unit behaviour and JavaScript organisation-name suggestions. Ruby and Node use the locked development tool image; quick checks do not start application services or compile production assets. The initial tool-image build can take time; subsequent runs reuse Docker build layers.

`full` runs quick checks, builds the production image and runs the image-level tests and full disposable smoke stack. Each build has a unique tag, and subsequent tests use the captured immutable image ID. Concurrent worktrees cannot silently replace each other's tested image. Output records the checkout revision, whether it has changes, the image ID and the selected platform.

Local builds default to the Docker host's architecture. To test another supported platform explicitly:

```sh
bin/check full --platform linux/amd64
bin/check full --platform linux/arm64
```

Emulation is slower. Release CI retains native amd64 and ARM64 jobs and uses `bin/check image` against each built image. To verify an existing local image or published digest, use `bin/check image --image IMAGE_REFERENCE --platform linux/amd64`, replacing `IMAGE_REFERENCE` with the actual reference. A supplied image ID must already exist for the requested platform; a published reference can be pulled.

Changes limited to root Markdown files and Markdown under `docs/` run documentation checks without building the application. Changes limited to `compose.yaml` and those documents run quick checks and verify the pinned registry image on both native architectures; they do not build or publish a new application image. All other changes, release tags and manual runs include quick checks and new builds on both architectures. Use the always-running `CI` check for branch protection: it fails if change detection, documentation or required quick/container checks fail.

The smoke test starts web, worker, scheduler, PostgreSQL and Redis in a uniquely named disposable project. It supplies its own settings; it does not read the project's `.env`. It checks migrations, administrator bootstrap, sign-in and organisation requests, health, assets, API documentation, scheduled tasks, worker processing and upload persistence. It verifies both missing and configured SMTP behaviour without sending real email. Each checkpoint reports elapsed time.

Expect exit status 0 and passing checks. On failure, read the first failing check and service logs. Cleanup removes only the test's own project and volumes; failures to clean up are reported. Never remove another project's volumes. Direct invocation of `tests/smoke.py` requires an explicit `SMOKE_IMAGE` and accepts `SMOKE_PLATFORM`.

The production smoke loop has no browser port and does not establish working Coolify routing, real email delivery or recovery. Use an isolated Coolify pilot for the [manual setup checks](README.md#set-up). The editable development environment above serves a different purpose and does not replace release verification.

For documentation alone, run `bin/check docs`. It uses a pinned Lychee container with networking disabled to check tracked Markdown and local heading anchors. External URLs are excluded; the initial checker-image pull requires network access. Add new Markdown files to Git's index before checking them.

For optional Ruby style and security checks, run the application's `bin/ci` inside the development image. These checks remain separate from release CI.

## Choose checks for the change

| Change | Verification |
| --- | --- |
| Documentation only | `bin/check docs`; check documented commands against the source |
| Compose, configuration or release references | `bin/check quick`; full image checks if runtime behaviour changes |
| Application, dependencies, Dockerfile or process scripts | `bin/check full`; manually inspect changed browser behaviour |
| Development environment or command launchers | Quick checks plus clean startup, edits, restart and worktree-isolation checks |
| Coolify setup, email or recovery | Complete the affected procedure on an isolated installation and record the result |

Include the problem, resulting behaviour and any setup changes a collective must make in your contribution. Link the relevant [CI run](https://github.com/supercollective-io/decidim-coolify/actions/workflows/images.yml) for automated results. Record manual checks and remaining limits in the PR description or release notes; identify the tested revision/image and architecture for runtime or deployment checks. Keep durable procedures and known limitations in the relevant guide, rather than maintaining a test-run diary.

## Source and generated files

Commit configuration, custom code, asset entry points, dependency manifests and lockfiles, installed migrations, required scripts and the licence. Keep secrets, installed dependencies, caches, logs, uploads and generated assets out of Git and the build context.

Preserve installed engine migration filenames. Regenerating migrations can give them new timestamps and make Rails attempt changes again.

The build runs `deployment:check_migrations` against the locked bundle before compiling assets. It checks that loaded Decidim engines' schema migrations exist locally and their upstream data migration paths are registered. It does not compare historical file contents or query a database. Decidim 0.32 loads data migrations from its gems; local copies are unnecessary.

The build also runs `decidim_api:generate_docs`. Its output in `app/app/views/static/api/docs/` is excluded from Git and the build context, included in the final image and served at `/api/docs`. With the application bundle and configuration available, regenerate it from `app/` using `bundle exec rails decidim_api:generate_docs`.

## Preparing a Decidim upgrade

Use a development checkout with the target release's Ruby and Node versions, Bundler, npm and application dependencies installed. Configure that checkout for an isolated development or restored test database. Keep production credentials out of this environment. These commands run from `app/`; use a development bundle that permits dependency updates, not the production image's frozen bundle.

1. Read the [Decidim release notes](https://github.com/decidim/decidim/releases) for each required upgrade step. Follow the supported version sequence and any release-specific actions. Update the Decidim version pins in `Gemfile`, including `decidim-dev` and any optional Decidim modules.
2. Update the bundle and run Decidim's application upgrade task:

   ```sh
   bundle update decidim
   bin/rails decidim:upgrade
   ```

   The upgrade task imports missing schema migrations. In Decidim 0.32.1 it can also patch historical migration contents and update frontend configuration. Preserve existing migration filenames and review every change. Do not delete and regenerate the migration directory. Changes to an already-applied migration do not rerun that migration on an existing database; follow the release notes for any required corrective action.

3. Check that every `@decidim/*` dependency in `package.json` matches the selected Ruby Decidim release. Correct any version drift introduced by the generator, then update the npm lockfile and check migration completeness:

   ```sh
   npm install
   bundle exec rails deployment:check_migrations
   ```

   Expect a `PASS` message with schema and data migration counts. A missing schema migration requires importing and reviewing the upstream migration. An unregistered data migration requires correcting the engine initialisers or data migration paths. Decidim 0.32 registers `db/data` directories inside the installed gems; do not copy those files into the app to satisfy the check. The check compares migration names and engine scopes, allowing the local timestamps assigned by Rails. It does not compare historical migration contents or query the database.

4. Review and commit the manifests, lockfiles, imported migrations and required application configuration together. Run the local build and checks in [Build and check a change](#build-and-check-a-change). The Docker build repeats the completeness check against its locked production bundle and fails before asset compilation if migrations are missing.
5. Rehearse the new image against an isolated restore before production deployment. Image startup runs `db:migrate` followed by `data:migrate`. If testing directly from the development checkout, apply them to the isolated database with:

   ```sh
   bin/rails db:migrate
   bin/rails data:migrate
   ```

   Confirm both commands succeed and complete any release-specific data repair tasks. Verify the affected application behaviour as well as the smoke checks. Then follow the [technical deployment and rollback procedure](docs/OPERATIONS.md#upgrades-and-rollback).

## Publishing a release

Application changes merged into `main` automatically produce tested images and one release-selection PR. Collectives pull the shared image; they do not build or publish it. Image publication and merging the PR do not deploy a running installation.

### Configure release automation

Repository maintainers complete this setup once:

1. In the repository's **Settings → Actions → General → Workflow permissions**, enable **Allow GitHub Actions to create and approve pull requests**. An organisation policy may need to permit this setting. The workflow uses the built-in `GITHUB_TOKEN` with Contents and Pull requests write permissions only in the proposal job. No release App, client ID or private key is needed; the workflow does not approve or merge its own PRs.
2. Keep review and the `CI` status check required on `main`. Allow the workflow to maintain its `update-application-image` PR branch. GitHub requires a person with repository write access to approve workflow runs triggered by the built-in token's PR creation or updates; see [GitHub's workflow-trigger guidance](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow).
3. Ensure Actions can publish the repository's GHCR package. Make the package public before accepting its first release-selection PR, so collectives and unprivileged PR checks can pull it anonymously. After the ownership transfer, the workflow publishes to `ghcr.io/supercollective-io/decidim-coolify`; the old image pin remains until the first reviewed update is merged.

Dependabot maintains GitHub Actions versions and commit pins on its weekly schedule. It no longer discovers this project's application image: the publication workflow already knows the exact tested digest. PostgreSQL, Redis and application dependency upgrades remain separate work.

### Review and select an image

1. Merge the reviewed application change into `main`. The workflow builds native amd64 and ARM64 candidate images with source metadata, SBOMs and provenance. Candidate tags contain the workflow run, attempt and architecture; their presence in GHCR does not establish a successful release.
2. Wait for quick checks and both registry-digest smoke tests to pass. Docker Buildx assembles the tested architecture images without rebuilding application layers, then publishes `sha-<full-source-commit>`. Confirm **Publish tested multi-architecture image** and **Propose the tested image on main** succeed; a green `CI` check alone does not establish publication. The workflow summary records the immutable digest. A failed architecture check prevents release publication and a new update proposal.
3. Review the automated **build(coolify): select tested application image** PR. It updates only the shared image reference in `compose.yaml`, names the source revision and links the successful publication run. Later successful builds update the same PR. Click **Approve workflows to run** on the PR when GitHub requests it, including after automated updates. Its checks verify the selected digest against the current Compose configuration on both architectures. Review the application changes and document migration or configuration requirements before merging.
4. Merge the PR after its checks and review pass. The resulting deployment commit selects the image for new installations and upgrades. An image-selection commit does not publish another image. Application source on `main` may be newer than the selected image; use the image's source tag and PR evidence to determine what is included.
5. Give the person applying the update the exact deployment commit and release notes, including required settings and migration actions. Follow the [manual deployment procedure](docs/OPERATIONS.md#deploying-a-reviewed-upgrade). Keep Coolify Auto Deploy disabled.

The workflow uses Docker's official build and metadata actions, Buildx manifest assembly and [Create Pull Request](https://github.com/peter-evans/create-pull-request). The only repository-specific edit is the validated shared image anchor in `pin_release.py`. The automation branch is an ordinary PR branch, not a deployment branch; Coolify continues to read reviewed revisions on `main`.

### Retries, manual builds and version tags

Use **Container image → Run workflow** on `main` to publish and propose the current source again, including after enabling PR creation or making the package public. A rerun may produce a different digest because build-time operating-system packages can change; digests, rather than SHA tags alone, identify exact image contents. Existing deployed digests remain unchanged.

Manual runs on other branches and `v*` tag pushes also build, test and publish images, but do not update the release-selection PR. Version-tag runs add the version tag alongside the source tag. These are explicit publication operations, not automatic selection of an older release for `main`.

Publication uploads a `deployment-compose` workflow artefact containing the source revision's Compose definition pinned to its published digest. Download it for inspection or recovery while it remains available; it is not the primary installation route. `.dockerbuild` artefacts are diagnostic records, not pullable images.

If publication succeeds but PR creation fails, the workflow remains failed and the committed deployment pin is unchanged. Fix the reported permissions or configuration and rerun. If application source has advanced, the old run leaves the update PR unchanged; allow the newer build to finish. Documentation-only and Compose-only commits do not invalidate an application build, and the PR checks still verify the current configuration. Concurrent proposal jobs are serialised.

Do not delete images used by installations or recovery records. Candidate and release images accumulate in GHCR; this change does not introduce automatic registry cleanup. Local and CI smoke tests do not establish Coolify routing, real email delivery or recovery.

## Technical references

- [Configuration](docs/CONFIGURATION.md): required values, defaults and generated credentials.
- [Operations](docs/OPERATIONS.md): deployment, backups, recovery and maintenance checks.
- [Organisation setup contract](docs/ORGANISATION-SETUP.md): behaviour, tests and local override responsibilities.
- [Setup research and upstream plan](https://github.com/supercollective-io/decidim-lab/blob/main/research/organisation-setup.md): evidence, proposed contributions and their status.
- [Upstream decisions](UPSTREAM.md): why this project maintains an image and when to revisit it.
- [Dependency audit](DEPENDENCY-AUDIT.md): dated findings and follow-up work.
- [Decidim 0.32.1 release](https://github.com/decidim/decidim/releases/tag/v0.32.1) and [versioned installation guidance](https://github.com/decidim/decidim/blob/v0.32.1/docs/modules/install/pages/index.adoc).
