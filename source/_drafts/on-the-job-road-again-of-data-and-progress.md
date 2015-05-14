title: 'On the (job) road again: Of data and progress'
tags:
---

Explanation of status flow

Data (to collect):
1. How often did I make it to what stage of the interview?
  - What percent of companies did I make it to the offer stage?
2. How long did it take to go from one stage to the next?
  - How long did it take to go from talking to a company to the final stage (offer or no opportunity)
  - Similarly, with number of calls
3. On average, how long did it take to go from me contacting a company to hearing back from them (initial contact v. later)
  - What was the overall average response time for first contact?
  - What was the average response time overall per company?
4. What companies were the most disappointing:
  - Took the longest before rejecting me as a candidate
  - Took the most points of contact before rejecting me as a candidate
5. Most common reasons for rejection
6. Most common means of initial contact (email vs. SO. vs LinkedIn vs call)... vs offers? Furthest stage?
7. Recruiter lead vs self-directed (vs offers, furthest stage)

Using textql (Paul!)
```
textql -source job_search_2015.csv -header -console
```


// Company count = SELECT COUNT(*) FROM (SELECT DISTINCT Company FROM tbl);
// SELECT Count(*) FROM (SELECT Company, Status FROM tbl WHERE Status = "STATUS" GROUP BY Company, Status ORDER BY Company, Date DESC);


```
# Scratch
# SELECT Status, Company FROM tbl GROUP BY Status;  # Will give us the total, but will count duplicate rows. Want only one per company
# SELECT Company, Status FROM tbl WHERE GROUP BY Company, Status ORDER BY Company, Date DESC  # All companies with all statuses from most recent to least recent
```

1. How often did I make it to what stage of the interview?

```
SELECT
	companies.Status, printf("%d / %d (%.2f%%)", Count(companies.Status), meta.companies, Count(companies.Status)*100.0 / meta.companies)
FROM (
	SELECT Company, Status FROM tbl GROUP BY Company, Status ORDER BY Company, Date DESC
) AS companies
JOIN (
	SELECT COUNT(*) AS companies FROM (SELECT DISTINCT Company FROM tbl)
) AS meta
GROUP BY Status;
```
| Stage          | Percentage       |
|----------------|------------------|
| No Opportunity | 22 / 31 (70.97%) |  // can happen at any point after 'Contacted'
| Contacted      | 26 / 31 (83.87%) |  // 5 companies reached out to me
| In Progress    | 19 / 31 (61.29%) |
| Scheduled      | 15 / 31 (48.39%) |
| Interview      | 12 / 31 (38.71%) |
| Rejected       | 5 / 31 (16.13%)  |  // Rejection can only happen after an interview
| Offer          | 5 / 31 (16.13%)  |
| Declined       | 4 / 31 (12.90%)  |


2. How long to get to each stage?
```
```

3. How long until first response?
( TODO: Get average response times )

```
SELECT
	Company, printf("%.2f", julianday(MAX(pairs.Date)) - julianday(MIN(pairs.Date))) AS duration
FROM (
	SELECT Date, Company, Type, Status FROM tbl GROUP BY Company, Type ORDER BY Company, Date, Type ASC
) as pairs
GROUP BY pairs.Company
HAVING Count(pairs.Date) >= 2
ORDER BY duration DESC, pairs.Company;
```
| Company            | First Response Time (days) |
|--------------------|----------------------------|
| Etsy               | 8.78                       |
| npm                | 6.65
| Codefights         | 5.77
| Streak             | 3.38
| Shopify            | 3.00
| Sandvine           | 2.54
| Demeure            | 1.00
| TribeHR / Netsuite | 1.00
| Customer.io        | 0.85
| StackExchange      | 0.43
| Flexport           | 0.13
| Wattpad            | 0.10
| Vehikl             | 0.04
| Mozilla            | 0.03
| Cafe               | 0.02
| Axonify            | 0.01
| Blitzen            | 0.01
| Gravity4           | 0.01
| Github             | 0.00
| Google Ventures    | 0.00
| JuiceMobile        | 0.00
| Plasticity Labs    | 0.00
| Primal             | 0.00
| Vidyard            | 0.00
| WeMesh             | 0.00
| Webflow            | 0.00

4. What companies took the longest (time) to reject, and the most points of contact to reject? (Most disappointing)
```
SELECT
	julianday(MAX(Date)) - julianday(MIN(Date)) AS duration, Company
FROM tbl WHERE Notes != "Accepted Shopify Offer"
GROUP BY Company ORDER BY Duration DESC;
```


SELECT julianday(MAX(Date)) - julianday(MIN(Date)) AS Duration, Company FROM tbl WHERE Notes != "Accepted Shopify Offer" GROUP BY Company ORDER BY Duration DESC;
This will give us the duration between first contact, and last contact. Unfortunately, this is distorted by entries I created to clear spreadsheet... This can be fixed by creating a flag column

4.1. Shouldn't this just be the above with a 'HAVING' query?
4.2. SELECT Count(*), Company FROM tbl GROUP BY Company;
This is equiavelent to how many points of contact per company

```
SELECT
	Company, julianday(MAX(Date)) - julianday(MIN(Date)) AS Duration, Count(*)
FROM tbl
WHERE Notes != "No response"
GROUP BY Company
HAVING SUM(case when Status = "No Opportunity" then 1 when Status = "Rejected" then 1 else 0 end) > 0
ORDER BY Duration DESC;
```
| Company            | Start to finish (days) | Points of Contact |
|--------------------|------------------------|-------------------|
| Etsy|43.5555555555038
Github|29.6645833333023
Cafe|22.0798611110076
Mozilla|20.7395833334886
Sandvine|18.7881944444962
npm|15.1875
StackExchange|13.5069444444962
Blitzen|13.2847222224809
Flexport|9.79513888899237
Wattpad|9.02083333348855
JuiceMobile|8.625
Google Ventures|6.75
Vidyard|4.58333333348855
Streak|3.37569444440305
Webflow|0.00069444440305233

http://stackoverflow.com/questions/25121916/selecting-rows-in-sql-only-where-all-values-do-not-meet-a-certain-criteria





I did my best to collect as much data as possible, but early efforts were spotty (omited time information)
A few of the companies I had to re-interview for... some I kept previous offer
If doing again, should build tools to track this, keep data without having to compile stats manually

Programmign relational algebra is hard... don't do it. Use a databas
