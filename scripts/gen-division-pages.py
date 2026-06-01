#!/usr/bin/env python3
"""Generate MDS division Layer 2 pages from one template, cloned off mds-reception.html."""
import os

ROOT = os.path.expanduser("~/MDS/mds-diversified")

# shared inline SVGs (24x24 stroke)
IC = {
  "phone":'<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.95.36 1.88.7 2.77a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.31-1.31a2 2 0 0 1 2.11-.45c.89.34 1.82.57 2.77.7A2 2 0 0 1 22 16.92z"/>',
  "refresh":'<path d="M3 12a9 9 0 0 1 15-6.7L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-15 6.7L3 16"/><path d="M3 21v-5h5"/>',
  "chat":'<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>',
  "users":'<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9"/><path d="M16 3.1a4 4 0 0 1 0 7.8"/>',
  "star":'<path d="M12 2l3 7 7 .5-5.5 4.5L18 21l-6-3.7L6 21l1.5-7L2 9.5 9 9z"/>',
  "doc":'<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/>',
  "mega":'<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
  "pen":'<path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.1 2.1 0 0 1 3 3L12 15l-4 1 1-4z"/>',
  "globe":'<circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15 15 0 0 1 0 20 15 15 0 0 1 0-20z"/>',
  "clock":'<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
  "inbox":'<path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5 5h14l3 7v6a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-6z"/>',
  "book":'<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
  "search":'<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
  "bulb":'<path d="M9 18h6"/><path d="M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.3 1 2.1V18h6v-1.2c0-.8.4-1.6 1-2.1A7 7 0 0 0 12 2z"/>',
  "chart":'<path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/>',
}

def feat(ic, h, p):
    return f'<div class="feat"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{IC[ic]}</svg></div><h3>{h}</h3><p>{p}</p></div>'

def step(n, h, p):
    return f'<div class="step"><div class="n">{n}</div><h3>{h}</h3><p>{p}</p></div>'

def faq(q, a):
    return f'<details><summary>{q}</summary><p>{a}</p></details>'

def bubbles(rows):
    # rows: list of (side, who, text); side 'them' or 'ai'
    out = ""
    for side, who, text in rows:
        out += f'<div class="bubble {side}"><span class="who">{who}</span>{text}</div>'
    return out

def checklist(title, time, items, outcomes):
    rows = "".join(f'<div class="bubble ai" style="margin-left:0;max-width:100%"><span class="who">{w}</span>{t}</div>' for w,t in items)
    oc = "".join(f'<span>{o}</span>' for o in outcomes)
    return (f'<div class="callcard"><div class="ch"><span class="live">{title}</span><span class="time">{time}</span></div>'
            f'{rows}<div class="outcome">{oc}</div></div>')

def callmock(title, time, rows, outcomes):
    oc = "".join(f'<span>{o}</span>' for o in outcomes)
    return (f'<div class="callcard"><div class="ch"><span class="live">{title}</span><span class="time">{time}</span></div>'
            f'{bubbles(rows)}<div class="outcome">{oc}</div></div>')

# ---- per-division data ----
DIV = {}

