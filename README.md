<p align="center">
  <img src="./img.png" alt="Project Banner" width="100%">
</p>

# [SkillSwap] 🎯

## Basic Details

### Team Name: [BIT&BYTE]

### Team Members
- Member 1: HARISREE S - COLLEGE OF ENGINEERING AND MANAGEMENT, PUNNAPRA
- Member 2: P S ASHNAGEETH -COLLEGE OF ENGINEERING AND MANAGEMENT, PUNNAPRA

### Hosted Project Link
[mention your project hosted link here]

### Project Description
SkillSwap is a peer-to-peer knowledge exchange platform that allows users to trade expertise without monetary transactions. It uses a "Tinder-style" matching system to connect people who want to learn a specific skill with mentors who are willing to teach it.

### The Problem statement
In traditional education, learning a new hobby or technical skill often requires expensive courses or subscriptions. Many people possess valuable skills but lack a platform to exchange them for the specific knowledge they need, creating a gap in community-based learning.

### The Solution
We built a web application where users list skills they "Give" and skills they "Want." The platform uses a mutual matching algorithm to pair users, provides a real-time messaging system for collaboration, and includes a secure Admin Panel to manage the community.

---

## Technical Details

### Technologies
- Languages used:Python, HTML5, CSS3 (Tailwind CSS)
- Frameworks used:Flask
- Libraries used:SQLite3 (Database), Jinja2 (Templating)
- Tools used: VS Code, Git
---

## Features

List the key features of your project:
- Feature 1: Tinder-style Discovery: Users can swipe right to "Like" or left to "Pass" on potential skill matches based on their learning goals.
- Feature 2: Mutual Matching System: A match is only established if both users express interest in each other's skills, ensuring a fair exchange.
- Feature 3: Real-time Messaging: Integrated chat interface allowing matched users to communicate and schedule their skill-swapping sessions
- Feature 4: Secure Admin Panel: A role-based dashboard for administrators to monitor platform statistics, manage the user database, and ban/delete accounts for safety.

---

## Implementation

#### Installation
```bash
pip install -r requirements.txt
```

#### Run
```bash
python app.py
```

---

## Project Documentation

#### Screenshots (Add at least 3)

!image1.png
Hero Section & Value Propositions: The SkillSwap landing page serves as the user's first point of contact, highlighting the core pillars of the platform: Skill Exchange, Smart Matching, and Community Building. It features a modern dark-mode aesthetic with clear navigation for discovery and authentication.

!image2.png
Advanced Admin Dashboard: The fully implemented management module. This view provides high-level metrics like Total Users and Mutual Matches, alongside a detailed user directory that shows exactly what skills are being traded across the network.

! image3.png
Personalized User Dashboard: This is the primary workspace for a registered user. It features two intuitive input sections: "Teach a Skill" (to list expertise they can offer) and "Learn a Skill" (to request new knowledge). The center area displays potential matches once skills are added to the system.


#### Diagrams

**System Architecture:**

!architecture.png
The SkillSwap platform is built on a Model-View-Controller (MVC) inspired architecture, utilizing a lightweight and efficient tech stack designed for rapid peer-to-peer data exchange.

1. Components & Tech Stack Interaction
Frontend (Views): Built using HTML5 and Tailwind CSS. It provides a responsive, "glassmorphism" styled interface for users to interact with the discovery deck and for admins to manage the platform.

Backend (Controller): Powered by Flask (Python). This acts as the central intelligence hub, handling routing, user session management (Role-Based Access Control), and the mutual matching logic.

Database (Model): A relational SQLite database stores all persistent data across four primary tables: users, skills, requests, and messages.

2. Data Flow & System Logic
The interaction between these components follows a structured flow as illustrated in your class and sequence diagrams:

Authentication & Authorization: When a user enters credentials on the Login Page, the Flask App sends a query to the DB to validate the user. Based on the role attribute (User or Admin), the app authorizes access to specific modules.

Skill Ownership: The system uses a One-to-Many relationship between the User class and the Skill class. One user can "own" multiple skills, which are stored with a user_id foreign key to maintain data integrity.

Matching Workflow:

The user inputs a "Want" request.

The Flask backend executes an SQL join to find other users offering that specific skill.

If a mutual "Right Swipe" is detected (stored in the requests table), the system enables the messaging component.

**Application Workflow:**

!workflow.png
User Authentication Workflow: This sequence diagram illustrates the secure communication between the client-side User, the Flask backend, and the SQLite database. It details the credential validation process, showing the conditional logic that either redirects a verified user to their dashboard or triggers an error message for invalid login attempts.
Landing Page (Images f5b843 & f7fa00):

SkillSwap Landing Page: The primary gateway to the platform, highlighting the core pillars of Skill Exchange, Smart Matching, and Community. It features a modern dark-mode UI with clear entry points for new and returning users.

User Dashboard (Images f7eb9a & f7f31d): Personalized Member Workspace: The central hub where users manage their learning journey. It includes intuitive forms for users to list their own expertise ("Teach a Skill") and request new skills they wish to acquire ("Learn a Skill").

Admin Panel (Images f5a8e7 & f7f6c0): Secure Administration Module: A high-level oversight interface for platform moderators. The enhanced view (Image f7f6c0) displays key metrics like Total Users and Mutual Matches, alongside a management table for monitoring active users and their specific skill sets.

Technical Environment (Image f77b3e): System Traceback: A terminal log showing a ModuleNotFoundError. This illustrates the necessity of installing project dependencies via pip install -r requirements.txt before launching the Flask server.

---

### For Scripts/CLI Tools:

#### Command Reference

**Basic Usage:**
```bash
python script.py [options] [arguments]
```

**Available Commands:**
- `command1 [args]` - Description of what command1 does
- `command2 [args]` - Description of what command2 does
- `command3 [args]` - Description of what command3 does

**Options:**
- `-h, --help` - Show help message and exit
- `-v, --verbose` - Enable verbose output
- `-o, --output FILE` - Specify output file path
- `-c, --config FILE` - Specify configuration file
- `--version` - Show version information

**Examples:**

```bash
# Example: Basic usage
python script.py input.txt
```

#### Demo Output

**Example: Basic Processing**

**Input:**
```
This is a sample input file
with multiple lines of text
for demonstration purposes
```

**Command:**
```bash
python script.py sample.txt
```

**Output:**
```
Processing: sample.txt
Lines processed: 3
Characters counted: 86
Status: Success
Output saved to: output.txt
```

---

## Project Demo

### Video
(https://youtu.be/j-ytheMXxaA)



### Additional Demos
[Add any extra demo materials/links - Live site, APK download, online demo, etc.]

---

## Team Contributions

- HARISREE S: Backend development (Flask routes, Mutual Match SQL logic), Database design (SQLite schema), and Authentication security.
- P S ASHNAGEETH: Frontend development (Tailwind CSS UI, Glassmorphism design), Admin Dashboard implementation, and Documentation.
- 

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Made with ❤️ at TinkerHub
