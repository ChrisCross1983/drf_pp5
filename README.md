# Lucky Cat


### Here you can explore the [Live webpage]()

## Developer

| Name            | Linkedin                     | GitHub           |
| --------------- | ---------------------------- | ---------------- |
| Christian Borza | [Linkedin Profile](https://www.linkedin.com/in/borzachristian/) | [GitHub repositories](https://github.com/ChrisCross1983) |

## About


## Project Goals

### User Goals

-

### Business Owner Goals

-

## User Stories


## User Experience

### Target Audience

-

### User Requirements and Expectations

-

### Agile Methodologies

The project followed Agile principles using:

- GitHub Projects: Kanban board to track tasks and progress.
- User Stories: Each feature aligned with specific user or business needs.

![Kanban Board](-)

[Link to GitHub Project Board](-)

## Design

### Design Decisions



### Colors

Primary colors include:

-

### Color Scheme

The visual identity of Wild Watch is based on warm, natural tones that reflect wildlife and conservation.

| Hex Code  | Usage                | Description                                                      |
|-----------|----------------------|------------------------------------------------------------------|
| `#FFC857` | Primary / Navbar     | Main brand color for navigation and call-to-actions              |
| `#1A7F3C` | Success / Text Icons | Green tone used in helper labels and visual accents              |
| `#F4E4BC` | Section Background   | Soft beige background for content blocks                         |
| `#D67B4B` | CTA-Highlight        | Contrast color for emphasis in special sections                  |
| `#42C460` | Success Badge        | Used to indicate successful report interaction                   |
| `#F0B914` | Warning Badge        | Warning and pending status visuals                               |
| `#830814` | Danger Badge         | Error messages and rejected reports                              |
| `#49A9E9` | Info Badge           | Informational elements and icons                                 |
| `#333333` | Main Text Color      | Strong dark tone for body and headline text                      |
| `#F4F4F4` | Light BG Elements    | Light grey for containers and subtle background elements         |

> *Note:* Additional utility classes from Bootstrap (e.g., `.btn-success`, `.alert-danger`) were partially customized to reflect this color palette.

### Fonts

Typography was selected for readability and aesthetic harmony:

-

### Layout & Structure

The layout follows a structured, user-friendly approach:

-

Visual hierarchy was created through:

-

### Wireframes

Wireframes were created for desktop, tablet, and mobile views using Balsamiq to visualize the layout structure and user flow at an early project stage.  
>Please note: The final implemented UI may differ slightly from these drafts due to design iterations and responsive adjustments during development.


### Responsive Design

WildWatch is fully responsive and optimized for various screen sizes, from large desktops to tablets and smartphones. The application was developed using a mobile-first approach and adapts layout and content dynamically based on device resolution.

Key responsive elements include:

-

## Database Diagram

The application uses a relational database with key models:



## Key Features


## Future Improvements

-

## Technologies Used

### Languages

- Python 3
- HTML5
- CSS3
- JavaScript (ES6+)

### Libraries & Frameworks

-

### Django Packages

-

### Deployment & DevOps

- Heroku (Production Hosting)
- Gunicorn (WSGI HTTP server)
- GitHub (Version control and project board)

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

    **Before**:


    **After**:


- **CSS Validation**: Used the [W3C CSS Validator](https://jigsaw.w3.org/css-validator/) which returned the following results:


- **JavaScript Validation**: Used [JSHint](https://jshint.com/) to validate JavaScript code. The validation process returned a clean report compliant with ES6+ standards.

### Lighthouse scores

Lighthouse metrics were scored on Incognito Chrome



### Running Tests

Although automated tests (e.g., unit tests or integration tests) are considered best practice in professional development workflows, they were not implemented in this project. The project scope focused primarily on core functionality, UI/UX design, and manual end-to-end testing in line with the PP4 requirements.

### Manual Testing Overview

All major user flows were tested manually to ensure functional coverage, usability, and correct feedback behavior across devices and user roles. The tables below outline test scenarios, expected outcomes, and actual results.

---

<details>
<summary><strong>General User Functional Tests</strong></summary>

| Test Name                      | Steps                                                             | Expected Result                                                   | Actual Result       | Pass/Fail |
|-------------------------------|-------------------------------------------------------------------|-------------------------------------------------------------------|----------------------|-----------|
| Home Navigation               | Click "WildWatch" logo or Home link in navbar                     | User is redirected to homepage                                   | Same as expected     | ✓         |
| Signup Process                | Click Signup → Fill form → Submit                                 | Account created & verification email sent                        | Same as expected     | ✓         |
| Signup with invalid data      | Leave required fields empty → Submit                              | Inline error messages shown                                      | Same as expected     | ✓         |
| Signup with existing username | Fill form with already registered username → Submit               | Error message: "A user with that username already exists."        | Same as expected     | ✓         |
| Email Confirmation Flow       | Register → Click email verification link                          | Account gets activated                                           | Same as expected     | ✓         |
| Resend Verification Email     | Try login unverified → Click “Resend Email”                       | New confirmation email is sent                                  | Same as expected     | ✓         |
| Login (valid credentials)     | Enter correct credentials → Submit                                | User logs in successfully                                       | Same as expected     | ✓         |
| Login (wrong credentials)     | Enter wrong password → Submit                                     | Error message: "Invalid password."                               | Same as expected     | ✓         |
| Login (unverified user)       | Attempt login before email verification                           | Error: “Account not verified” message shown                      | Same as expected     | ✓         |
| Password Reset Flow           | Click “Forgot password” → Enter email → Receive link → Set new pw | Password reset completed successfully                            | Same as expected     | ✓         |
| View Profile                  | Navigate to Settings/Profile                                      | Profile details are displayed                                   | Same as expected     | ✓         |
| Edit Profile                  | Edit profile data → Submit                                        | Data updated, success message shown                             | Same as expected     | ✓         |
| Edit Email Address            | Change email → Submit                                             | User logged out → Verification email sent                        | Same as expected     | ✓         |
| Upload Profile Picture        | Upload image → Submit                                             | Image preview visible, saved to profile                         | Same as expected     | ✓         |
| Delete Account (cancel)       | Click Delete → Cancel confirmation popup                          | No action taken                                                  | Same as expected     | ✓         |
| Delete Account (confirmed)    | Click Delete → Confirm popup                                      | Account and data deleted                                        | Same as expected     | ✓         |
| Submit a Report               | Fill report form → Submit                                         | Report created and saved                                         | Same as expected     | ✓         |
| Edit Report                   | Open own report → Edit fields → Submit                            | Report updated, confirmation shown                              | Same as expected     | ✓         |
| Delete Report                 | Click Delete on own report → Confirm                              | Report deleted from system                                      | Same as expected     | ✓         |
| View All Reports Feed         | Click “Animal Reports Overview”                                   | Public reports displayed in list                                | Same as expected     | ✓         |
| Filter Reports (species/keyword) | Select species or enter keyword → Apply filter                  | Filtered reports displayed                                      | Same as expected     | ✓         |
| View Report Details           | Click “View Details” on report card                               | Full report detail shown                                        | Same as expected     | ✓         |
| Help on Report                | Click “I want to help” on report                                  | User added to helpers, button changes                           | Same as expected     | ✓         |
| Cancel Help                   | Click “I can no longer help”                                      | User removed from helpers                                       | Same as expected     | ✓         |
| Scroll-to-Top Button          | Scroll down → Click scroll arrow                                 | Page scrolls to top smoothly                                    | Same as expected     | ✓         |
| Responsive Mobile View        | Open site on mobile → FAB menu visible                           | Responsive behavior confirmed                                   | Same as expected     | ✓         |
| Navigation Menu               | Click through navbar items                                        | Pages load correctly                                             | Same as expected     | ✓         |
| Session Persistence           | Login → Navigate through site                                     | Session remains active                                           | Same as expected     | ✓         |
| Logout                        | Click Logout button                                               | User is logged out and redirected                               | Same as expected     | ✓         |

</details>
<br>

---

<details>
<summary><strong>Edge Cases & Negative Testing</strong></summary>

| Test Name                            | Steps                                                               | Expected Result                                               | Actual Result       | Pass/Fail |
|-------------------------------------|---------------------------------------------------------------------|---------------------------------------------------------------|----------------------|-----------|
| Upload invalid profile picture      | Try uploading non-image file (e.g. .pdf) as profile image → Submit | Error: "Upload a valid image."                                | Same as expected     | ✓         |
| Submit Report – Missing Fields      | Leave required report fields empty → Submit                        | Inline validation errors shown                                | Same as expected     | ✓         |
| Submit Report with large image      | Upload very high-res image → Submit                                 | Image saved successfully, scaled in display                   | Same as expected     | ✓         |
| Edit Report Image                   | Edit existing report → Upload new image → Submit                   | New image replaces previous one                               | Same as expected     | ✓         |
| Attempt edit by another user        | Login as another user → Access another user's edit URL             | Redirect or access denied                                     | Same as expected     | ✓         |
| Attempt delete by another user      | Login as another user → Access delete URL of other's report        | Redirect or access denied                                     | Same as expected     | ✓         |
| Filter Reports – no match           | Enter a rare/invalid keyword → Submit                              | Message shown: "No reports found matching your criteria"      | Same as expected     | ✓         |
| Try to help on own report           | Open own report detail page                                        | "Help" button is not visible                                  | Same as expected     | ✓         |
| Attempt double-helping              | Click “I want to help” multiple times rapidly                      | Only one helper entry added, button becomes disabled          | Same as expected     | ✓         |
| Admin – Reject Report with Comment  | Admin logs in → Rejects report → Adds rejection comment            | Status set to "Rejected", comment visible for user            | Same as expected     | ✓         |
| Admin – Approve Report              | Admin logs in → Approves report                                    | Status set to "Approved"                                      | Same as expected     | ✓         |

</details>
<br>

## Bugs

### Known Issues

-

### Resolved Issues

-

> All reported issues were tracked and resolved via GitHub commit references.

## Deployment

### Clone & Local Setup

To run the project locally:

1. Open your terminal (e.g., Git Bash, Command Prompt, Terminal).
2. Clone the repository:

    - git clone https://github.com/ChrisCross1983/pp4-wildwatch.git
    - cd pp4-wildwatch

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

![Environment Message](assets/env_message.png)

> Example of how environment variables are loaded in `settings.py`:

![Setting Message](assets/settings_message.png)

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

- [WebAIM](https://webaim.org/) – Contrast Checker (Accessibility Testing)
- [TinyPNG](https://tinypng.com/) – Image Compression
- [Icons8](https://icons8.com/) – Favicon and UI icon sets
- [Font Awesome](https://fontawesome.com/) – Icon integration
- [Unsplash](https://unsplash.com/) – Free wildlife placeholder images
- [Balsamiq](https://balsamiq.com/) – Wireframe design

### Additional Resources & Support

Throughout the development process, various tools and platforms were consulted to support error resolution, refresh knowledge, and ensure efficient troubleshooting:

- [chatgpt](https://chatgpt.com) - Used as a support tool for resolving technical issues and validating code logic.
- [StackOverflow](https://stackoverflow.com) - Community-driven platform for researching specific error messages and best practices.
- [YouTube](https://youtube.com) - Reference for tutorial content and visual explanations to reinforce concepts and workflows.

### Media

-

## Acknowledgements

I would like to thank those who were a great support and inspiration during writing this project:

- My wife, who supported me during the process of creating this project.