DIV["recover"] = dict(
  name="MDS Recover", short="Recover", accent="#ff3d9c", argb="255,61,156", adeep="#c61f72",
  title="MDS Recover · Chase every quote, win back every lead",
  desc="MDS Recover automatically follows up every quote, revives dead leads and reactivates old customers, so the jobs you already earned never slip away. Part of MDS Diversified.",
  kicker="MDS Recover · Follow up &amp; Recovery",
  h1a="Chase every quote.", h1b="Win back every lead.",
  lede="Most jobs are won on the follow up, not the first call. MDS Recover chases every quote, revives dead leads and reactivates old customers automatically, so nothing you already earned slips through the cracks.",
  micro="Follows up automatically · Politely persistent · Books the job for you",
  heromock=callmock("Quote follow-up","Day 3 · no reply yet",
     [("them","Quote sent","Deck rebuild, $6,400 · 3 days ago, no response"),
      ("ai","MDS Recover","Hi Dave, just following up on the deck quote we sent Tuesday. Happy to answer anything or lock in a start date if you are good to go?"),
      ("them","Dave","Yeah let's book it in for next week")],
     ["Cold quote revived","Job booked","Zero chasing from you"]),
  problem="<b>78%</b> of customers buy from the first business that gets back to them, yet most quotes never get a second follow up. The work you already won is quietly going cold.",
  source='<div class="src">Source: speed-to-lead research</div>',
  steps=[("01","A quote or lead goes out","A quote, an enquiry or an old customer sits in your list, waiting."),
         ("02","MDS Recover follows up","Politely, on the right cadence, by text and email, again and again until you get an answer."),
         ("03","Cold turns into booked","Quotes get accepted, dead leads come back to life, old customers rebook.")],
  feats=[("refresh","Missed lead recovery","Every enquiry that did not convert gets a smart, friendly follow up until it books or bows out."),
         ("chat","Quote follow-up","Sent a quote? It chases it for you on the perfect schedule, so good jobs do not go quiet."),
         ("users","Reactivation","Wakes up your old customer list with the right offer at the right time, turning past jobs into new ones.")],
  demoh="Won on the <em>follow up.</em>", demosub="A quote that would have gone cold, revived automatically while the owner was on a job.",
  demomock=callmock("Reactivation","Old customer · 8 months","",
     [], ),
  demorows=[("them","Past customer","(no contact in 8 months)"),
            ("ai","MDS Recover","Hi Sarah, it has been a while since we serviced your unit. Want me to book your next one in before summer hits?"),
            ("them","Sarah","Oh good reminder, yes please")],
  demooutcomes=["Old customer reactivated","Repeat job booked","No effort from you"],
  demonote="A live walk-through is one quick call away.",
  faq=[("Will it annoy my customers?","No. It uses a polite, human cadence and stops the moment someone replies or opts out. Done right, customers thank you for the reminder."),
       ("What does it follow up?","Quotes, unconverted enquiries and old customers. You choose what gets chased and how often."),
       ("Will it sound like me?","Yes. We tailor the wording to how you talk, so every message feels like it came from your business."),
       ("How long does setup take?","Most businesses are live within a few days. We map your follow-up flow, then it runs on autopilot."),
       ("Is my customer data safe?","Yes. Details are handled securely and only used to follow up and book. We never sell or share your data.")],
  leadh="Stop letting good jobs <em>go cold.</em>",
  leadsub="Tell us about your business and we will show you how much work MDS Recover can win back. No pressure.",
  msubject="MDS Recover enquiry", mbody="I want to stop losing jobs that go cold with MDS Recover.",
)

DIV["reputation"] = dict(
  name="MDS Reputation", short="Reputation", accent="#b5ff3d", argb="181,255,61", adeep="#7fbf16",
  title="MDS Reputation · More 5-star reviews, on autopilot",
  desc="MDS Reputation turns every happy job into a Google review and a referral, and catches unhappy customers before they post. Part of MDS Diversified.",
  kicker="MDS Reputation · Reviews &amp; Referrals",
  h1a="More 5-star reviews.", h1b="On autopilot.",
  lede="MDS Reputation turns every happy job into a Google review and a referral, and quietly catches unhappy customers before they post. You climb the rankings while you work.",
  micro="Asks at the perfect moment · Catches issues privately · Builds referrals",
  heromock=callmock("Review request","Job complete · 2:15 PM",
     [("them","You","Job marked complete"),
      ("ai","MDS Reputation","Hi Sarah, so glad we could help today! If you have 20 seconds, a quick Google review means the world to a local business. Here is the link."),
      ("them","Sarah","Done! Left you 5 stars")],
     ["Review asked automatically","5-star posted","You ranked higher"]),
  problem="<b>75%</b> of people read reviews before choosing a local business, and <b>93%</b> use them to judge quality. A thin or stale review profile quietly sends buyers to your competitor.",
  source='<div class="src">Source: BrightLocal Local Consumer Review Survey, 2024</div>',
  steps=[("01","You finish a job","The moment a job is done is the moment a customer is happiest."),
         ("02","We ask at the right time","MDS Reputation sends a friendly, one-tap review request while the good feeling is fresh."),
         ("03","Reviews and referrals stack","Your rating climbs, referrals flow, and you outrank the business down the road.")],
  feats=[("star","Review engine","Automatically asks every happy customer for a Google review at the perfect moment, with a one-tap link."),
         ("users","Referral system","Turns your best customers into a steady stream of word-of-mouth referrals, on autopilot."),
         ("chat","Unhappy-customer catch","Spots an unhappy customer first and routes them to you privately, before it becomes a public 1-star.")],
  demoh="Caught <em>before it posted.</em>", demosub="An unhappy customer intercepted privately, turned around, and a public bad review avoided.",
  demomock=None,
  demorows=[("them","Customer","Honestly a bit disappointed with the finish"),
            ("ai","MDS Reputation","I am really sorry to hear that. Let me get the owner to call you today and make it right, no charge."),
            ("them","Customer","That would actually be great, thank you")],
  demooutcomes=["1-star avoided","Customer recovered","Owner alerted instantly"],
  demonote="Want to see it on your own Google profile? Book a quick call.",
  faq=[("How do you get more reviews?","Timing and ease. We ask at the happiest moment and make it a one-tap link, so far more customers actually follow through."),
       ("What about bad reviews?","Unhappy customers are caught privately first and routed to you, so you can fix it before it ever goes public."),
       ("Which platforms?","Google first, since it drives the most local trust, plus Facebook and others if you want."),
       ("How long does setup take?","Most businesses are live within a few days, connected to your Google profile and how you finish a job."),
       ("Is my customer data safe?","Yes. Details are handled securely and only used to request reviews. We never sell or share your data.")],
  leadh="Outrank the business <em>down the road.</em>",
  leadsub="Tell us about your business and we will show you how fast MDS Reputation can lift your reviews. No pressure.",
  msubject="MDS Reputation enquiry", mbody="I want more 5-star reviews and referrals with MDS Reputation.",
)

