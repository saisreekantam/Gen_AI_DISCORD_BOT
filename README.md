# Night-owls

## 1) Track - Discord Bot
**Contributors:** 
- Sreekantam Sai Venkat (IMT2023501)
- Abhinav Kishan (IMT2023580)
- Pammi Nanda Mitra (IMT2023583)

## 2) Problem Statement
**Creating a Discord bot involves designing and implementing various features and functionalities to enhance the user experience within a Discord server.**

## 3) Goal
**The goal is to create a versatile Discord bot that enables users to:**
- To solve their doubt with the help of a generative AI which can answer any sort of question.
- Announce coding contests and create dedicated channels for contests.
- Provide and solve coding problems sourced from platforms like LeetCode and Codeforces.
- To facilitate user to learn via repl sessions.
- Support code submission, review, and collaboration within Discord.
- Offer features such as note uploading, recommendation,search on stackoverflow or AI chatbot, GitHub and YouTube search, and code execution.

## 4) Features
**a) Coding Contest Management:**  
The bot effectively manages coding contests by allowing users to announce, join, and compete in contests, providing a structured and engaging experience for participants.

**b) Problem of the Day:**  
It offers a daily coding problem feature, enhancing users' skills by regularly challenging them with new problems and providing relevant resources.

**c) Interactive Gameplay:**  
The bot facilitates interactive gameplay, such as collaborative coding sessions, quiz competitions, and problem-solving challenges, fostering community engagement and learning.

**d) AI Integration:**  
Integration with generative AI enables users to interact with AI-based features like asking questions, receiving recommendations, and generating content, enhancing the bot's utility and interactivity.

**e) Content Recommendations:**  
Users can receive recommendations for LeetCode problems based on their profile, allowing them to focus on relevant challenges and improve their problem-solving skills effectively.

**f) Stack Overflow Search:**  
Integration with Stack Overflow enables users to search for programming-related queries directly within Discord, providing quick access to relevant information and solutions.

**g) Leaderboard and Ratings:**  
The bot maintains a leaderboard of users based on their performance in coding challenges, encouraging healthy competition and skill development within the community. Additionally, it tracks user ratings, reflecting their progress and accomplishments over time.

## 5) Tech Stack
- *Discord.py*: Library for creating Discord bots in Python.
- *Python*: Programming language used for bot development.
- *requests*: HTTP library for making API requests.
- *Beautiful Soup (bs4)*: Library for web scraping.
- *google.generativeai (gemini-pro)*: Library for AI text generation.
- *Other Python libraries*: speech_recognition, gtts (Google Text-to-Speech)

## 6) Commands
**a) >jarvis [prompt]:**  
Interacts with a generative AI model to generate content based on the provided prompt.

**b) >create_channel [channel_name]:**  
Creates a new channel for a contest with the specified name.

**c) >contest [platform] [contest_name] [start_time]:**  
Announces a coding contest. Replace [platform] with the platform name, [contest_name] with the name of the contest, and [start_time] with the start time of the contest.

**d) >visualise:**  
Opens the PyTutor website, allowing users to visualize Python code execution step by step.

**e) >schedule_event [event_name] [event_date]:**  
Schedules an event with the specified name and date (format: YYYY-MM-DD HH:MM).

**f) >stackoverflow [query]:**  
Searches Stack Overflow for the given query and returns relevant results.

**g) >youtube_search [query]:**  
Searches YouTube for the given query and returns the search results with links.

**h) >github_search [query]:**  
Searches for related queries on GitHub and returns the results, including repository names, descriptions, and links.

**i) >upload_note [note_name] [note_link]:**  
Uploads a PDF note with the given name and link.

**j) >recommend_note [note_name]:**  
Recommends a stored note by providing its link based on the given name.

**k) >leetcode_profile [username]:**  
Displays LeetCode profile information for the specified username.

**l) >recommend_problems [username]:**  
Recommends next problems to solve based on a user's LeetCode profile.

**m) >start_contest [contest_name] [duration_minutes] [problem_ids]:**  
Starts a coding contest with the specified name, duration in minutes, and a list of problem IDs.

**n) >submit_solution [contest_name] [problem_id]:**  
Allows users to submit a solution to a coding contest by providing the contest name and problem ID.

**o) >endcontest [contest_name]:**  
Ends a coding contest with the specified name and displays the final leaderboard.

**p) >compete [channel] [contest_name]:**  
Starts a coding contest in the specified channel and invites users to compete against each other.

**q) >check:**  
Displays ongoing contests, including channel, contest name, and participants.

**r) >invite_link:**  
Generates an invite link for the server, allowing users to invite others to join.

To use any of these commands, simply type the command followed by the required parameters (if any) in a Discord channel where the bot is present. For example, to announce a coding contest, you would type >contest Codeforces WeeklyContest 2024-04-10 08:00 UTC.

## 7) Deployment (if Done)
**If deploying the bot:**
- Host the bot script on a server or use a hosting service like Heroku or AWS.
- Set up environment variables for sensitive information (e.g., API keys).
- Configure the bot to run continuously using tools like pm2 or screen.

## 8) Applications of Your Idea
**The Discord bot can be used for:**
- Managing and hosting coding contests within coding communities.
- Facilitating problem-solving discussions and collaborations.
- Enhancing engagement and interaction among community members.
- Providing resources, notes, and external content search capabilities.
- Enabling code sharing, review, and execution directly within Discord.

## 9) Further Improvements
**Future improvements to the bot could include:**
- Implementing more advanced AI capabilities for problem generation or solution evaluation.
- Integrating with more coding platforms for problem retrieval and contest management.
- Enhancing code execution features with sandboxing and security measures.
- Adding user authentication and profile management for personalized experiences.
- Implementing more interactive and engaging features for coding challenges and quizzes.
- Optimizing performance and scalability for larger communities and usage patterns.
