# MLE Case Studies - Datasets

This directory contains datasets that can be used for Machine Learning Engineer case studies. These datasets simulate a platform where users engage in discussions with each other and have conversations with StoryBot.

## Overview

The datasets include:

1. **Conversations** - One-on-one conversations between users and an AI agent (StoryBot)
2. **Discussions** - Forum-like discussions with posts and comments from multiple users
3. **Activity** - Record of user activities related to discussions: reading, commenting on, and creating posts.

## Data Files

### conversations.json

Contains conversations between individual users and StoryBot. Each conversation includes:

- `messages_list`: List of messages in the conversation
- `ref_conversation_id`: Unique identifier for the conversation
- `ref_user_id`: ID of the user participating in the conversation

Example structure:

```json
{
  "messages_list": [
    {"message": "Good morning! How are you feeling today?",
    "ref_conversation_id": 42615,
    "ref_user_id": 1,
    "transaction_datetime_utc":  "2023-10-01T08:00:00Z",
    "screen_name": "StoryBot"
    },
    {"message": "I'm doing well, thanks for asking! Just trying to get through the day.",
    "ref_conversation_id": 42615,
    "ref_user_id": 822,
    "transaction_datetime_utc":  "2023-10-01T08:01:00Z",
    "screen_name": "User822"
    },
    {"message": "That's great to hear! Is there anything specific on your mind?",
    "ref_conversation_id": 42615,
    "ref_user_id": 1,
    "transaction_datetime_utc":  "2023-10-01T08:02:00Z",
    "screen_name": "StoryBot"
    },
  ],
  "ref_conversation_id": 42615,
  "ref_user_id": 822
}
```

### discussions.json

Contains discussion threads with posts and comments. Each discussion includes:

- `post_id`: Unique identifier for the post
- `messages_list`: List of messages (both the initial post and comments)

Example structure:

```json
{
  "post_id": 3830,
  "messages_list": [
    {
      "post_id": 3830,
      "comment_id": null,
      "text": "Initial post content",
      "author_ref_user_id": 10,
      "reported_or_removed": false,
    },
    {
      "post_id": 3830,
      "comment_id": 1,
      "text": "Comment on the post",
      "author_ref_user_id": 45,
      "reported_or_removed": false,
    }
  ]
}
```

### activity.json

Contains user activities related to discussions. Each activity entry includes:

- `ref_user_id`: ID of the user who performed the activity
- `activity_type`: Type of activity ("read", "commented", or "created")
- `post_id`: ID of the post related to the activity

Example structure:

```json
{
  "ref_user_id": 10,
  "activity_type": "created",
  "post_id": 3830
}
```
## Notes on Data Generation

- The data is synthetically generated to simulate realistic user behavior
- Timestamps and some metadata might be simplified or omitted for clarity
- The current dataset size is limited for demonstration purposes