DIV["growth"] = dict(
  name="MDS Growth", short="Growth", accent="#7c3dff", argb="124,61,255", adeep="#5a1fd6",
  title="MDS Growth · Keep the pipeline full",
  desc="MDS Growth keeps your marketing running, content, local presence, website and ads, all pointing at more enquiries, month after month. Part of MDS Diversified.",
  kicker="MDS Growth · Content &amp; Growth",
  h1a="Keep the pipeline full.", h1b="Without lifting a finger.",
  lede="MDS Growth keeps your marketing running, content, local presence, website and ads, all pointing at one number: more enquiries, month after month. No agency runaround, no blank-page Mondays.",
  micro="Always-on marketing · One clear number · No work from you",
  heromock=checklist("This month, handled","Auto-run",
     [("Mon","3 social posts published, on-brand"),
      ("Wed","Google Business profile refreshed"),
      ("Fri","Local ad live, targeting your area"),
      ("Result","Enquiries up vs last month")],
     ["Marketing never went quiet","Pipeline stayed full","Zero hours from you"]),
  problem="Generating leads is the <b>#1 challenge</b> for most small businesses. When the marketing goes quiet, the pipeline goes quiet 60 to 90 days later. Consistency beats intensity, every time.",
  source='<div class="src">Source: small business lead-generation surveys, 2024-26</div>',
  steps=[("01","We build your plan","A simple growth plan around your best jobs, your area and your margins."),
         ("02","It runs, consistently","Content, local presence and ads go out on schedule, every week, without you chasing it."),
         ("03","Enquiries come in","A steady, predictable flow of new work, pointed at one number you can actually track.")],
  feats=[("pen","Social content","On-brand posts published consistently, so you stay top of mind without ever touching a caption."),
         ("globe","Local growth","Google Business, local SEO and reviews working together so you show up first when locals search."),
         ("mega","Smart ads","Targeted local ads that bring in real enquiries, watched and tuned so budget is never wasted.")],
  demoh="One number. <em>Up and to the right.</em>", demosub="Marketing that does not go quiet the moment you get busy, because it runs whether you do or not.",
  demomock=None, demorows=None, demooutcomes=None,
  demonote="Want a quick growth plan for your business? Book a call.",
  faq=[("Do I have to write anything?","No. We handle the content, the posting and the ads. You approve the direction once, then it runs."),
       ("How fast will I see results?","Marketing compounds. Local presence and content build over weeks, ads can bring enquiries sooner. We track one clear number."),
       ("What exactly is included?","Social content, your Google Business and local SEO, website improvements and targeted local ads, tuned each month."),
       ("How long does setup take?","Most businesses are live within a week or two, once we have your branding and goals."),
       ("Is my data safe?","Yes. Your accounts and data are handled securely and never sold or shared.")],
  leadh="Stop marketing <em>in bursts.</em>",
  leadsub="Tell us about your business and we will map a simple plan to keep your pipeline full. No pressure.",
  msubject="MDS Growth enquiry", mbody="I want to keep my pipeline full with MDS Growth.",
)

