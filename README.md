# What is this?

This is an autoswipe Tinder bot. As the name suggests, it swipes Tinder profiles for you.

The bot has some GUI implemented with Tkinter. In the GUI you can tweak following settings: 
1. Dislike profiles with empty description.
2. Dislike profiles, where description consists only of Instagram link.
3. Add "stop-words" to dislike profile, if found any. For example, you can add "420" as a stop-word, and if we encounter this as a separate word and not
a part of other word, we will dislike the profile. Regex pattern matching is used to achieve that.
4. Send message to a new match. You can add a bunch of random greeting messages and bot can randomly pick one to send to a new match, if we encounter one.
5. Set the chance of like.

To use this bot, clone the repo and launch TinderBot.py. You should have Google Chrome installed.

Here's a small video, demonstrating how it works:
https://youtu.be/dF6HK3yjGyU

Note that the GUI is in not in english. I have no intentions of implementing a proper localization system, as i dropped this project.

One more note is that when i was building this app, speed was crucial. I needed to test the hypothesis as quick is possible. Expect to see every programming sin, if you dare to read through code.
Speed/code quality proportions in this project are 100/0.

The market hypothesis i was trying out proved to be false, but i still had a lot of fun with browser automation and learning Python on fly as i wrote this project.
