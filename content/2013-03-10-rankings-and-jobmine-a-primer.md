layout: post
title: Rankings and Jobmine: A primer
slug: rankings-and-jobmine-a-primer
date: 2013-03-10 13:55
comments: true
categories: 

I find the problem of hiring good candidates for a company fascinating. I'll just get that out in the open. As much as I am a software developer, finding talented people and evaluating them just seems like an exciting exercise. Maybe it's the power that I wield (unlikely), but I think it's the combination of the challenge with the opportunity to make a positive change in another person's life (I hope). It comes as no surprise then that I enjoy hiring co-operative education students at Willet (hereafter simply referred to as *co-ops*).

Hiring is no small feat, but hiring co-ops is made slightly easier by a few things. One of which is the fact that co-ops typically have a four-month contract; it gives them a chance to get a taste of what it's like to be at a startup as a developer, and us a chance to evaluate potentially long-term candidates, broaden our talent network, and mentor people (well, and learn a lot from them as well). However, the thing that makes co-op hiring significantly easier for us is [the University of Waterloo](http://uwaterloo.ca), specifically, [Jobmine](https://uwaterloo.ca/jobmine/).

I'm not going to brag about Jobmine, because, as is well established, [it isn't very good as a piece of software](https://www.google.ca/search?q=jobmine+sucks). What it does provide is a nice framework for students to find jobs, for employers to find students and schedule interviews, and for both parties to come to a job offer in a *mostly* fair way.

*I'm not here to debate the benefits and drawbacks of jobmine, at least, not today. Just providing some background on the matter.*

One element that is unique to jobmine is the job matching process. After students have been screened and interviewed, a process of *ranking* occurs. This is an interesting contrast to how events play out outside of jobmine: typically, a job offer is made to a candidate, and that's it. Instead, in rankings, an employer can make an offer to a student by ranking them as number one, and students can rank the positions they interviewed for from one to ten. Students don't know what their rank is unless it's an offer, and employers don't know what the students ranked the position as either.

After rankings are complete from both sides, the system 'magically' begins matching students. Offers are matched first, then other rankings are matched. How do the matches actually take place? The system uses the sum of the preferences, and picks the lowest value to match. For example, lets suppose we have the following example:

 Employer (E) | Student (S) | E Ranking / S Ranking 
 Goggle       | Steve Brine | 1 / 1                 
 Goggle       | Will Yates  | 2 / 3                 
 Goggle       | Mike Drucker| 3 / 2                 
 VisageTome   | Steve Brine | 2 / 9                 
 VisageTome   | Will Yates  | 3 / 9                 
 VisageTome   | Mike Drucker| 1 / 3                 
<br/>

The first thing Jobmine would do is take a look at the offers from *Goggle* and *VisageTome*. In this case, it would notice that *Steve Brine* also ranked the *Goggle* position as one, and would match that student. Fantastic. In the case of *VisageTome*, *Mike Drucker* didn't accept the offer, so we will match position by the smallest sum of the rankings.

 Employer (E) | Student (S) | Ranking Sum 
 VisageTome   | Will Yates  | 12                    
 VisageTome   | Mike Drucker| 4                     
<br/>

*Goggle* only had one position available, so we no longer need to worry about it's other rankings, and we don't need to worry about *Steve Brine* either, because we already matched him. After getting the sums, it turns out that *Mike Drucker* gets matched with *VisageTome* anyway because both parties preferences were better in that combination than the alternatives.

It's a contrived example, but it works as a simple, quick explanation. Because of how Jobmine does rankings, they can ensure that a maximal number of students get matched with jobs, which looks good for the university, because [there are a lot of co-op students](http://findoutmore.uwaterloo.ca/coop/).

This past week, we did our rankings for our summer co-op position. We found three really good candidates, did our rankings, and waited to see how the matching would go.

...And we got none of the candidates. None. Despite the fact that one of the candidate reached out *to us*, we got *none* of them. I had a suspicion that this might happen, but still, it's a bit frustrating to say the least.

Part of the problem, as I see it, is that the three candidates were *really* good. It's a good problem to have, but because the candidates were *so good*, they likely received a lot of offers.

This got me thinking, 'How do these awesome candidates (e.g. candidates getting multiple offers) affect jobmine rankings?'

Then I thought back to my computer science courses. Then I went *through* my computer science course notes. **Then** I was confused.

Long story short, I need to brush up on my graph theory, because next post, I'm going to delve deeper into the ranking problem as an academic exercise, and then actually get to the heart of the matter: **How do multi-offer candidates affect jobmine matching?**
