# What is this?

This is an autoswipe Tinder bot. As the name suggests, it swipes Tinder profiles for you. It uses Selenium browser automation framework and Tkinter GUI.

![image](https://github.com/ForestSquirrelDev/TinderBot/assets/82777171/9e79a431-265c-435b-83cc-8fb943e77ca6)

The bot does not use machine learning or any other fancy decision-making ways. It has a set of basic rules to pick from:
1. Dislike profiles with empty description.
2. Dislike profiles, where description consists only of Instagram link.
3. Add "stop-words" to dislike profile, if found any. For example, you can add "420" as a stop-word, and if we encounter this as a separate word, we will dislike the profile. Regex pattern matching is used.
4. Send message to a new match. You can add a bunch of random greeting messages and bot can randomly pick one to send to a new match, if we encounter one.
5. Set the chance of like.
6. Set your location.

This was supposed to be an executable file, but you can aswell clone the repository and launch TinderBot.py, which happens to be entry file. You should have Google Chrome installed.

Here's a small video, demonstrating how it works:
https://youtu.be/dF6HK3yjGyU

Note that the GUI is in not in english. I have no intentions of implementing a proper localization system, as i dropped this project.

Another very important note: when i was building this app, speed was crucial. I needed to test the hypothesis as quick is possible. Don't be surprised by lots of programming sins as you read through code.
Speed/code quality proportions in this project are 100/0.

The customer market hypothesis i was trying out proved to be false, but i still had a lot of fun with browser automation and learning Python on fly as i wrote this project.
