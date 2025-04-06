from typing import List

import httpx
import os
import random
from dotenv import load_dotenv
from app.CRUD.joining_crud import get_random_user_by_discussion_id
from app.CRUD.post_crud import create_question_to_db, get_questions_by_discussion_id, create_answer_to_db
from app.CRUD.discussion_crud import get_discussion_by_id, get_local_discussions
from app.models import Post
from app.services.openai_api import generate_discussion_question, generate_answer_to_question

load_dotenv()
DOT_NET_API = os.getenv("ASPNET_API_URL")


async def populate_discussion_with_posts(discussion, db) -> list[Post] | None:
    questions = []
    if discussion is None:
        raise ValueError("Discussion not found")
    for i in range(random.randint(5, 16)):
        print("Creating post number", i + 1)
        owner = get_random_user_by_discussion_id(discussion.id, db)
        if owner is None:
            raise ValueError("No user found for the discussion")
        question = await generate_discussion_question(discussion.d_Name)
        if question is None:
            raise ValueError("Failed to generate question")
        async with httpx.AsyncClient(verify=False) as client:
            question_json = {
              "title": question["title"],
              "content": question["content"],
              "postedBy": str(owner.id),
              "discussionId": discussion.id,
              "postType": 0
            }
            response = await client.post(
                f"{DOT_NET_API}/Post",
                headers={
                    "Content-Type": "application/json"
                },
                json=question_json
            )
            if response.status_code in (200, 201):
                response_json = response.json()
                question_json["id"] = response_json["id"]
            else:
                raise ValueError(f"Failed to create question: {response.text}")
        question = create_question_to_db(question_json, db)
        questions.append(question)
    return questions

##########################################################################################
#################### Main function to populate all discussions with posts ################
async def populate_all_discussions_with_posts(db) -> List[dict] | None:
    discussions = get_local_discussions(db)
    list_of_questions = []
    if discussions is None:
        raise ValueError("No discussions found")
    for discussion in discussions:
        print("Creating posts for discussion:", discussion.d_Name)
        questions = await populate_discussion_with_posts(discussion, db)
        list_of_questions.append({
            "discussion": discussion.d_Name,
            "questions": questions
        })
        if questions is None:
            raise ValueError("Failed to create questions")
    return list_of_questions
############################################################################################


async def populate_discussion_with_answers(discussion_id: int, db) -> None:
    discussion = get_discussion_by_id(discussion_id, db)
    answers = []
    if discussion is None:
        raise ValueError("Discussion not found")
    questions = get_questions_by_discussion_id(discussion_id=discussion_id, db=db)
    for question in questions:
        for i in range(random.randint(2, 10)):
            print("Creating post number", i + 1)
            owner = get_random_user_by_discussion_id(discussion_id, db)
            if owner is None:
                raise ValueError("No user found for the discussion")
            answer = await generate_answer_to_question({
                "title": question.title,
                "content": question.content
            })
            if answer is None:
                raise ValueError("Failed to generate answer")
            async with httpx.AsyncClient() as client:
                answer_json = {
                  "title": "answer to question: " + question.title,
                  "content": answer,
                  "postedBy": owner.id,
                  "questionId": question.id,
                  "postType": 1
                }
                response = await client.post(
                    f"{DOT_NET_API}/Post",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {owner.token}"
                    },
                    data=answer_json
                )
                if response.status_code == 200:
                    answer = create_answer_to_db(answer_json, db)
                    answers.append(answer)
                else:
                    raise ValueError(f"Failed to create answer: {response.text}")