DIV["ops"] = dict(
  name="MDS Ops", short="Ops", accent="#ffb800", argb="255,184,0", adeep="#c68e00",
  title="MDS Ops · Get your week back",
  desc="MDS Ops clears the admin that eats your day, reminders, invoices, intake, email and SOPs, so your time goes on winning and doing the work. Part of MDS Diversified.",
  kicker="MDS Ops · Admin &amp; Back Office",
  h1a="Get your week back.", h1b="We run the busywork.",
  lede="MDS Ops clears the unglamorous admin that eats your day, reminders, invoices, intake forms, email and the SOPs no one gets around to, so your time goes on winning and doing the work.",
  micro="Clears the admin · Runs in the background · Hours back every week",
  heromock=checklist("Today, handled","Back office",
     [("9:02","Sent 4 invoices, chased 2 overdue"),
      ("11:20","Processed 3 new job intake forms"),
      ("2:15","Cleared the shared inbox to zero"),
      ("4:40","Updated the job tracker for tomorrow")],
     ["A day of admin, gone","Nothing slipped","You stayed on the tools"]),
  problem="The average owner loses around <b>14 hours a week</b> to admin. That is a full working day, every week, spent on paperwork instead of winning and doing the work.",
  source='<div class="src">Source: Time Etc small business study</div>',
  steps=[("01","Map the busywork","We list the repetitive admin that eats your week, the stuff you dread."),
         ("02","MDS Ops takes it over","Invoices, reminders, intake, email and SOPs get handled in the background, reliably."),
         ("03","You get hours back","Your week opens up for the work that actually makes money.")],
  feats=[("inbox","Admin cleanup","Invoices, reminders, intake forms and data entry, handled on time, every time, without you."),
         ("chat","Email replies","Your inbox kept moving with fast, on-brand replies, so nothing important sits unread."),
         ("book","Training &amp; SOPs","The SOPs no one gets around to, written and kept current, so your business runs without you in it.")],
  demoh="A day of admin, <em>before lunch.</em>", demosub="The repetitive back-office work that quietly eats your week, cleared in the background.",
  demomock=None, demorows=None, demooutcomes=None,
  demonote="Want to see what we could take off your plate? Book a call.",
  faq=[("What can it actually do?","Invoicing and reminders, job intake, inbox management, data entry, scheduling and writing your SOPs. If it is repetitive admin, it is in scope."),
       ("Will it access my systems securely?","Yes. We connect with secure, permissioned access and only touch what you approve."),
       ("Do I lose control?","No. You set the rules and approvals. MDS Ops does the work, you stay in charge."),
       ("How long does setup take?","Most businesses see admin lifting within a week, starting with your biggest time-drains first."),
       ("Is my data safe?","Yes. Everything is handled securely and never sold or shared.")],
  leadh="Stop losing a day a week <em>to admin.</em>",
  leadsub="Tell us about your business and we will show you exactly what MDS Ops can take off your plate. No pressure.",
  msubject="MDS Ops enquiry", mbody="I want my week back with MDS Ops.",
)

DIV["research"] = dict(
  name="MDS Research", short="Research", accent="#2dd4bf", argb="45,212,191", adeep="#1a9e8e",
  title="MDS Research · Decisions backed by data",
  desc="MDS Research gives you on-demand market research and clear, actionable briefs, so you price, pitch and plan with real data instead of gut feel. Part of MDS Diversified.",
  kicker="MDS Research · Research &amp; SME",
  h1a="Decisions backed by data.", h1b="Not guesswork.",
  lede="MDS Research gives you on-demand market research and clear, actionable briefs, so you price, pitch and plan with real data instead of gut feel. Ask a question, get an answer you can act on.",
  micro="On-demand research · Clear briefs · Act with confidence",
  heromock=checklist("Brief: pricing in your market","Ready in hours",
     [("Finding","Your quotes sit 12% below the local average"),
      ("Finding","Two competitors raised prices last quarter"),
      ("Finding","Customers rank speed over price in your area"),
      ("Action","Lift prices on call-outs, lead with same-day")],
     ["Real market data","Clear next step","Decision made in a day"]),
  problem="Most operators set prices, pitches and plans on gut feel, not current market data. That quietly costs margin and momentum, every single month.",
  source="",
  steps=[("01","Ask a question","Pricing, a competitor, a new service, a market you are eyeing. Whatever you need to know."),
         ("02","MDS Research digs in","We gather the real data and sources, then cut through the noise."),
         ("03","You get a clear brief","A short, plain-English brief with the findings and a recommended next step.")],
  feats=[("search","Research assistant","On-demand answers to the business questions slowing your decisions, gathered and summarised fast."),
         ("bulb","Subject-matter expert","Expertise on tap for pricing, markets, competitors and new services, without hiring a consultant."),
         ("doc","Report builder","Clear, actionable briefs and reports you can actually use, not 40 pages of fluff.")],
  demoh="A decision, <em>made in a day.</em>", demosub="A pricing question that used to be a guess, answered with real market data and a clear next step.",
  demomock=None, demorows=None, demooutcomes=None,
  demonote="Have a question keeping you up at night? Book a call.",
  faq=[("What can I ask?","Anything that helps you decide: pricing, competitors, demand, a new service or market, or a quick fact-check before a big move."),
       ("How fast do I get answers?","Most briefs land within hours to a day, depending on depth. Quick questions are quick."),
       ("Where does the data come from?","Credible, current sources, gathered and sense-checked, with the key points summarised so you do not have to dig."),
       ("How long does setup take?","There is barely any. Send your first question and you get a brief back."),
       ("Is my information safe?","Yes. Your questions and data are handled securely and never sold or shared.")],
  leadh="Stop deciding <em>on gut feel.</em>",
  leadsub="Tell us about your business and the questions slowing you down. We will show you how MDS Research helps. No pressure.",
  msubject="MDS Research enquiry", mbody="I want clearer decisions with MDS Research.",
)

