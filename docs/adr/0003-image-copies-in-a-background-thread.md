# srcset copies are made in a background thread after upload, never in a page request

The smaller WebP copies of each uploaded photo used to be made the first time a page asked for them. On Runflare, where gunicorn runs sync workers with a 30 s timeout, the home page's first request after a deploy had to resize dozens of photos, ran past the timeout, and every worker was killed: the site returned 502 until the copies were made by hand. Now a page only offers the copies already on disk, and a model schedules its upload's copies with `transaction.on_commit`, which hands them to one daemon thread per process that works through a queue. `manage.py make_image_sizes` makes whatever is missing.

## Considered Options

- **Make copies in the page request (original):** No moving parts, but a page's cost depends on how many copies are missing, and one busy page can take the site down.
- **Make copies synchronously in `save()`:** Off the page path, but an admin save of a gallery inline with twenty photos would run into the same 30 s timeout.
- **Celery, RQ or a cron job:** The robust choice elsewhere, but Runflare runs only gunicorn and nginx, so it would mean new infrastructure for one small job.
- **A thread per upload:** Simple, but twenty uploads would resize twenty photos at once on a small container, slowing every request it serves meanwhile.
- **One background thread per process with a queue (chosen):** No new infrastructure and a bounded cost. The trade-off is that a job is lost if gunicorn restarts the worker before it finishes (a deploy, `max_requests`). That costs only a heavier photo, never a broken page, and the catch-up command makes the missing copies; run it after a deploy that touches images.
