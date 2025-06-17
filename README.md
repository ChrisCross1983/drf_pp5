# LUCKY CAT

Lucky Cat is a platform where cat owners and cat lovers can connect. Whether you're looking for someone to take care of your cat while you're away, or you're happy to help others by cat-sitting, Lucky Cat makes it easy to post and respond to requests.
<br>
On the site, users can reate posts to find a cat sitter or offer cat-sitting services or browse through local requests and offers.<br>
It's simple, user-friendly, and all about helping each other take care of our feline friends.

Link to the live site: [Lucky Cat](https://chriscross1983.github.io/react_pp5/)

## Table of Contents

1. [Developer](#developer)  
2. [Project Goals](#project-goals)  
3. [UX](#ux)  
    - [Target Audience](#target-audience)  
    - [User Goals](#user-goals)  
4. [User Stories](#user-stories)  
5. [Design](#design)  
    - [Decisions](#design-decisions)  
    - [Colors](#colors)  
    - [Typography](#typography)  
    - [Layout & Structure](#layout--structure)  
    - [Wireframes](#wireframes)  
6. [Features](#features)
    - [Posting and Requesting](#posting-and-requesting)
    - [Profiles](#profiles)
    - [Following](#following)
    - [Commenting](#commenting)
    - [Liking](#liking)
7. [Future Improvements](#future-improvements)  
8. [Technologies & Libraries](#technologies--libraries)
    - [Technologies used](#technologies-used)
        - [HTML](#html)
        - [CSS](#css)
        - [JavaScript](#javascript)
        - [JSX](#jsx)
        - [Python](#python)
        - [Django REST Framework (DRF)](#django-rest-framework-drf)
    - [Libraries used](#libraries-used)
        - [dj-rest-auth](#dj-rest-auth)
        - [rest_framework_simplejwt](#rest_framework_simplejwt)
        - [django-allauth](#django-allauth)
        - [Cloudinary](#cloudinary)
        - [Django REST Framework (rest_framework)](#django-rest-framework-rest_framework)
9. [Testing](#testing)
10. [Bugs](#bugs)
11. [Deployment](#deployment)  
12. [Credits](#credits)
    - [Coolors](#coolors)
    - [GetEmoji](#getemoji)
    - [Visual Studio Code](#visual-studio-code)

---

## Developer

| Name | LinkedIn | GitHub |
|-----|----------|-------|
| Christian Borza | [LinkedIn Profile](https://www.linkedin.com/in/borzachristian/) | [GitHub Repositories](https://github.com/ChrisCross1983) |

---

## Project Goals

The primary goal of this project is to create a user-friendly and trustworthy space for exchanging cat-sitting offers and requests. It aims to simplify the process of finding suitable matches based on location, availability, and experience. The platform also seeks to promote responsible pet care by making it easier for owners to find dependable help and for sitters to share their services with others in the community.

---

## UX

### Target Audience

The platform is intended for individuals who own cats and are in need of temporary or occasional care, as well as those who enjoy looking after cats and are willing to offer their time and experience. This includes pet owners planning holidays, people with busy schedules, students or retirees seeking part-time opportunities, and anyone with a genuine interest in animal care. The age is mostly irrelevant.

### User Goals

Users of the website should be able to:

- Post requests or offers with clear details
- Contact others through a secure and straightforward messaging system
- View profiles and past activity to make informed decisions
- Manage own posts and interactions with minimal effort

---

## User Stories

1. User Story: User Registration

As a new user, I can register for an account so that I can access features like posting, commenting, and interacting with other users.

Acceptance Criteria:

Users can register with a unique username and email.
Password must meet basic security criteria (e.g., minimum 8 characters).
Users receive a confirmation email upon registration.

2. User Story: User Login

As a registered user, I can log into my account so that I can access personalized features and manage my activity.

Acceptance Criteria:

Users can log in with their username and password.
Incorrect login attempts display an appropriate error message.
Token-based authentication is used to secure sessions.

3. User Story: Password Reset

As a user, I can reset my password so that I can regain access to my account if I forget my password.

Acceptance Criteria:

Users can request a password reset link via email.
Password reset functionality includes token validation and password change form.

4. User Story: Profile Overview

As a user, I can view my profile so that I can see a summary of my activity, including posts, followers, and followings.

Acceptance Criteria:

Profiles display total posts, followers, and followings.
Users can see their recent posts on their profile.

5. User Story: Edit Profile

As a user, I can edit my profile details so that I can update my username, profile picture, or other personal information.

Acceptance Criteria:

Users can upload a profile picture using Cloudinary.
Profile editing options include username, bio, and picture.

6. User Story: Change Password

As a user, I can change my password so that I can enhance the security of my account.

Acceptance Criteria:

Users can change their password from the profile settings menu.
Users must confirm their current password before setting a new one.

7. User Story: Create Post

As a user, I can create a post so that I can share my cat-sitting needs, services, or general tips with the community.

Acceptance Criteria:

Posts must include a title, category, description, and optional image.
Categories include "Offer Sitting," "Search Sitting," and "General."
Posts are displayed on the feed after submission.

8. User Story: View Feed

As a user, I can view all posts in an infinite scrolling feed so that I can explore the community's activities and posts.

Acceptance Criteria:

The feed supports infinite scrolling to dynamically load more posts.
Posts display the title, category, image, and number of likes/comments.

9. User Story: Interact with Posts

As a user, I can like, unlike, and comment on posts so that I can engage with the community and show appreciation for posts.

Acceptance Criteria:

Users can like and unlike posts with a single click.
Users can leave comments on posts, which are displayed below each post.

10. User Story: Search and Filter Posts

As a user, I can search and filter posts by category so that I can find relevant content quickly.

Acceptance Criteria:

A search bar allows users to search by keyword.
Filters include "Offer Sitting," "Search Sitting," and "General."

11. User Story: Edit/Delete Post

As a user, I can edit or delete my posts so that I can update or remove content I no longer want to share.

Acceptance Criteria:

Users can edit the title, category, description, and image of their posts.
Users can delete their posts, which are removed from the feed.

12. User Story: Edit/Delete Comments

As a user, I can edit or delete my comments so that I can correct or remove comments I have made.

Acceptance Criteria:

Users can edit the content of their comments.
Users can delete their comments, which are removed from the post.

13. User Story: Follow Users

As a user, I can follow other users so that I can stay updated with their posts.

Acceptance Criteria:

Users can follow/unfollow other users with a single click.
Followers and followings are displayed on the profile page.

14. User Story: Dashboard Insights

As a user, I can view and interact with a list of recent notifications in my dashboard so that I can quickly react to relevant activities and stay up to date.

Acceptance Criteria:

Users see a scrollable list of recent notifications in the dashboard sidebar.
Unread notifications are visually highlighted (e.g. background color, red badge).
Each notification shows a type (e.g. like, comment, follow, sitting request, sitting message) and a timestamp.
Clicking a notification redirects the user to the corresponding detail page (e.g. post, comment, chat).
Users can mark individual notifications as read (automatically on click).
Users can mark all notifications as read via a dedicated button.
If a referenced post or request no longer exists, the user receives a toast notification.

15. User Story: Create Sitting Request

As a user, I can send a sitting request to post owners so that I can arrange cat-sitting services directly.

Acceptance Criteria:

Posts include a "Request Sitting" button.
Clicking the button sends a private message to the post owner.

16. User Story: Manage Sitting Requests

As a user, I can view and manage all my sitting requests so that I can track ongoing and past requests.

Acceptance Criteria:

A dashboard shows incoming sitting requests and responses.

17. User Story: Receive Notifications

As a user, I can receive notifications for new comments, likes, and sitting requests so that I stay updated on interactions with my posts.

Acceptance Criteria:

Notifications appear as a dropdown or a separate section.
Notifications include a timestamp and a link to the relevant activity.

---

## Design

### Design Decisions

The design of the platform follows a clean, blog-like structure with content centered on the page. This layout was chosen for several reasons:

- Centered Layout: It draws attention to the content and improves readability across different screen sizes.
- Blog-Style Format: Posts resemble short blog entries, which encourages detailed and thoughtful descriptions.
- Comment Section in Posts: Inspired by blogging platforms, this feature promotes open and visible discussion, helping users get quick answers and engage with each other directly.

The design focuses on simplicity and clarity to ensure a smooth experience for users regardless of their technical background.

### Colors

The chosen color palette combines clarity, accessibility, and modern aesthetics.

- #212529 (dark gray) provides a strong, neutral color that ensures high contrast and readability without the harshness of pure black.
- #FFFFFF (white) serves as the primary background and text color for light sections, creating a clean, minimal look that emphasizes content.
- #198754 (green) is used to highlight positive actions or success states. It offers a calm yet noticeable contrast, guiding user attention without overwhelming the interface.
- #0D6EFD (blue) is used for primary buttons and interactive elements. It reflects trust and professionalism while standing out clearly against both light and dark backgrounds.

This color combination follows common accessibility standards and creates a visually balanced, user-friendly experience.

![Picture of the color palette](assets\readme\palette.jpg)

### Typography

To ensure wide compatibility and a consistent look across operating systems and devices, the platform uses a modern system font stack.
This combination prioritizes performance and readability, while maintaining a familiar appearance for users on macOS, Windows, Linux, Android, and iOS.

### Layout & Structure
The layout follows a structured, user-friendly approach:

- Card-based blog design for displaying posts in a clear and organized format
- Website-wide navigation bar to ensure consistent access to main features
- Interactivity for neccessary parts of the application (Commenting, messaging, liking, ...)
- Mobile-first responsiveness ensures accessibility on all screen sizes
- Visual hierarchy was created through:
    - Consistent button styles (primary, danger, success, etc.) to guide user actions
    - Badges and alert styles to highlight report status and feedback
    - Rounded elements (cards, buttons, images) for a soft and friendly visual appeal

### Wireframes

<details>
<summary>Click to expand the wireframe view</summary>

### Start page (Desktop)

![Wireframe](assets\readme\start_desktop.jpg)

### Start page (Mobile)

![Wireframe](assets\readme\start_mobile.jpg)

---

### Profile page (Desktop)

![Wireframe](assets\readme\profile_desktop.jpg)

### Profile page (Mobile)

![Wireframe](assets\readme\profile_mobile.jpg)

---

### Post page (Desktop)

![Wireframe](assets\readme\post_desktop.jpg)

### Post page (Mobile)

![Wireframe](assets\readme\post_mobile.jpg)

---

### Requests page (Desktop)

![Wireframe](assets\readme\requests_desktop.jpg)

### Requests page (Mobile)

![Wireframe](assets\readme\requests_mobile.jpg)

</details>

## Database Diagram

The application uses a relational database with the following key models and relationships:

- **User**  
  Stores authentication identity of each user.

- **Profile**  
  Extends the `User` with additional profile information such as:
  - Bio
  - Profile picture
  - Follower relationships

- **Post**  
  Represents a public user post. Includes:
  - Title, description, image, category
  - Author (linked to `User`)
  - Like count (aggregated)

- **Comment**  
  Represents user comments on posts. Supports:
  - Nested replies via `parent`
  - Likes per comment
  - Editing and deletion

- **Like**  
  Tracks which user liked which post.

- **Follower**  
  Captures follower relationships between users:
  - `owner` follows `followed`

- **Notification**  
  Used for alerting users of events (e.g., likes, comments, sitting requests). Includes:
  - Type of notification
  - Read/unread state
  - Linked entities like `post`, `comment`, `sitting_request`

- **Sitting Request**  
  Represents a care or hosting request:
  - Between `sender` and `receiver`
  - Refers to a `post` and includes a message & status

- **Sitting Response Message**  
  Enables message exchange related to a `Sitting Request`:
  - Linked to a `sitting_request`
  - Contains message content and sender

![Entity Relationship Diagram of Wild Watch](assets\readme\database_pp5.jpg)

## Features

The website includes several key features aimed at creating an engaging and easy-to-use experience:

### Posting and Requesting

Post Offers and Requests: Users can create detailed listings to either request cat-sitting services or offer them. Each post should include descriptions, availability, and location information.

![Screenshot of the feature](assets\readme\post.jpg)

### Profiles

Visit Profiles: Every user has a profile where their listings, interactions, and basic information are visible. This helps build trust and allows others to learn more about who they are interacting with.

![Screenshot of the feature](assets\readme\profile.jpg)

### Following

Users can follow others to stay updated on new posts or changes. This is especially helpful for those who frequently look for or offer services in specific areas.

![Screenshot of the feature](assets\readme\following.jpg)

### Commenting

Comment on posts: Listings include a comment section where users can ask questions, provide feedback, or start conversations directly under a post.

![Screenshot of the feature](assets\readme\commenting.jpg)

### Liking

Like Posts: Posts can be liked to show appreciation, increase visibility, or bookmark them for later reference.

![Screenshot of the feature](assets\readme\liking.jpg)

### Instant Messaging

People can connect via instant messaging to share their information and plan meetings.

![Screenshot of the feature](assets\readme\messaging.jpg)

---

## Future Improvements

While the platform offers essential functionality, several enhancements are planned for future development:

- Review and Rating System: Allowing users to leave feedback on their experiences with sitters or owners
- Calendar Integration: To help users manage availability and scheduling more efficiently

## TECHNOLOGIES & LIBRARIES

### Technologies used

#### HTML
The backbone of the website’s structure. HTML defines the content and layout of each page using semantic tags and elements.

#### CSS
Used for styling and layout. CSS makes the site visually appealing by handling colors, spacing, fonts, and responsive design.

#### JavaScript
Adds interactivity to the front end. JavaScript handles dynamic behavior like form validation, animations, and user interactions.

#### JSX
A syntax extension for JavaScript, mainly used with React. It allows you to write HTML-like code directly inside JavaScript, making component structure more intuitive.

#### Python
Powers the server-side logic of the application. Python handles data processing, request handling, and communication with the database.

#### Django REST Framework (DRF)
A powerful toolkit for building Web APIs in Django. DRF simplifies serialization, authentication, and permissions for backend development.

### Libraries Used

#### dj-rest-auth
Provides a set of REST API endpoints for user authentication and registration, making it easier to integrate login and signup features.

#### rest_framework_simplejwt
Adds JSON Web Token (JWT) authentication support to Django REST Framework, allowing for secure, stateless user sessions.

#### django-allauth
A complete authentication solution for Django. It supports both local and social account authentication and integrates well with dj-rest-auth.

#### Cloudinary
A cloud-based media management service used for uploading, storing, and delivering images and videos efficiently.

#### Django REST Framework (rest_framework)
The core framework that enables the creation of flexible and robust RESTful APIs in Django. It handles things like routing, request parsing, and response rendering.

## Testing

### Accessibility

- The platform adheres to **WCAG 2.1 AA guidelines**
- ARIA labels and roles are implemented for screen reader compatibility
- Contrast levels tested with WebAIM contrast checker

### Performance Optimization

- Optimized static file handling via Django Whitenoise
- Lazy loading of images and media
- Minified CSS and compressed assets
- Lighthouse audits conducted across all key user flows

### Device & Browser Compatibility

- **Devices tested:**
  - Desktop: Windows, macOS
  - Mobile: Android, iOS

- **Browsers tested:**

  - Google Chrome (desktop/mobile)
  - Mozilla Firefox
  - Microsoft Edge

### Automated Testing

- **HTML Validation**: Used the [W3C HTML Validator](https://validator.w3.org/) which returned the following results:

    ![HTML Validator Results](assets\readme\w3_validation_pp5.jpg)

- **CSS Validation**: Used the [W3C CSS Validator](https://jigsaw.w3.org/css-validator/) which returned the following results:

    ![CSS Validator Results](assets\readme\w3_css_pp5.jpg)

- **JavaScript Validation**: Used [JSHint](https://jshint.com/) to validate JavaScript code. The validation process returned a clean report compliant with ES6+ standards.

### Lighthouse scores

Lighthouse metrics were scored on Incognito Chrome

![Lighthouse Test - Home Page](assets/)

![Lighthouse Test - Login Page](assets/)

![Lighthouse Test - Create Report Page](assets/)

![Lighthouse Test - Animal Report Overview Page](assets/)

![Lighthouse Test - My Reports Page](assets/)

![Lighthouse Test - Profile Page](assets/)

### Running Tests

Although automated tests (e.g., unit tests or integration tests) are considered best practice in professional development workflows, they were not implemented in this project. The project scope focused primarily on core functionality, UI/UX design, and manual end-to-end testing in line with the PP4 requirements.

A list of manual tests can be found [here](TESTING.md).

## Bugs

There are currently no known bugs.

## Deployment

### Clone & Local Setup

To run the project locally:

1. Open your terminal (e.g., Git Bash, Command Prompt, Terminal).
2. Clone the repository:

    - git clone https://github.com/ChrisCross1983/drf_pp5.git
    - cd drf_pp5

3. Create and activate a virtual environment:

On macOS/Linux:

    - python -m venv .venv
    - source .venv/bin/activate

On Windows:

    - python -m venv .venv
    - .venv\Scripts\activate

4. Install all required packages:

    - pip install -r requirements.txt

5. Create a .env file in the project root and add the following variables:

![Environment Message](assets\readme\env_message_pp5.png)

> Example of how environment variables are loaded in `settings.py`:

![Setting Message](assets\readme\settings_message_pp5.png)

6. Run the server locally:

    - python manage.py makemigrations
    - python manage.py migrate
    - python manage.py runserver

### Deployment via Heroku

1. Navigate to [heroku](https://www.heroku.com/home) and create an account.
2. Click `Create new app`, enter the app name and choose your region, hit `create app`.
3. Click **Deploy** and in the _Deployment method_ option choose **Github**. Enter the repository's name and click connect, you can leave the branch deployment to `main`.
   > You need to have created your github repository.
4. Head to **Settings** and click `Reveal config vars`
5. On the KEY inputs add: DATABASE_URL - SECRET_KEY - CLOUDINARY_URL - DEBUG. On the VALUE inputs add your own, for each one.
6. Click **Add buildpack** and choose `python`.
7. Now you're set. Go back to `Deploy` and click **Deploy branch**.

Heroku will install packages, apply migrations and launch the app.

### Forking the Project

Forking a repository is commonly done to contribute to another developer's project or to use it as the foundation for your own. To fork a repository:

1. Click the **Fork** button at the top right of the repository page.
2. This creates a separate copy in your own account for further modification or contribution.

## Credits

### [Coolors](https://coolors.co/)
Used to create the color palette.

### [GetEmoji](https://getemoji.com/)
Used for emojis in the application.

### [Visual Studio Code](https://code.visualstudio.com/)
Used to edit the code for the application.

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX