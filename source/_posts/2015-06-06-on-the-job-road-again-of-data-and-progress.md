title: 'On the (job) road again: Of data and progress'
tags:
  - job search
  - career
date: 2015-06-06 17:31:12
---


I talk a lot about jobs and careers and such. For the past few weeks, I've talked about [how I ended up moving on from a great opportunity](/2015/05/14/on-the-job-road-again-of-acquisitions-and-departures/), and [how I got to my next one](/2015/05/31/on-the-job-road-again-of-the-long-job-road/), and in the past I've mentioned [gathering data](/2014/06/23/times-are-a-changin/) on the job search.

Well, this time, I actually have a decent data set to analyze. I'm going to show you how I collected and analyzed the data. If you're like me, you can even use this on your next job search to see how things are going. Or not!

## Data Background

Each entry in my spreadsheet contained a row describing a 'point of contact' as follows:
- Date and time
- Company name
- Channel (e.g. Email, LinkedIn, StackOverflow Careers)
- Type (e.g. Incoming vs Outgoing)
- Status (e.g. Contacted, Interview, Scheduled, Offer)
- Contact
- Notes

I definitely made some mistakes in collecting the data though. For starters, I didn't record the *time* of the point of contact for the first week or so, leaving me with only *day* granularity.

Also, the *flow* through the stages is a little unclear. This is what it generally looks like (with all the various states):
| State          | Next States                                              |
|----------------|----------------------------------------------------------|
| No Opportunity |                                                          |
| Contacted      | In Progress, Scheduled, Interview, Offer, No Opportunity |
| In Progress    | Scheduled, Interview, Offer, No Opportunity              |
| Scheduled      | Interview, Offer, No Opportunity                         |
| Interview      | Offer, Rejected, No Opportunity                          |
| Rejected       |                                                          |
| Offer          | Declined                                                 |
| Declined       |                                                          |

