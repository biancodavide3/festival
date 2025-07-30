# Turin All Star 2025

## Description

This web application manages a **single annual music festival** taking place over one weekend (Friday to Sunday), in Turin.

There are **two types of registered users**:

-  **Participants**: can browse the schedule and purchase tickets.

-  **Organizers**: can manage performances and monitor ticket sales.

### Participants

- elisa@gmail.com, giorgio@gmail.com, anna@gmail.com with password "password" are Participant accounts you can try login to.

- Must register and log in (with a unique ID like email) to purchase tickets.

- Can view published performances by day and time, with filters (day, stage, genre).

- Can click on performances to see full details.

- Can buy only **one ticket type** per edition:

-  **Single Day Ticket** (valid for one day of choice)

-  **2-Day Pass** (valid for two consecutive days)

-  **Full Pass** (all three days)

- Maximum **200 participants per day**. Once reached, no more tickets can be sold for that day.

- After purchase, ticket details appear in the user’s profile.

### Organizers

- andrea@gmail.com, marco@gmail.com with password "password" are Organizer accounts you can try login to.

- Can create and edit performance details (as drafts).

- Cannot overlap performances on the same stage and time.

- Performances can be edited **only if unpublished**.

- Can view ticket sales stats per day.

- Can browse the public site but **cannot purchase tickets**.

- Only see their own unpublished performances, but all published ones.

  

###  Performance Details

- Artist/group name (unique per festival)

- Day and start time

- Duration (in minutes)

- Short description

- Stage (e.g., Main, Secondary, Experimental)

- Genre

- Promo images

- Published status (visible to all or only the organizer)

  

###  Homepage

- Shows a short list of published performances, sorted by day/time.

- Filters available (day, stage, genre).

## Technologies Used

  

- Python

- Flask

- Flask-Login

- SQLite

  

## How To Use

1. Download code from the repository 

2. Host with ```python3 src/app.py```

4. Open any browser at [http://localhost:5003](http://localhost:5003)
