import discord
from discord.ext import commands,tasks
import webbrowser
import random
import asyncio
import datetime
import requests
import google.generativeai as genai
from bs4 import BeautifulSoup
import speech_recognition as sr
from gtts import gTTS
import os
bot = commands.Bot(command_prefix=">", intents=discord.Intents.all())
API_KEY="PUT_YOUR_GEMINI_API_KEY"
# Initialize generative AI model
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro',
                               safety_settings=[
                                   {
                                       "category": "HARM_CATEGORY_DANGEROUS",
                                       "threshold": "BLOCK_NONE",
                                   },
                                   {
                                       "category": "HARM_CATEGORY_HARASSMENT",
                                       "threshold": "BLOCK_NONE",
                                   },
                                   {
                                       "category": "HARM_CATEGORY_HATE_SPEECH",
                                       "threshold": "BLOCK_NONE",
                                   },
                                   {
                                       "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                                       "threshold": "BLOCK_NONE",
                                   },
                                   {
                                       "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                                       "threshold": "BLOCK_NONE",
                                   },
                               ]
                               )

# Mock database for demonstration
class MockDatabase:
    def _init_(self):
        self.contests = []
        self.notes = {}

    async def add_contest(contest):
        self.contests.append(contest)

    async def get_contests():
        return self.contests

    async def get_problem():
        # This is a placeholder function to demonstrate the concept
        # You should replace this with your actual implementation
        leetcode_problems = [
            {
                'title': 'Two Sum',
                'description': 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may assume that each input would have exactly one solution, and you may not use the same element twice. You can return the answer in any order.',
                'link': 'https://leetcode.com/problems/two-sum/'
            },
            {
                'title': 'Add Two Numbers',
                'description': 'You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list. You may assume the two numbers do not contain any leading zero, except the number 0 itself.',
                'link': 'https://leetcode.com/problems/add-two-numbers/'
            },
            {
                'title': 'Longest Substring Without Repeating Characters',
                'description': 'Given a string s, find the length of the longest substring without repeating characters.',
                'link': 'https://leetcode.com/problems/longest-substring-without-repeating-characters/'
            }
        ]
        return random.choice(leetcode_problems)

    async def upload_note(self, note_name, note_link):
        self.notes[note_name] = note_link

    async def recommend_note(self, note_name):
        return self.notes.get(note_name, "Note not found.")


# Command to open PyTutor website
@bot.command("visualise")
async def visualize(ctx):
    """Visualise the code using PyTutor."""
    py_tutor_url = "http://pythontutor.com/"
    await ctx.send(f"PyTutor website: {py_tutor_url}")

# Command to announce a contest
@bot.command("contest")
async def announce_contest(ctx, platform: str, contest_name: str, start_time: str):
    """Announce a coding contest."""
    contest_info = {
        'platform': platform,
        'name': contest_name,
        'start_time': start_time
    }
    await database.add_contest(contest_info)
    await ctx.send(f"Contest announced: {contest_name} on {platform}, starting at {start_time}")

# Command to send the problem of the day
@bot.command(name="give_problem")
async def problem_of_the_day(ctx):
    """Send the problem of the day."""
    problem = await MockDatabase.get_problem()
    problem_message = f"*Problem of the Day*\n\nTitle: {problem['title']}\nDescription: {problem['description']}\n[Link to Problem]({problem['link']})"
    await ctx.send(problem_message)
BASE_URL = "https://api.github.com"
@bot.command(name="create_channel")
async def create_contest_channel(ctx, channel_name: str):
    """Create a new channel for a contest."""
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)

    if existing_channel:
        await ctx.send(f"A channel with the name '{channel_name}' already exists.")
    else:
        # Create a new text channel
        await guild.create_text_channel(channel_name)
        await ctx.send(f"Contest channel '{channel_name}' created successfully.")
