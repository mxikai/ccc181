# CleanQ Accessibility Check (Part 9)

Screens tested (Lighthouse, Accessibility + Mobile, run in Chrome DevTools):

| Screen in assignment | CleanQ screen | URL tested |
| --- | --- | --- |
| Join | New Order | /join |
| My place | Customer Dashboard (lookup, results and ticket page) | /track, /track?phone=09171234567, /track/1 |
| Staff | Dashboard | /staff |

Bonus screens: Manage Queue (/queue/6) and the home page (/).

## 9a. Lighthouse

| Screen | First score | Final score | Performance | Best Practices | SEO | Screenshot |
| --- | --- | --- | --- | --- | --- | --- |
| Join (/join) | 95 | 100 | 99 | 100 | 90 | screenshots/lighthouse_join.png |
| My place: lookup (/track) | 100 | 100 | 97 | 100 | 90 | screenshots/lighthouse_track.png |
| My place: results (/track?phone=...) | 100 | 100 | 99 | 100 | 90 | screenshots/lighthouse_track_results.png |
| My place: ticket (/track/1) | 100 | 100 | 99 | 100 | 90 | screenshots/lighthouse_myplace.png |
| Staff (/staff) | 100 | 100 | 98 | 100 | 90 | screenshots/lighthouse_staff.png |
| Bonus: Manage Queue (/queue/6) | 96 | 100 | 99 | 100 | 90 | screenshots/lighthouse_manage.png |
| Bonus: Home (/) | 100 | 100 | 96 | 100 | 90 | screenshots/lighthouse_home.png |

**Issues found and fixes**
- Join (95): "Background and foreground colors do not have a sufficient contrast ratio." The failing items were the service name, turnaround text and price inside the service buttons. Bootstrap's `btn-outline-primary` used a lighter default blue. Fixed by setting a darker text color (#1d4ed8) for `.btn-outline-primary` in style.css, and by removing `opacity-75` from the turnaround text.
- Ticket page had no `<h1>`: added a visually hidden `<h1>My ticket status</h1>`.
- Small buttons were under 44 px tall on phones: added a 44 px minimum for `.btn-sm` below 768 px.
- SEO: added a meta description in `base.html`.
- Navigation: the "Manage Queue" tab only appeared after opening a ticket, so staff could not reach it from other pages. It is now always in the staff menu (it opens the oldest active ticket), and the Dashboard has a "Manage" button on each row.
- Manage Queue (96): "Background and foreground colors do not have a sufficient contrast ratio." The failing item was the "Mark as paid" button, which used Bootstrap's light gray `btn-outline-secondary`. Changed it to `btn-outline-primary`, which uses the darker blue (#1d4ed8) set in style.css.

**Score notes**
- Manage Queue (96): the only failing item was the "Mark as paid" button contrast. Fixed as described above.
- Performance items about render-blocking requests come from loading Bootstrap from a CDN. They are not part of the accessibility check, and every performance score is 96 or higher.

## 9b. Keyboard-only test

Tested with Tab, Shift+Tab, Enter, Space and arrow keys only, mouse put away.

**Flow 1: create an order from the home page**
1. First Tab on `/` shows the "Skip to main content" link: ✅
2. Tab to "Staff? Create a new order" and press Enter: ✅
3. Tab through name, mobile, service (arrow keys choose a radio), weight, payment (arrow keys change the select), notes: ✅
4. Enter on "Create ticket" opens Manage Queue with a success message: ✅
5. Focus visible at every step: ✅

**Flow 2: staff dashboard**
1. Tab to a service in the filter bar and press Enter: ✅
2. "Start next load" moves a ticket to Washing: ✅
3. "Advance" buttons work with Enter, up to "Mark claimed", and the ticket appears in "Claimed today": ✅
4. Focus visible at every step: ✅

**What failed and how I fixed it**
- The Manage Queue tab was missing from the menu until a ticket was open. Fixed by always showing it.
- After the last control on a page, Tab moves focus into the browser (address bar, tabs), so nothing on the page looks highlighted. This is normal browser behavior. Tab again wraps back to the skip link, and Shift+Tab goes backwards.
- Radio groups and selects need arrow keys once focused, not repeated Tab. This is standard behavior, so no change was needed.

## 9c. Manual checklist

| Check | Join | My place | Staff |
| --- | --- | --- | --- |
| Every input has a visible label | ✅ every field has a `<label>` or `<legend>` | ✅ "Your mobile number" label | ✅ no text inputs; filter links and buttons have visible text |
| Error messages say what to do, in text | ✅ e.g. "Enter the weight in kilos, between 0.1 and 50." under each field | ✅ "Please enter a valid mobile number, like 0917 123 4567." | ✅ no forms to fill in; actions confirm in text ("Ticket #3 moved to drying.") |
| Status is shown in words, not only color | ✅ Paid / Unpaid is a word | ✅ badge says "Folding", "Ready", etc., plus a sentence | ✅ badges and "Waiting for pickup" are text |
| Text and buttons readable at 375 px, no sideways page scroll | ✅ | ✅ | ✅ (tables and filter bar scroll inside their own boxes) |
| Buttons at least about 44 × 44 px on a phone | ✅ "Create ticket" is `btn-lg` | ❌ "Leave the queue" was `btn-sm`. Fixed with a 44 px minimum on phones | ❌ table buttons were `btn-sm`. Fixed with a 44 px minimum on phones |
| One `<h1>` and headings in order | ✅ | ❌ ticket page had no `<h1>`. Fixed with a visually hidden `<h1>` | ✅ h1, then h2 "Claimed today" |
| `<html lang="en">` is set | ✅ set once in base.html | ✅ | ✅ |

## What is left and why

- Flash-message close buttons ("x") are smaller than 44 px. This is Bootstrap's default, and the message text is readable without it.
- Manage Queue: nothing left after the button fix (update this if the re-run still lists anything).
- Performance is slightly under 100 because Bootstrap loads from a CDN. I left it because this check is about accessibility.