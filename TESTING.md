# Testing for Lucky Cat

### Frontpage

| Testing method | Expected Result | Result |
|-----|----------|-------|
| Visiting the starting page as a logged-out user | The login prompt should appear | Pass |
| Visiting the starting page as a logged-in user | The posts should appear | Pass |
| Clicking on the login link | The login form should appear | Pass |

### Login

| Testing method | Expected Result | Result |
|-----|----------|-------|
| Trying to login without a username | A warning should appear, indicating that the field is not filled | Pass |
| Trying to login without a password | A warning should appear, indicating that the field is not filled | Pass |
| Logging in with false credentials | "Invalid username or password. Please try again." should be displayed | Pass |
| Logging in with right credentials | The user should be logged in and redirected to the posts page | Pass |
| Visiting the login page as a logged-in user | The user should be redirected and the posts page should appear | Pass |

### Register

| Testing method | Expected Result | Result |
|-----|----------|-------|
| Trying to register without first name | A warning should appear that the field is required | Pass |
| Trying to register without last name | A warning should appear that the field is required | Pass |
| Trying to register without username | A warning should appear that the field is required | Pass |
| Trying to register without password | A warning should appear that the field is required | Pass |
| Trying to register without password 2 | A warning should appear that the field is required | Pass |
| Trying to register without matching passwords | A warning should appear that the passwords do not match | Pass |
| Trying to register with a password that is less than 8 characters long | A warning should appear that the password is too short | Pass |
| Trying to register with an already taken username | A warning should appear that the user is already registered | Pass |
| Trying to register with an already taken email address | A warning should appear that the email address is already used | Pass |
| Trying to register with valid credentials | A user should be created and a confirmation email should be sent | Pass |
| Visiting the register page as a logged-in user | The user should be redirected and the posts page should appear | Pass |

### Posts

| Testing method | Expected Result | Result |
|-----|----------|-------|
| Trying to create a post without a title | A warning message should appear that the field is requried | Pass |
| Trying to create a post without a description | A warning message should appear that the field is requried | Pass |
| Trying to create a post without a category | The general category should be used as a fallback | Pass |
| Trying to create a post with valid data | The post should be created and the user should be redirected to the posts page | Pass |
| Using offer as the category | The post should be listed as an offer and users should be able to request the offer | Pass |
| Using request as the category | The post should be listed as a request and users should be able to make offers | Pass |
| Accessing owned post | No offer or request should be possible | Pass |
| Accessing owned post | A dropdown window with the possibility to edit or delete the post should appear | Pass |
| Clicking on edit post | A modal window should appear that contains the information | Pass |
| Trying to edit a post without title or description | A warning should appear that the fields are required | Pass |
| Trying to edit a post without a category | The default category should be chosen | Pass |
| Trying to edit a title with more than 255 characters | A warning should appear to tell about the character limit | Pass |
| Trying to delete a post | A modal window should appear that the post will be deleted once the user clicks on delete | Pass |
| Confirming the deletion | The post should be deleted | Pass |
| Clicking outside of the modal, using the X button or clicking on cancel | The modal should disappear | Pass |
| Clicking on the heart icon | A like should be given to the post and the number should change accordingly | Pass |
| Scrolling down until no more posts are visible | New posts should be fetched if there are any | Pass |

### Comments

| Testing method | Expected Result | Result |
|-----|----------|-------|
|Submitting a valid comment | The comment appears at the top of the comment list | Pass |
| Submitting a comment with only whitespace | No comment is created, submit button remains disabled | Pass |
| Replying to a comment | The reply appears under the parent comment | Pass |
| Liking a comment | Like count increases, button changes to active state | Pass |
| Unliking a comment | Like count decreases, button resets to inactive | Pass |
| Editing own comment | Edited comment is updated inline and saved | Pass |
| Deleting own comment | Comment disappears, toast confirms deletion | Pass |
| Deleting a reply | Reply disappears from the comment thread | Pass |
| Clicking "Load more comments" | Next page of comments is appended to the list | Pass |
| Visiting post with comment ID in URL | The referenced comment is auto-scrolled and highlighted | Pass |

### Notifications

| Testing method | Expected Result | Result |
|-----|----------|-------|
| Making an offer for an open request | A message window should appear | Pass |
| Sending the message | The offer should be directed to the post's owner | Pass |
| Making a request for an open offer | A message window should appear | Pass |
| Sending the message | The request should be directed to the post's owner | Pass |
| Accessing the account that has notifications | Notification messages should be highlighted in the menu | Pass |
| Receiving a request, offer or message | It should be labelled accordingly | Pass |

### Messaging

| Testing method | Expected Result | Result |
|-----|----------|-------|
| Sending a message | The most recent message should appear in the chat on the top | Pass |
| Bein the sender of a message | A dropdown menu icon to edit and delete the message should appear | Pass |
| Editing a message with no content | A warning should appear to inform the user that the message cannot be empty | Pass |
| Editing a message with content | The content should change | Pass |
| Clicking on delete | A modal should appear to warn about the deletion | Pass |
| Confirm the deletion | The message should disappear | Pass |
| Receiving a message | The message should be displayed | Pass |
| Clicking on a chat | The chat with that person should appear | Pass |

### Profiles

| Testing method | Expected Result | Result |
|-----|----------|-------|
| Sending a follow request | A request should be sent to the according user | Pass |
| Checking the follow requests tab | The request should appear in the tab | Pass |
| Clicking on allow | The request should be accepted and the count should increase | Pass |
| Clicking on decline | The request should be denied | Pass |
| Clicking on the followers tab | The followers should be displayed | Pass |
| Clicking on the posts tab | The posts the user made should be displayed | Pass |
| Clicking on the following tab | The people the user follows should be displayed | Pass |
| Clicking on the follow requests tab | The incoming and sent requests should be displayed | Pass |
| Clicking on the activity tab | The last actions should be displayed | Pass |
| Clicking on an activity | The corresponding page should open up | Pass |

### Responsiveness

| Testing method | Expected Result | Result |
|-----|----------|-------|
| Resizing the browser window on the posts page | The notifications and requests windows should disappear | Pass |
| Resizing the browser window on the profile page | The information and dropdown menus should float into the next row | Pass |