@bot.command(name="github_search")
async def github_search(ctx, query: str):
    """Search for related queries on GitHub."""
    search_url = f"{BASE_URL}/search/repositories?q={query}"
    response = requests.get(search_url)

    if response.status_code == 200:
        data = response.json()
        if data.get('items'):
            search_results = data['items']
            result_count = len(search_results)
            output = f"Found {result_count} results for '{query}' on GitHub:\n"
            for result in search_results:
                output += f"• [{result['name']}]({result['html_url']}) - {result['description']}\n"
            await ctx.send(output)
        else:
            await ctx.send(f"No results found for '{query}' on GitHub.")
    else:
        await ctx.send("Failed to fetch results from GitHub.")
# Command to ask AI
@bot.command(name="jarvis")
async def askai(ctx: commands.Context, *, prompt: str):
    response = model.generate_content(prompt)
    await ctx.reply(response.text)
#command to upload notes
@bot.command(name="upload_note")
async def upload_note(ctx, note_name: str, note_link: str):
    """Upload a PDF note."""
    await MockDatabase.upload_note(note_name, note_link)
    await ctx.send(f"Note '{note_name}' uploaded successfully.")

# Command to recommend a note
@bot.command(name="recommend_note")
async def recommend_note(ctx, note_name: str):
    """Recommend a stored note."""
    note_link = await MockDatabase.recommend_note(note_name)
    if note_link != "Note not found.":
        await ctx.send(f"Here's the link for '{note_name}': {note_link}")
    else:
        await ctx.send("Note not found.")
#command to do a youtube search
@bot.command(name="youtube_search")
async def youtube_search(ctx, *, query: str):
    """Search YouTube for the given query."""
    search_query = "+".join(query.split())
    youtube_url = f"https://www.youtube.com/results?search_query={search_query}"
    await ctx.send(f"Here's the YouTube search results for '{query}':\n{youtube_url}")
ongoing_contests = {}
#command to compete with friends
@bot.command(name="compete")
async def compete(ctx, channel: discord.TextChannel, contest_name: str):
    """Start a coding contest in the specified channel."""
    await ctx.send(f"{ctx.author.mention} has initiated a coding contest '{contest_name}' in channel {channel.mention}.")
    await ctx.send("Who would you like to compete against? Mention the user.")

    def check(message):
        return message.author != bot.user and message.channel == ctx.channel

    try:
        competition_partner = await bot.wait_for('message', timeout=60.0, check=check)
        partner = competition_partner.mentions[0]
        await ctx.send(f"{partner.mention}, {ctx.author.mention} has challenged you to compete in the coding contest '{contest_name}'! Type 'accept' to join.")

        def accept_check(message):
            return message.author == partner and message.content.lower() == "accept" and message.channel == ctx.channel

        try:
            acceptance = await bot.wait_for('message', timeout=60.0, check=accept_check)
            await ctx.send(f"{partner.mention} has accepted the challenge! The coding contest is now starting.")
            ongoing_contests[channel.id] = (ctx.author, partner, contest_name)
        except TimeoutError:
            await ctx.send(f"{partner.mention} did not accept the challenge. Contest canceled.")
    except TimeoutError:
        await ctx.send("No one responded. Contest canceled.")
#command to check whether 
@bot.command(name="check")
async def show_ongoing_contests(ctx):
    """Show ongoing contests."""
    if ongoing_contests:
        message = "Ongoing Contests:\n"
        for channel_id, (user1, user2, contest_name) in ongoing_contests.items():
            channel = bot.get_channel(channel_id)
            message += f"Channel: {channel.mention}, Contest Name: {contest_name}, Participants: {user1.mention} vs {user2.mention}\n"
        await ctx.send(message)
    else:
        await ctx.send("No ongoing contests.")
# Event handler for bot's on_ready event
   

