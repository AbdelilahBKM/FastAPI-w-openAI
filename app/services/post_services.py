import json

import httpx
import os
from dotenv import load_dotenv
from app.CRUD.joining_crud import get_random_user_by_discussion_id
from app.CRUD.post_crud import create_answer_to_db, create_question_to_db
from app.CRUD.discussion_crud import get_discussion_by_id
from app.services.openai_api import generate_discussion_question

load_dotenv()
DOT_NET_API = os.getenv("ASPNET_API_URL")


async def populate_discussion_with_posts(discussion_id: int, nbr_posts: int, db):
    discussion = get_discussion_by_id(discussion_id, db)
    if discussion is None:
        raise ValueError("Discussion not found")
    for i in range(nbr_posts):
        print("Creating post number", i + 1)
        owner = await get_random_user_by_discussion_id(discussion_id, db)
        if owner is None:
            raise ValueError("No user found for the discussion")
        question = await generate_discussion_question(discussion.d_Name)
        if question is None:
            raise ValueError("Failed to generate question")
        async with httpx.AsyncClient() as client:
            question_json = {
              "title": question["title"],
              "content": question["content"],
              "postedBy": owner.id,
              "discussionId": discussion.id,
              "postType": 0
            }
            response = await client.post(
                f"{DOT_NET_API}/Post/Question",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {owner.token}"
                },
                data=question_json
            )
            if response.status_code == 200:
                create_question_to_db(question_json, db)
            else:
                raise ValueError(f"Failed to create question: {response.text}")