layout: post
title: The Perfect Blog?
slug: the-perfect-blog
date: 2012-02-17 16:12
comments: true
categories: 
I am a pretty lazy guy.

Maybe lazy isn't the right way to put it, but I definitely do not enjoy doing work over, especially repetitive work. I'm also a technical guy, so it can be pretty easy to get distracted by details instead of looking at the big picture. I figure those are probably the biggest reasons I have such a hard time getting into the rhythm of blogging. Everytime I get started, I go through the following steps:

- Say to myself "I am going to write a blog"
    - Sure, why not! I'm a technical guy, I can share my "insights", and generally be popular! AWESOME!
- Set up a web host for my blog
    - Alright, so I'm not exactly doing what I want to do, but I want this to be my blog, not some hosted thing. I'm learning, right?!
- Install the database, and blogging software
    - Follow the steps, run into a few problems, finally get things running. I guess I could have just made some HTML files, but this'll just make it easy for me to write in my blog, right? Sure!
- Start thinking about theming, and make a half-finished theme before realizing I should be writing a blog
    - Why is everything written in this weird templating language? I mean, I can figure it out, but it seems like a lot of work...
- Write some moronic first post to get myself motivated
    - I am the best! I will write this blog every day!
- Keep up my efforts for a week or two
    - Well, it's better than nothing right?
- Complain that everything I've done sucks, get busy with other projects, and abandon the blog
    - Too much stuff going on! How did I manage to do this every day in highschool?!
- Try again a few weeks later, never to update again
    - I can get back into this, it's not that hard!
- Repeat this about once a year
    - Fuck it. Let's try this again.

...And that's generally how it goes, with a few variations. Against my better judgement, I'm giving it another shot. Why? Because I think that the tools I'm using lend themselves a lot better to what it is that I actually want to do: blog!

Enter [Octopress](http://octopress.org).

One of the problems I had with [Wordpress](http://wordpress.org) is that there is a lot to take you "out of the action", so to speak. There're a lot of plugins to be installed, making sure you have the right version of this or that, installing the database, using Wordpress' theming shenanigans, worrying about security. Argh... it's just annoying.

One of the nice things about Octopress is its all HTML / Javascript / CSS. You write your blog post in [Markdown](http://daringfireball.net/projects/markdown/syntax) (which is just a really simple syntax that is used in places like [StackExchange](http://stackexchange.com)), and it will generate a static HTML file.

That's it.

Well, it's not quite that easy. When I want to create a new blog post, I just run this command:

```
rake new_post["post name"]
```

...And go edit the file, and that's it.

It has a lot of other nice features too; it uses sass (a superset of CSS) and compass (a set of scripts for CSS to make it easy to do things like gradients), and has a lot of prebuilt plugins.

Yeah, it's all managed via the command line, but that doesn't really bother me. It's really, really simple, and that's exactly what I need.

So, we'll see how things go. I'm happy with octopress, and I'd recommend it. We'll see how long I can keep blogging though.