class Contest:
    def _init_(self, ctx, leetcode_problems, codeforces_problems, duration):
        self.ctx = ctx
        self.leetcode_problems = leetcode_problems
        self.codeforces_problems = codeforces_problems
        self.solved_problems = set()
        self.duration = duration
        self.end_time = None
        self.leaderboard = {}

    def get_next_problem(self):
        for problem_id in self.leetcode_problems:
            if problem_id not in self.solved_problems:
                return "leetcode", problem_id
        for problem_id in self.codeforces_problems:
            if problem_id not in self.solved_problems:
                return "codeforces", problem_id
        return None, None

    def start_timer(self):
        self.end_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=self.duration)

    def is_contest_over(self):
        return datetime.datetime.utcnow() >= self.end_time

    def add_score(self, user_id, score):
        if user_id not in self.leaderboard:
            self.leaderboard[user_id] = 0
        self.leaderboard[user_id] += score

    def get_leaderboard(self):
        sorted_leaderboard = sorted(self.leaderboard.items(), key=lambda x: x[1], reverse=True)
        return sorted_leaderboard

contests = {}
#command to start_contest
@bot.command(name="start_contest")
async def start_contest(ctx, contest_name: str, duration_minutes: int, *problem_ids: str):
    """Start a coding contest."""
    leetcode_problems = [pid for pid in problem_ids if pid.startswith("lc")]
    codeforces_problems = [pid for pid in problem_ids if pid.startswith("cf")]
    duration = duration_minutes * 60
    contest = Contest(ctx, leetcode_problems, codeforces_problems, duration)
    contest.start_timer()
    contests[contest_name] = contest

    # Create a new channel for the contest
    guild = ctx.guild
    category = discord.utils.get(guild.categories, name="Contests")
    if not category:
        category = await guild.create_category("Contests")
    channel = await category.create_text_channel(contest_name)

    # Send initial message with contest details
    await channel.send(f"The contest '{contest_name}' has started for {duration_minutes} minutes.")
    await channel.send("Here are your problems:")

    # Send the first problem
    await send_next_problem(channel, contest)

async def send_next_problem(channel, contest):
    platform, problem_id = contest.get_next_problem()
    if problem_id is None:
        await channel.send("No more problems left in the contest.")
        return
    if platform == "leetcode":
        await channel.send(f"LeetCode problem: https://leetcode.com/problems/{problem_id}/")
    elif platform == "codeforces":
        await channel.send(f"Codeforces problem: https://codeforces.com/problemset/problem/{problem_id}")
    else:
        await channel.send("Unknown platform.")
    await channel.send(f"Solve this problem and submit your solution using >submit_solution <problem_id>")

@bot.command(name="submit_solution")
async def submit_solution(ctx, contest_name: str, problem_id: str):
    """Submit a solution to a coding contest."""
    if contest_name not in contests:
        await ctx.send("No contest with that name exists.")
        return
    contest = contests[contest_name]
    if contest.is_contest_over():
        await ctx.send("The contest is already over.")
        return
    platform, current_problem_id = contest.get_next_problem()
    if current_problem_id is None:
        await ctx.send("No more problems left in the contest.")
        return
    if problem_id != current_problem_id:
        await ctx.send("You must solve the current problem before moving to the next one.")
        return
    contest.solved_problems.add(problem_id)
    contest.add_score(ctx.author.id, 1)  # Add 1 point for each solved problem
    await ctx.send(f"Problem '{problem_id}' solved! Your next problem is from {platform.capitalize()}.")
    # Send the next problem
    channel = ctx.channel
    await send_next_problem(channel, contest)

@tasks.loop(seconds=10)
async def check_contest_timers():
    for contest_name, contest in list(contests.items()):
        if contest.is_contest_over():
            channel = discord.utils.get(contest.ctx.guild.channels, name=contest_name)
            if channel:
                await channel.send("The contest is over.")
            del contests[contest_name]
            await end_contest(contest.ctx, contest_name)
