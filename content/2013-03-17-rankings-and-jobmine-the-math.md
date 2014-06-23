layout: post
title: Rankings and Jobmine: The Math
slug: rankings-and-jobmine-the-math
date: 2013-03-17 15:00
comments: true
categories: 

Last week, I started talking about jobmine, and generally opened this question:

> How do multi-offer candidates affect jobmine matching?

I can't say that I've fully brushed up on my graph theory, but let's walk through the matching problem again.

Since I made a few mistakes in explaining how the matching works, I'll restate the matching problem with the constraints that we know.

**Problem:** How do we obtain a maximal number of matchings given the following constraints:  

- Employers rank only candidates that they would hire
- Employers rank a student between 1 (offer) and 9, or do not rank a student
- Employers may only make one offer per job position
- Students rank jobs for which they are ranked (from 1 to 9 in a similar fashion as employers)
- Students can see job offers, if they are ranked (but not which ranking), or if they were not ranked for a position
- "Employee and student ranking numbers are summed for each student-job"
- "Any jobs left blank by students are automatically assigned a value of '9'"
- "A random number is assigned to each student-job ranking ... [t]he algorithm looks for the lowest sum ... with the lowest random number. If both the student and the job are still available, then the student is assigned to that job, and the number of available openings for that job is reduced by one."
- "The matching algorithm then continues to look for the next lowest sum with the lowest random number, and so on, until all potential matches take place."

That's a lot of constraints (in fact, some of our constraints merely describe the algorithm), but it paints us a picture about how that matching takes place.

Let's take an example; I won't be silly, and this time I'll use actual companies. Since this is a graph theory problem, it would be really helpful to use an actual graph, but I am not up on my LaTeX...

In any case, let's use a simple example: an oversupply of jobs. I've included the random number column as it will make it easier to conduct the matching.

 Employer (E) | Student (S) | E Rank / S Rank | Random #
Google        | Jane        | 1 / 1           | 2
Facebook      | Jane        | 1 / 1           | 1
<br/>

Notice that *Jane* isn't restricted to ranking a single employer as number 1; she can rank whatever positions as whatever she wants, even with duplication of rank. In this case, it doesn't matter because she was offered by both companies. In this case, the matching will be determined by the random number. *Jane* is matched with Facebook (because it has a lower random number), and the *Google* position remains unfilled.

Right. So, who cares? We have one person two jobs, *of course* one job goes unfilled. The situation will be the same if we have mores students than positions.

Alright, so what about if we have an equal number of jobs and students?

 Employer (E) | Student (S) | E Rank / S Rank | Random #
Facebook      | Jane        | 1  / 2          | 4
Facebook      | John        | NR / -          | 2
Google        | Jane        | 1  / 1          | 3
Google        | John        | 2  / 1          | 1
<br/>

*John* wasn't ranked for *Facebook* in this case. We sort by lowest combined rank (with the lowest random value), meaning that we match *Jane* with *Google*. And, since *Google* has no more positions, *John* ends up with nothing. **Dang**.

This isn't maximal at all; we clearly could have had two people matched up with jobs, and instead we only got one. What could we have done about this? *Facebook* could have ranked *John*, but maybe they felt it wasn't a good fit. *Jane* could have accepted the other offer, but we presume she made her choice for a reason. The situation is the same for an employer: if a an employer's choices all accept offers from other companies.

What do we know then? Well, we know that even with an equal number of jobs, we won't necessarily get a maximal matching. But that doesn't tell us too much.

Well, we know that we can arrange the information differently. Instead of as a chart, let's establish some sort of *dominance relationship*.

    # ((E, S), (Ranking Sum, Random))
    ((Google, Jane), (2, 3)) > ((Google, John), (3, 1)) > ((Facebook, Jane), (3, 4))

Where does that get us? In this particular case, not very far. *Jane* is matched, and we remove *Google* and *Jane*, leaving no matches.

Let's build a bigger dominance relationship using the same setup, and add in a few additional connections:

 Employer (E) | Student (S) | E Rank / S Rank | Random #
Facebook      | Jane        | 1  / 2          | 4
Facebook      | John        | NR / -          | 2
Google        | Jane        | 1  / 1          | 3
Google        | John        | 2  / 1          | 1
Twitter       | Bob         | 2  / 1          | 6
Twitter       | John        | 1  / 2          | 5
<br/>

    ((Google, Jane), (2, 3)) >
    ((Google, John), (3, 1)) >
    ((Facebook, Jane), (3, 4)) >
    ((Twitter, John), (3, 5)) >
    ((Twitter, Bob), (3, 6))

We've got our relationship, what happens? Again, *Jane* is matched, removing all *Jane* and *Google* matches:

    ((Twitter, John), (3, 5)) >
    ((Twitter, Bob), (3, 6))

*John* finally has some luck, and ends up with *Twitter*.

If a job has *n* rankings, and a student is ranked for *m* jobs, then we remove *n + m - 1* listings whenever we match a student.

That seems pretty straightforward, but I think this might be getting us somewhere...

Let's assume we have a [complete, bipartite graph](http://en.wikipedia.org/wiki/Complete_bipartite_graph) (hey, I can remember *some* graph theory). In this arrangement, there are *ab* edges, where *a* is the number of vertices in one partition, and *b* the number of vertices in the other. In our case, *a* would be the number of jobs, and *b* the number of students.

For our purposes, let's use this as an example:

    a = 10
    b = 100
    total edges = ab = 1000

And we'll say that one particularly lucky student gets a lot of rankings:

    m = 10  # Student was ranked for every job
    n = 100 # Since this is a complete graph
    n + m - 1 = 109

In this case, more than 10% of the edges will disappear when this student is matched. Of course, this is not a great example because it's a complete bipartite graph, so we know that this will be the case for all of the students, and we know that we can only match up to 10 jobs, because there are only that many available to match.

But, we start to see the extent of things.

Let's take a similar scenario, except this time, each job onl ranks two students, and our golden boy is always the first choice. The second choice will be some random person we aren't concerned with.

    a = 10
    b = 100
    total edges = 2a = 20

    m = 10 # Student was offered every job, in this case
    n = 2  # Every job ranks only two students
    n + m - 1 = 11 

Now that one student has over *half* of the total edges removed when they are ranked.

Finally, we're getting somewhere.

We can see that, when a student is matched from the graph, our constraints on the graph are cosntricted. Naturally, we have less choice (because we have removed both a student and a job, and the accompanying edges), but we've also changed the nature of the graph. When a person is ranked or offered quite a few times, we end up disconnecting portions of the graph. A student (or employer) who may have been ranked number two may end up with nothing by simple virtue of large numbers of edges diappearing when matching occurs.

Things are still a bit fuzzy, but we now have some idea what effect students with a lot of rankings (or offers) have on the system.

A question for another day: is there a better way to match students? I'll also leave the question of what is 'fairer' for another day.