# read the Reception page as the base template
with open(os.path.join(ROOT, "mds-reception.html"), encoding="utf-8") as f:
    base = f.read()

# Build each page by string-replacing the Reception-specific blocks.
# We reconstruct cleanly from data instead of regex on the base, to stay robust:
# extract the shared CSS by swapping only color tokens, then rebuild body.

def build(d):
    # demo mock: build from demorows if provided, else use checklist already in d['demomock'] style
    if d.get("demorows"):
        demomock = callmock("Example", "Real flow", d["demorows"], d["demooutcomes"])
    else:
        demomock = ""  # non-conversational divisions: no duplicate card in the demo section

    steps_html = "".join(step(*s) for s in d["steps"])
    feats_html = "".join(feat(*fz) for fz in d["feats"])
    faq_html = "".join(faq(q,a) for q,a in d["faq"])

    page = base
    # ---- color swaps (Reception cyan -> division accent) ----
    page = page.replace("#00d4ff", d["accent"])
    page = page.replace("0,212,255", d["argb"])
    page = page.replace("#0094c6", d["adeep"])
    # ---- head ----
    page = page.replace("<title>MDS Reception · Never miss a call, never miss a job</title>",
                        f'<title>{d["title"]}</title>')
    page = page.replace('content="MDS Reception is the always on AI receptionist that answers every call, chat and message, qualifies the lead and books the job, day or night. Part of MDS Diversified." />',
                        f'content="{d["desc"]}" />')
    # ---- hero ----
    page = page.replace('<span class="kicker">MDS Reception &middot; Capture &amp; Answer</span>'.replace("&middot;","·"),
                        f'<span class="kicker">{d["kicker"]}</span>')
    page = page.replace('<span class="kicker">MDS Reception · Capture &amp; Answer</span>',
                        f'<span class="kicker">{d["kicker"]}</span>')
    page = page.replace("<h1>Never miss a call.<br><em>Never miss a job.</em></h1>",
                        f'<h1>{d["h1a"]}<br><em>{d["h1b"]}</em></h1>')
    page = page.replace("Your always on AI receptionist answers every call, chat and message, day or night. It qualifies the lead, books the job, and texts you the details, while you are on the tools.",
                        d["lede"])
    page = page.replace("Answers 24/7 · Books straight into your calendar · No missed jobs", d["micro"])
    return page, demomock, steps_html, feats_html, faq_html

# Because the call-mock / steps / feats / faq blocks in Reception are large and unique,
# we replace them by locating their wrapper markers.
import re

def replace_between(text, start_marker, end_marker, new_inner, keep_markers=True):
    i = text.index(start_marker)
    j = text.index(end_marker, i) + len(end_marker)
    if keep_markers:
        return text[:i] + start_marker + new_inner + end_marker + text[j:]
    return text[:i] + new_inner + text[j:]