Yes, it probably would be best to show this as some sort of [finite state machine](http://en.wikipedia.org/wiki/Finite-state_machine) diagram, but its not a complicated process. Actually, as I write this, it is a complicated process, and writing out a finite state machine might have actually made things clearer. The process also isn't great because the *interview* state covers multiple interviews.

Sometimes, I miscategorized things, expecially when a process dropped off. It would have been good to have a state that indicates they stopped getting back to me (as *"No Opportunity"* reflects a lack of my interest, and *"Rejected"* is unclear).

As a convention, whenever I have an interview, or a call, I count that as *incoming* (even though it is *incoming* and *outgoing*).

Not much else that I can think of regarding describing the data. I kept everything in a google spreadsheet, exported as CSV, then used a [friend's](http://pauldbergeron.com/) tool, [textql](https://github.com/dinedal/textql), to put the data in a sqlite database. Getting the database setup is as easy as this:

```
textql -source job_search_2015.csv -header -console
```

## Questions

Given the data I had, I wanted to answer a few questions about my job search:
- How often did I make it to each 'stage' of an offer process?
- How long did it take to progress between 'stages' of the offer process?
  - In particular, how long (duration, or points of contact) did it take to go from initial contact to the end of the process?
- On average, how long did it take to go from first contact to first response?
  - What was the overall average 'first response' rate?
  - What was the average response time for each company?
- What companies were 'most disappointing' (i.e. took the longest time before rejecting)?
  - Either in terms of duration, or points of contact
- What were the most common reasons for rejection (i.e. what are my areas of weakness)?
- What was the most successful means of reaching out, and how did those methods perform?
- How did recruiters fare?

With that being said, lets dive into the questions!

### How do I do?

| Stage          | Percentage       |
|----------------|------------------|
| No Opportunity | 22 / 31 (70.97%) |
| Contacted      | 26 / 31 (83.87%) |
| In Progress    | 19 / 31 (61.29%) |
| Scheduled      | 15 / 31 (48.39%) |
| Interview      | 12 / 31 (38.71%) |
| Rejected       | 5 / 31  (16.13%) |
| Offer          | 5 / 31  (16.13%) |
| Declined       | 4 / 31  (12.90%) |

`sqlite` query:

```
SELECT   companies.status,
         Printf("%d / %d (%.2f%%)", Count(companies.status), meta.companies, Count(companies.status)*100.0 / meta.companies)
FROM     (
                  SELECT   company,
                           status
                  FROM     tbl
                  GROUP BY company,
                           status
                  ORDER BY company,
                           date DESC ) AS companies
JOIN
         (
                SELECT Count(*) AS companies
                FROM   (
                                       SELECT DISTINCT company
                                       FROM            tbl) ) AS meta
group BY status;
```

One thing that sticks out is that *Contacted* is less than the total number of companies. This is because there were five companies that reached out to me instead of the other way around.

Otherwise, I think the key takeaways here are:
- I get to an inteview about 38% of the time
- Of times that I interview, I get an offer about 41% (5 / 12) of the time
- Data quality is a bit of an issue (since *Scheduled* should always lead to *Interview*, and not all *Offers* came from *Interviews* necessarily)

Overall, that seems pretty successful!

### How long to progress?

| Stage          | Average Duration | Max Duration     |
|----------------|------------------|------------------|
| No Opportunity | 1.34823232324032 | 29.661111111287  |
| Contacted      | 2.07972756413241 | 13.7256944444962 |
| In Progress    | 3.65442251460627 | 20.1909722220153 |
| Scheduled      | 2.20000000003104 | 19.2048611114733 |
| Interview      | 9.76961805562799 | 27.78125         |
| Rejected       | 0.0              | 0.0              |
| Offer          | 2.60416666669771 | 13.0208333334886 |
| Declined       | 0.0              | 0.0              |

`sqlite` query:
```
SELECT companies.status,
       Avg(duration),
       Max(duration)
FROM   (SELECT Julianday(Max(date)) - Julianday(Min(date)) AS duration,
               company,
               status
        FROM   tbl
        GROUP  BY company,
                  status
        ORDER  BY company,
                  date DESC) AS companies
GROUP  BY status; 
```

As it turns out, due to the non-linear nature of the interview process, it's not as straightforward to calculate the time to reach each stage. I also thought it would make sense to calculate how much time was spent in each stage, but apparently that gives a weird, skewed number (since you are summing over all companies, and you are pursuing multiple companies at the same time).

However we can calculate the maximum and averages. This yields some neat results (from the table above):
- An offer, from start to finish, takes about 17 days
- First contact to interview takes a calendar week
- It takes between a week and two weeks to hear back about an interview
- People are pretty good about responding within a few days (based on *scheduled*, *in progress*, and *contacted* data)
- Generally, I don't take a long time to decide on an offer

### How do they respond?
| Company            | First Response Time (days) |
|--------------------|----------------------------|
| Etsy               | 8.78                       |
| npm                | 6.65                       |
| Codefights         | 5.77                       |
| Streak             | 3.38                       |
| Shopify            | 3.00                       |
| Sandvine           | 2.54                       |
| Demeure            | 1.00                       |
| TribeHR / Netsuite | 1.00                       |
| Customer.io        | 0.85                       |
| StackExchange      | 0.43                       |
| Flexport           | 0.13                       |
| Wattpad            | 0.10                       |
| Vehikl             | 0.04                       |
| Mozilla            | 0.03                       |
| Cafe               | 0.02                       |
| Axonify            | 0.01                       |
| Blitzen            | 0.01                       |
| Gravity4           | 0.01                       |
| Github             | 0.00                       |
| Google Ventures    | 0.00                       |
| JuiceMobile        | 0.00                       |
| Plasticity Labs    | 0.00                       |
| Primal             | 0.00                       |
| Vidyard            | 0.00                       |
| WeMesh             | 0.00                       |
| Webflow            | 0.00                       |

`sqlite` query:

```
SELECT company,
       Printf("%.2f", Julianday(Max(pairs.date)) - Julianday(Min(pairs.date)))
       AS
       duration
FROM   (SELECT date,
               company,
               type,
               status
        FROM   tbl
        GROUP  BY company,
                  type
        ORDER  BY company,
                  date,
                  type ASC) AS pairs
GROUP  BY pairs.company
HAVING Count(pairs.date) >= 2
ORDER  BY duration DESC,
          pairs.company; 
```

Again, lending to data quality issues, it looks like some of these companies got back to me *really* quickly (under a day) but it is most likely because either they reached out to me, or because something else happened, such as I decided to reject the opportunity.

Unfortunately, that doesn't tell me a lot about how long it typically takes to get in touch. I had to do a separate query to figure that out:
| Company            | Average response time (days) |
|--------------------|------------------------------|
| Demeure            | 6.41815476192694             |
| npm                | 5.0625                       |
| Gravity4           | 4.80555555550382             |
| Codefights         | 4.42083333330229             |
| Github             | 4.23779761904318             |
| Hireology          | 3.9143518518346              |
| RecruitLoop        | 3.9143518518346              |
| Plasticity Labs    | 3.5                          |
| WeMesh             | 3.38060897434703             |
| Primal             | 3.33333333333333             |
| Axonify            | 3.31770833337214             |
| Customer.io        | 3.08506944449618             |
| Wattpad            | 3.00694444449618             |
| TribeHR / Netsuite | 2.64460784314639             |
| Cafe               | 2.45331790122307             |
| Shopify            | 2.35611979165697             |
| Blitzen            | 2.21412037041349             |
| Mozzaz             | 2.19097222217048             |
| StackExchange      | 1.92956349207088             |
| Streak             | 1.68784722220153             |
| Google Ventures    | 1.6875                       |
| Mozilla            | 1.5953525641145              |
| Sandvine           | 1.56568287037468             |
| Etsy               | 1.55555555555371             |
| Flexport           | 1.22439236112405             |
| Vehikl             | 1.17414529915326             |
| JuiceMobile        | 0.958333333333333            |
| Vidyard            | 0.763888888914759            |
| Webflow            | 0.000347222201526165         |

`sqlite` query:
```
SELECT companies.company,
       duration / ( _count + 1 ) AS average
FROM   (SELECT Julianday(Max(date)) - Julianday(Min(date)) AS duration,
               company
        FROM   tbl
        GROUP  BY company
        ORDER  BY company,
                  date DESC) AS companies
       INNER JOIN (SELECT company,
                          Count(*) AS _count
                   FROM   tbl
                   WHERE  type = "incoming"
                   GROUP  BY company,
                             type) AS contacts
               ON contacts.company = companies.company
GROUP  BY companies.company
ORDER  BY average DESC; 
```

When we look at this data, the picture is a bit clearer, namely, that most companies get back to you within a few days. Demeure is a bit skewed on this list because I received an offer early, but didn't act on it till much later in the month.

### Most disappointing companies
| Company            | Start to finish (days) | Points of Contact |
|--------------------|------------------------|-------------------|
| Etsy               | 43.5555555555038       | 42                |
| Github             | 29.6645833333023       | 13                |
| Cafe               | 22.0798611110076       | 15                |
| Mozilla            | 20.7395833334886       | 23                |
| Sandvine           | 18.7881944444962       | 17                |
| npm                | 15.1875                | 5                 |
| StackExchange      | 13.5069444444962       | 12                |
| Blitzen            | 13.2847222224809       | 10                |
| Flexport           | 9.79513888899237       | 13                |
| Wattpad            | 9.02083333348855       | 5                 |
| JuiceMobile        | 8.625                  | 12                |
| Google Ventures    | 6.75                   | 5                 |
| Vidyard            | 4.58333333348855       | 9                 |
| Streak             | 3.37569444440305       | 3                 |
| Webflow            | 0.00069444440305233    | 2                 |

`sqlite` query:
```
SELECT company,
       Julianday(Max(date)) - Julianday(Min(date)) AS Duration,
       Count(*)
FROM   tbl
WHERE  notes != "no response"
GROUP  BY company
HAVING Sum(CASE
             WHEN status = "no opportunity" THEN 1
             WHEN status = "rejected" THEN 1
             ELSE 0
           END) > 0
ORDER  BY duration DESC; 
```

I don't like to pick on companies, and I'd like to think that I'm not picking on these companies, but I was curious which companies took the most effort to yield the least. Unfortunately, that will highlight companies where there was a long process.

Etsy is a bit of an outlier on this list as I started interviewing for one position, then pivoted about halfway through. Even if you cut the time in half, it still puts it in the top three.

What can we take away from this? Well, some companies have a longer process to hire. Unsurprisingly, larger companies take a longer time to decide on candidates.

### Why did things not work out?

I won't post the raw data here, because my notes are personal, nor will I post the companies. These are some approximations of my notes from companies that either *rejected* me, there was *no opportunity*, or I *declined*:

- "I did not hear back from the company, so I am marking this as a dead lead"
- "I accepted an offer with another company"
- "I thought that the interview went well. I had to be prompted in a few areas, but generally things were positive."
- "Company is holding off on hiring for now"
- "They were hiring remote, but the position was filled"
- "They will only be proceeding with local candidates"
- "They are not interested in continuing; no details were given"
- "They are not interested in having remote developers"
- "They say that I am too junior, couldn't provide examples of my work, and asked for too much compensation"
- "I talked too much in the context of myself as opposed to talking about how I worked as part of a team"

What can I take away from this? Not a lot, actually. The majority of the notes I have indicate that things were out of my control, or I wasn't given any feedback that I can act on. The few that did, the latter points, contradict the feedback I have been given by past managers and teammates.

Oh well.

`sqlite` query:

```
SELECT status,
       notes,
       Count(notes)
FROM   tbl
WHERE  status = "rejected"
        OR status = "no opportunity"
        OR status = "declined"
GROUP  BY notes,
          status
ORDER  BY Count(notes) DESC; 
```

### Competition: Channel versus channel

| Channel               | Stage          | Percentage       |
|-----------------------|----------------|------------------|
| Application           | No Opportunity | 1 / 1 (100%)     |
| Application           | Contacted      | 1 / 1 (100%)     |
| Application           | Interview      | 1 / 1 (100%)     |
| Application           | Scheduled      | 1 / 1 (100%)     |
| Stackoverflow Careers | No Opportunity | 2 / 2 (50%)      |
| Stackoverflow Careers | Contacted      | 1 / 2 (50%)      |
| Stackoverflow Careers | In Progress    | 1 / 2 (50%)      |
| Stackoverflow Careers | Scheduled      | 1 / 2 (50%)      |
| Stackoverflow Careers | Interview      | 1 / 2 (50%)      |
| LinkedIn              | No Opportunity | 1 / 1 (100%)     |
| LinkedIn              | Contacted      | 1 / 1 (100%)     |
| LinkedIn              | In Progress    | 1 / 1 (100%)     |
| LinkedIn              | Scheduled      | 1 / 1 (100%)     |
| Email                 | No Opportunity | 18 / 27 (66.6%)  |
| Email                 | Contacted      | 23 / 27 (85.2%)  |
| Email                 | In Progress    | 17 / 27 (63.0%)  |
| Email                 | Scheduled      | 12 / 27 (44.4%)  |
| Email                 | Interview      | 10 / 27 (37.0%)  |
| Email                 | Rejected       | 5 / 27  (18.5%)  |
| Email                 | Offer          | 5 / 27  (18.5%)  |
| Email                 | Declined       | 4 / 27  (14.8%)  |

`sqlite` query:
```
SELECT channel.channel,
       companies.status,
       Count(companies.status)
FROM   (SELECT company,
               status
        FROM   tbl
        GROUP  BY company,
                  status
        ORDER  BY company,
                  date DESC) AS companies
       INNER JOIN (SELECT Min(CASE
                                WHEN channel = "application" THEN 0.1
                                WHEN channel = "stackoverflow careers" THEN 0.2
                                WHEN channel = "linkedin" THEN 0.3
                                WHEN channel = "email" THEN 1
                                WHEN channel = "interview" THEN 2
                                WHEN channel = "call" THEN 3
                                WHEN channel = "in-person" THEN 4
                                ELSE 100
                              END) AS Channel,
                          company
                   FROM   tbl
                   GROUP  BY company) AS channel
               ON channel.company = companies.company
GROUP  BY channel,
          status; 
```

I fudged the above a bit from the SQL query (because I am not an SQL wizard) to get the relative totals. Unfortunately, there is not a lot of data to work with, so its hard to draw meaningful conclusions.

### Me versus recruiters

| Source    | Stage          | Percentage       |
|-----------|----------------|------------------|
| Recruiter | No Opportunity | 9 / 15  (60%)    |
| Me        | No Opportunity | 13 / 16 (81.3%)  |
| Recruiter | Contacted      | 12 / 15 (80%)    |
| Me        | Contacted      | 14 / 16 (87.5%)  |
| Recruiter | In Progress    | 9 / 15  (60%)    |
| Me        | In Progress    | 10 / 16 (62.5%)  |
| Recruiter | Scheduled      | 5 / 15  (33.3%)  |
| Me        | Scheduled      | 10 / 16 (62.5%)  |
| Recruiter | Interview      | 4 / 15  (26.7%)  |
| Me        | Interview      | 8 / 16  (50%)    |
| Recruiter | Rejected       | 3 / 15  (20%)    |
| Me        | Rejected       | 2 / 16  (12.5%)  |
| Recruiter | Offer          | 2 / 15  (13.3%)  |
| Me        | Offer          | 3 / 16  (18.8%)  |
| Recruiter | Declined       | 2 / 15  (13.3%)  |
| Me        | Declined       | 2 / 16  (12.5%)  |

Since I didn't declare a "source" for a job, this is a bit trickier. I didn't have a lot of recruiter assistance, so to answer this question I just separated the recruiter responses from the first question. There were about six "recruiters".

I didn't expect the results to turn out like this. Based on this data:
- Recruiters had a better chance of finding good opportunities (comparing *No Opportunity* entries). My guess is that I take a bit more of a shotgun approach, or recruiters don't bother with opportunities that don't meet my criteria.
- I was more likely to reach an interview on my own than with a recruiter (comparing *Interview* or *Scheduled* entries)
- Odds of being offered were pretty similar between the two. This makes sense, as that is more about my own performance than anything else.

## Wrapping it up

I learned a lot from this experience. When I started doing the data analysis initially, I was a bit stumped and thought that programming would be easier... it is not. This is exactly what databases are designed for: [relational algebra](http://en.wikipedia.org/wiki/Relational_algebra).

Next time I do this, and I don't plan on doing it for a long time, I will probably want to make the flow between states clearer, record all the date information initially, and probably include some additional states to make transitions clearer. I feel like this whole process of collecting data, and the tracking and analysis of it, could be used in some sort of lead management system, but I'm not interested in exploring that at the moment.