#command to end_contest
@bot.command(name="endcontest")
@commands.has_permissions(administrator=True)  # Ensure only admins can end the contest
async def end_contest(ctx, contest_name: str):
    """End a coding contest."""
    if contest_name not in contests:
        await ctx.send("No contest with that name exists.")
        return
    contest = contests.pop(contest_name)
    leaderboard = contest.get_leaderboard()
    leaderboard_message = "Leaderboard:\n"
    for idx, (user_id, score) in enumerate(leaderboard, start=1):
        user = ctx.guild.get_member(user_id)
        user_name = user.name if user else f"Unknown User ({user_id})"
        leaderboard_message += f"{idx}. {user_name}: {score} points\n"
    await ctx.send(f"The contest '{contest_name}' has ended. Thanks for participating!\n{leaderboard_message}")

# Event handler for bot's on_ready event
#command to give_problem_on
@bot.command(name="give_problems_on")
async def recommend_leetcode(ctx, query: str):
    """Recommend LeetCode problems based on the given query."""
    search_url = f"https://leetcode.com/problems/{query}/"
    response = requests.get(search_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        problems = soup.find_all('div', class_='question-title')

        if problems:
            await ctx.send(f"Here are some LeetCode problems related to '{query}':")
            for problem in problems[:5]:  # Limiting to 5 recommendations
                problem_title = problem.a.text.strip()
                problem_link = f"https://leetcode.com{problem.a['href']}"
                await ctx.send(f"• [{problem_title}]({problem_link})")
        else:
            await ctx.send(f"No LeetCode problems found related to '{query}'.")
    else:
        await ctx.send("Failed to fetch LeetCode problems.")
def get_user_profile(username):
    """Fetch user profile information from LeetCode API."""
    api_url = f"https://leetcode.com/{username}/"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
def get_recommendations(username):
  """Get recommendations for the next problems to solve."""
  # Your recommendation algorithm here
  # Example: Fetch random problems from LeetCode API or use user's solved problems for similarity

  # For simplicity, we'll just return a list of random problem IDs
  return [str(random.randint(1, 1000)) for _ in range(3)]


code_reviews = {}
#command to submit_code_for_analysis
@bot.command(name="submit_code")
async def submit_code(ctx, *, code: str):
    """Submit code for review."""
    user_id = ctx.author.id
    if user_id in code_reviews:
        await ctx.send("You have already submitted code for review. Please wait for feedback on your previous submission.")
    else:
        code_reviews[user_id] = code
        await ctx.send("Your code has been submitted for review. Please wait for feedback.")
#command for reviewing_code
@bot.command(name="review_code")
async def review_code(ctx, user: discord.User):
    """Review submitted code."""
    reviewer_id = ctx.author.id
    if reviewer_id == user.id:
        await ctx.send("You cannot review your own code.")
    elif user.id not in code_reviews:
        await ctx.send("No code found for the specified user.")
    else:
        code = code_reviews[user.id]
        await ctx.send(f"Here's the code submitted by {user.mention} for review:\n{code}")
        await ctx.send(f"{ctx.author.mention}, please provide feedback on the code.")
#command for collaborating with replit
@bot.command(name="collaborate")
async def collaborate(ctx):
    """Start a collaborative coding session using Repl.it."""
    # Send a message prompting the user to join the collaboration session
    await ctx.send("Let's start a collaborative coding session! Click the link below to join:")

    # Generate a new Repl.it collaboration link
    response = requests.post("https://repl.it/data/repls", json={"language": "python"})
    if response.status_code == 200:
        data = response.json()
        repl_id = data["id"]
        repl_link = f"https://repl.it/@{data['username']}/{data['id']}?lite=true"
        await ctx.send(repl_link)
    else:
        await ctx.send("Failed to generate collaboration link. Please try again later.")
#command to run code
@bot.command(name="runcode")
async def run_code(ctx, language: str, *, code: str):
    """Compile and execute code."""
    # Map Discord command language aliases to JDoodle language codes
    language_aliases = {
        "python": "python3",
        "java": "java",
        "c": "c",
        "cpp": "cpp",
    }

    # Check if the provided language is supported
    if language.lower() not in language_aliases:
        await ctx.send("Unsupported programming language.")
        return

    # Map Discord command language aliases to JDoodle language codes
    jdoodle_language = language_aliases[language.lower()]

    # Construct the request payload
    payload = {
        "clientId": "YOUR_JDOODLE_CLIENT_ID",
        "clientSecret": "YOUR_JDOODLE_CLIENT_SECRET",
        "script": code,
        "language": jdoodle_language,
        "versionIndex": "0",
    }

    # Make the API request to JDoodle
    response = requests.post("https://api.jdoodle.com/v1/execute", json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if "output" in data:
            await ctx.send("Output:\n" + data["output"])
        elif "error" in data:
            await ctx.send("Error:\n" + data["error"])
        else:
            await ctx.send("Unknown error occurred.")
    else:
        await ctx.send("Failed to execute code. Please try again later.")
#command for maintaing leetcode_profile
@bot.command("leetcode_profile")
async def leetcode_profile(ctx, username: str):
  """Display LeetCode profile information."""
  profile_data = get_user_profile(username)
  if profile_data:
      solved_count = profile_data.get("num_solved", 0)
      submission_count = profile_data.get("num_total_submitted", 0)
      acceptance_rate = profile_data.get("ac_easy", 0) + profile_data.get("ac_medium", 0) + profile_data.get("ac_hard", 0)
      ranking = profile_data.get("ranking", "Not ranked")

      profile_message = (
          f"*LeetCode Profile for {username}:*\n"
          f"Solved Problems: {solved_count}\n"
          f"Total Submissions: {submission_count}\n"
          f"Acceptance Rate: {acceptance_rate:.2f}%\n"
          f"Global Ranking: {ranking}\n"
      )
      await ctx.send(profile_message)
  else:
      await ctx.send("Failed to fetch LeetCode profile. Please check the username and try again.")
badges = {
  "Gold Badge": "🥇",
  "Silver Badge": "🥈",
  "Bronze Badge": "🥉"
}

# Mock leaderboard for demonstration
leaderboard = {
  "user1": 100,
  "user2": 80,
  "user3": 60,
  "user4": 40,
  "user5": 20
}

# Function to assign roles (badges or stickers) to users based on their position in the leaderboard
async def assign_badges_from_leaderboard(guild):
  for idx, (user_id, score) in enumerate(leaderboard.items(), start=1):
      user = guild.get_member(user_id)
      if user:
          if idx == 1:
              await award_badge(guild, user, "Gold Badge")
          elif idx == 2:
              await award_badge(guild, user, "Silver Badge")
          elif idx == 3:
              await award_badge(guild, user, "Bronze Badge")
          else:
              break

# Function to assign roles (badges or stickers) to users based on their performance
async def award_badge(guild, user, badge_name):
  role = discord.utils.get(guild.roles, name=badge_name)
  if role:
      await user.add_roles(role)
      return True
  else:
      return False

# Command to manually award a badge or sticker to a user
@bot.command(name="award_badge")
async def award_badge_command(ctx, user: discord.Member, badge_name: str):
  """Manually award a badge or sticker to a user."""
  guild = ctx.guild
  if badge_name in badges:
      result = await award_badge(guild, user, badge_name)
      if result:
          await ctx.send(f"{user.mention} has been awarded the {badge_name} {badges[badge_name]}.")
      else:
          await ctx.send(f"Failed to award the {badge_name}.")
  else:
      await ctx.send("Invalid badge name.")

# Command to automatically assign badges or stickers to top performers based on the leaderboard
@bot.command(name="assign_badges")
async def assign_badges_command(ctx):
  """Automatically assign badges or stickers to top performers based on the leaderboard."""
  guild = ctx.guild
  await assign_badges_from_leaderboard(guild)
  await ctx.send("Badges or stickers assigned based on the leaderboard.")
#command to give problems from leetcode
@bot.command("recommend_problems")
async def recommend_problems(ctx, username: str):
  """Recommend next problems to solve based on LeetCode profile."""
  recommendations = get_recommendations(username)

  if recommendations:
      message = "*Recommended Problems:*\n"
      for idx, problem_id in enumerate(recommendations, start=1):
          message += f"{idx}. [Problem {problem_id}](https://leetcode.com/problems/{problem_id})\n"
      await ctx.send(message)
  else:
      await ctx.send("Failed to fetch recommendations. Please try again later.")

scheduled_events = []

# Command to schedule an event
@bot.command(name="schedule_event")
async def schedule_event(ctx, event_name: str, event_date: str):
    """Schedule an event."""
    try:
        # Convert event_date string to datetime object
        event_datetime = datetime.datetime.strptime(event_date, "%Y-%m-%d %H:%M")
        # Append event details to the scheduled_events list
        scheduled_events.append((event_name, event_datetime))
        await ctx.send(f"Event '{event_name}' scheduled for {event_datetime}.")
    except ValueError:
        await ctx.send("Invalid date format. Please use YYYY-MM-DD HH:MM.")

# Task to check for scheduled events
@tasks.loop(seconds=60)  # Check every minute
async def check_scheduled_events():
    current_time = datetime.datetime.now()
    for event in scheduled_events:
        event_name, event_datetime = event
        if current_time >= event_datetime:
            # Remove the event from the list
            scheduled_events.remove(event)
            # Send a reminder message for the event
            channel = bot.get_channel(YOUR_CHANNEL_ID)  # Replace YOUR_CHANNEL_ID with the ID of the channel to send reminders
            if channel:
                await channel.send(f"Reminder: Event '{event_name}' is happening now!")
def search_stackoverflow(query):
  stackoverflow_api_url = "https://api.stackexchange.com/2.3/search"
  params = {
      "site": "stackoverflow",
      "intitle": query,
      "order": "relevance"
  }
  response = requests.get(stackoverflow_api_url, params=params)
  if response.status_code == 200:
      data = response.json()
      if data.get("items"):
          # Extract relevant information from the search results
          results = data["items"]
          search_results = []
          for result in results[:5]:  # Limiting to 5 search results
              title = result["title"]
              link = result["link"]
              search_results.append((title, link))
          return search_results
      else:
          return None
  else:
      return None

class Game:
  def _init_(self, ctx, opponent):
      self.ctx = ctx
      self.opponent = opponent
      self.channel = None
      self.questions = {"What is 2 + 2?": "4"}  # Quiz questions and answers
      self.completed_players = set()

  async def start(self):
      # Create a new text channel for the game
      guild = self.ctx.guild
      category = discord.utils.get(guild.categories, name="Coding Competitions")
      if not category:
          category = await guild.create_category("Coding Competitions")
      self.channel = await category.create_text_channel(f"{self.ctx.author.display_name}-vs-{self.opponent.display_name}")
      await self.channel.send(f"Game started between {self.ctx.author.mention} and {self.opponent.mention}!")

      # Send the first question
      await self.send_question()

  async def send_question(self):
      for question, _ in self.questions.items():
          await self.channel.send(question)
          break  # Send only the first question

  async def handle_answer(self, message):
      if message.author in (self.ctx.author, self.opponent):
          player = message.author
          answer = message.content.strip().lower()
          correct_answer = self.questions.get("What is 2 + 2?")
          if player not in self.completed_players and answer == correct_answer:
              self.completed_players.add(player)
              await self.channel.send(f"{player.mention} has completed the game!")
              if len(self.completed_players) == 1:
                  await self.channel.send(f"{player.mention} wins the gold medal!")
              elif len(self.completed_players) == 2:
                  await self.channel.send(f"{player.mention} wins the silver medal!")
              else:
                  await self.channel.send(f"{player.mention} wins the bronze medal!")
          else:
              await self.channel.send("Incorrect answer or unauthorized player.")
#command to create game
@bot.command(name="create_game")
async def create_game(ctx, opponent: discord.Member):
  """Create a new channel for a coding competition or quiz between the user and their opponent."""
  # Check if the opponent is not the command invoker
  if opponent == ctx.author:
      await ctx.send("You cannot compete against yourself.")
      return

  game = Game(ctx, opponent)
  await game.start()

@bot.event
async def on_message(message):
  if message.author == bot.user:
      return

  # Check if the message is sent in a game channel
  channel = message.channel
  if isinstance(channel, discord.TextChannel) and channel.category and channel.category.name == "Coding Competitions":
      # Handle answers to quiz questions
      game = get_game_from_channel(channel)
      if game and message.content.strip().lower() in game.questions.values():
          await game.handle_answer(message)

  await bot.process_commands(message)

def get_game_from_channel(channel):
  # Placeholder function to get the game object from the channel
  # You need to implement this based on your bot's structure
  return None

# Command to search Stack Overflow
# Mock database for demonstration
class Database:
    def _init_(self):
        self.problems = {
            "Problem 1": {"rating": 100},
            "Problem 2": {"rating": 150},
            "Problem 3": {"rating": 200}
        }
        self.ratings = {}

    def get_problems(self):
        return self.problems

    def get_ratings(self, user):
        return self.ratings.get(user, 1000)  # Default rating is 1000

    def update_rating(self, user, new_rating):
        self.ratings[user] = new_rating

database = Database()
#command to solve challenge problems
@bot.command(name="challenge_problems")
async def challenge_problems(ctx):
    """Display the list of challenge problems."""
    problems = database.get_problems()
    problem_list = "\n".join([f"{problem}: {data['rating']} rating" for problem, data in problems.items()])
    await ctx.send(f"*Challenge Problems:*\n{problem_list}")

@bot.command(name="solve")
async def solve_problem(ctx, problem_name: str):
    """Solve a challenge problem."""
    problems = database.get_problems()
    if problem_name in problems:
        problem_rating = problems[problem_name]["rating"]
        user_rating = database.get_ratings(ctx.author)
        new_rating = user_rating + problem_rating
        database.update_rating(ctx.author, new_rating)
        await ctx.send(f"{ctx.author.mention} solved {problem_name} and gained {problem_rating} rating points! Your new rating is {new_rating}.")
    else:
        await ctx.send("Invalid problem name.")
#command to see leaderboard 
@bot.command(name="leaderboard")
async def leaderboard(ctx):
    """Display the server's leaderboard."""
    ratings = sorted(database.ratings.items(), key=lambda x: x[1], reverse=True)
    leaderboard = "\n".join([f"{idx+1}. {user}: {rating} rating" for idx, (user, rating) in enumerate(ratings)])
    await ctx.send(f"*Leaderboard:*\n{leaderboard}")
#command to search query on stackoverflow
@bot.command(name="stackoverflow")
async def stackoverflow_search(ctx, *, query: str):
  """Search Stack Overflow for the given query."""
  search_results = search_stackoverflow(query)
  if search_results:
      response_message = "*Search Results:*\n"
      for idx, (title, link) in enumerate(search_results, start=1):
          response_message += f"{idx}. [{title}]({link})\n"
      await ctx.send(response_message)
  else:
      await ctx.send("No results found on Stack Overflow.")
#command to creat an invite link for server
@bot.command(name="invite_link")
async def server_invite(ctx):
    """Generate an invite link for the server."""
    invite = await ctx.channel.create_invite(max_age=3600, max_uses=1)
    await ctx.send(f"Here's the invite link for the server: {invite}")
@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name}!")

# Run the bot
bot.run(#API key)