for slug, d in DIV.items():
    page, demomock, steps_html, feats_html, faq_html = build(d)

    # hero call mock: between <div class="callcard" aria-label="Sample call"> ... </div>\n        </div>
    page = re.sub(r'<div class="callcard" aria-label="Sample call">.*?</div>\s*</div>\s*</div>\s*</div>\s*</div>',
                  d["heromock"] + '</div></div></div></div>', page, count=1, flags=re.S)

    # problem stat band
    page = re.sub(r'<p class="big">.*?</p>\s*<div class="src">Source: 411 Locals study, 2024</div>',
                  f'<p class="big">{d["problem"]}</p>\n    {d["source"]}', page, count=1, flags=re.S)

    # steps
    page = re.sub(r'<div class="steps" style="text-align:left">.*?</div>\s*</div>\s*</section>',
                  f'<div class="steps" style="text-align:left">{steps_html}</div>\n  </div>\n</section>',
                  page, count=1, flags=re.S)
    # how-it-works heading
    page = page.replace("<h2>Set up once. <em>Never miss again.</em></h2>",
                        f'<h2>{d["stepsh"]}</h2>' if d.get("stepsh") else "<h2>How it works.</h2>")
    page = page.replace("No new apps to learn. It plugs into the phone, website and socials you already use.",
                        d.get("stepssub","No new apps to learn. It plugs into what you already use."))

    # features section
    page = re.sub(r'<div class="feats" style="text-align:left">.*?</div>\s*</div>\s*</section>',
                  f'<div class="feats" style="text-align:left">{feats_html}</div>\n  </div>\n</section>',
                  page, count=1, flags=re.S)
    page = page.replace("<h2>One receptionist. <em>Every channel.</em></h2>",
                        f'<h2>{d.get("featsh","What you get.")}</h2>')

    # demo section heading + sub + mock + note
    page = page.replace("<h2>This happened <em>after hours.</em></h2>", f'<h2>{d["demoh"]}</h2>')
    page = page.replace("A real example of the flow. The caller got an instant answer and a booking. The owner was asleep.", d["demosub"])
    demo_repl = f'<div style="max-width:520px;margin:36px auto 0">{demomock}</div>' if demomock else ''
    page = re.sub(r'<div style="max-width:520px;margin:36px auto 0">\s*<div class="callcard">.*?</div>\s*</div>\s*</div>',
                  demo_repl, page, count=1, flags=re.S)
    # genericize the "who it's for" copy (was Reception-specific)
    page = page.replace("<h2>Built for businesses <em>that live on the phone.</em></h2>",
                        "<h2>Built for businesses <em>that want to grow.</em></h2>")
    page = page.replace("If a missed call is a missed job, MDS Reception pays for itself fast.",
                        f'If you run a busy local business, {d["name"]} pays for itself fast.')
    page = page.replace("A live voice demo is coming soon. Want to hear it now? <a href=\"#start\" style=\"color:" + d["accent"] + "\">Book a quick call.</a>",
                        d["demonote"] + ' <a href="#start" style="color:'+d["accent"]+'">Book a call.</a>')
    page = page.replace("A live voice demo is coming soon. Want to hear it now? <a href=\"#start\" style=\"color:#00d4ff\">Book a quick call.</a>",
                        d["demonote"] + ' <a href="#start" style="color:'+d["accent"]+'">Book a call.</a>')

    # FAQ
    page = re.sub(r'<div class="faq">.*?</div>\s*</div>\s*</section>',
                  f'<div class="faq">{faq_html}</div>\n  </div>\n</section>', page, count=1, flags=re.S)

    # lead section
    page = page.replace("<h2>Stop losing jobs <em>to a missed call.</em></h2>", f'<h2>{d["leadh"]}</h2>')
    page = page.replace("Tell us a little about your business and we will show you exactly how MDS Reception works for you. No pressure.", d["leadsub"])
    page = page.replace("Send to MDS Reception &rarr;", f'Send to {d["name"]} &rarr;')

    # footer slug
    page = page.replace("© 2026 · MDS Reception · AU · UAE · USA",
                        f'© 2026 · {d["name"]} · AU · UAE · USA')

    # mailto
    page = page.replace("var subject='MDS Reception enquiry';",
                        f"var subject='{d['msubject']}';")
    page = page.replace("var body='Hi James,\\n\\nI want to never miss a call again with MDS Reception.\\n\\nName: '+name+'\\nBusiness: '+biz+'\\nContact: '+contact+'\\n\\nPlease show me how it works.';",
                        f"var body='Hi James,\\n\\n{d['mbody']}\\n\\nName: '+name+'\\nBusiness: '+biz+'\\nContact: '+contact+'\\n\\nPlease show me how it works.';")

    out = os.path.join(ROOT, f"mds-{slug}.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    print("wrote", out, len(page), "bytes")
