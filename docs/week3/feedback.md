# CleanQ Wireframe Self-Review

## Join Queue (Frames 1 and 2)

**Works well:** The ticket preview shows the next ticket number, kilos × price, total due and estimated pickup right beside the "Create ticket" button, so Mort can check the whole order before he commits. This is visibility of system status, and it follows his rule about few taps and large buttons. On the laptop the preview sits next to the form; on the phone it comes straight after it.

**Problem:** This screen serves two people. The "Already in the queue?" customer lookup sits under a "Staff workspace" order form, and on the phone it is the last thing on a very long page. Kim would have to scroll past a staff form to find it, which breaks her rule about finding her ticket with just her mobile number and one tap. The tab name "Join Queue" also doesn't match the real world (match between system and the real world): customers drop off laundry, and staff create an order.

**Change:** Remove the lookup panel from this screen, since the Customer Dashboard already has one, and rename the tab from "Join Queue" to "New Order" so it matches the "New order" task in Mort's persona.

## Customer Dashboard (Frames 3 and 4)

**Works well:** "Your ticket number is #1053" is the largest text on the page, with Service, Current stage and Estimated pickup in three cards right under it. Kim sees everything she came for within 5 seconds, in plain high-contrast text with no images. This is visibility of system status, and it follows her rules about one-handed use and a lightweight page. On the phone the cards stack in the same order, so the number still comes first.

**Problem:** The "Shop queue" grid shows every other customer's ticket number (1 of 13 up to 13 of 13) and pushes the lookup box to the bottom of the page. For a customer this breaks Kim's rule that she only sees tickets tied to her number, and FR-08. It is also an error-prevention problem, because the design allows what the rules forbid. On the phone she has to scroll past 13 tiles to look up another ticket. The page also has no state for a first-time visitor who hasn't entered a number yet, because it already greets "Hello, Nina!".

**Change:** Split the Dashboard into two views. The customer view shows only her own ticket cards plus one line, "12 tickets ahead of you", which keeps the sense of how busy the shop is without exposing anyone else's ticket. The full grid of ticket numbers moves to the staff view of the same Dashboard (FR-01), where each number opens Manage Queue. In the customer view, move the mobile number lookup to the top of the page as the first thing a visitor sees, with her ticket cards appearing below it after she searches.

## Manage Queue (Frames 5 and 6)

**Works well:** On the laptop, the stage list, the blue "Advance to Drying →" button and the payment actions are in a right-hand column that is visible without scrolling. Finished stages are checked off and the current one is highlighted, so Mort can answer "ready na ba?" in seconds. This is visibility of system status, and it follows his rules about large buttons and showing the current stage clearly.

**Problem:** On the phone, the stage list and the Advance button come after the whole order card, so the action Mort does most often is below the fold. He has to scroll past the name, mobile number and notes every time he wants to move a ticket forward. This is a visibility of system status problem, and it breaks his rule about as few taps as possible with busy hands.

**Change:** On the phone frame, pin a bar to the bottom of the screen with the current stage badge and the full-width "Advance to Drying →" button, so it stays reachable with one thumb while he scrolls. The laptop layout stays as it is, because both actions are already visible without scrolling.