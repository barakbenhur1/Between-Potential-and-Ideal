# Between Potential and Ideal — Static Theory Website

No build tools. No dependencies. Static HTML/CSS/JS.

## Important
The discussion button now links to `discussion.html` directly. It does not depend on `mailto`, scrolling, or JavaScript.

## Deploy on Render
- Build command: `echo static`
- Publish directory: `theory-site-static` if this folder is inside your repo root, or `.` if these files are the repo root.


## Visitor counter
This version includes a simple public visitor counter.
It uses CounterAPI V1 from the browser, because this is a static site with no backend.
The counter increments at most once per browser per ~24 hours using localStorage, so refreshes do not keep increasing the number from the same browser.

Counter namespace/key used in the code:
- Namespace: `between-potential-and-ideal`
- Counter name: `site-visits`

To reset or change the counter, edit the `namespace` and `counterName` values inside `index.html` and `discussion.html`.
