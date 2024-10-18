from survey import models


def create_one_question(**kwargs):
    return models.Question.objects.create(**kwargs)


def create_questions(data, company):
    for i in data:
        if i.pop('add_to_saved_questions', False):
            i['company'] = company
    questions = []
    # NOTE (i.bogretsov) bulk_create does not work with M2M relations
    for i in data:
        q = create_one_question(**i)
        questions.append(q)
    return questions


def create_survey(data, company):
    return models.Survey.objects.create(**data, company=company)


def add_questions_to_survey(survey, questions):
    survey.questions.add(*questions)
    survey.save()


def create_answers_values(data):
    """Creating answers values.
        In current version it is possible to create only 'Yes/No' answers.
    """
    answers = []
    # NOTE (i.bogretsov) bulk_create does not work
    for i in data:
        answer = models.Answer.objects.create(**i)
        answer.save()
        answers.append(answer)
    return answers


def delete_existing_answers_values(job_seeker_answers):
    models.Answer.objects.filter(
        job_seeker_answers__in=job_seeker_answers).delete()
    job_seeker_answers.delete()


def create_answers(job, data, job_seeker, existing_answers):
    """Create answers.
    First create ansewrs values.
    Second create job seeker answers.
    """
    delete_existing_answers_values(existing_answers)
    answers_data = [i['answer'] for i in data]
    questions = [i['question'] for i in data]

    answers = create_answers_values(answers_data)

    for answer, el in zip(answers, data):
        el['answer'] = answer
        el['owner'] = job_seeker
        el['job'] = job

    (models.AnswerJobSeeker
           .objects
           .bulk_create(models.AnswerJobSeeker(**i) for i in data))

    # NOTE (i.bogretsov): it is impossible to return result
    # of 'bulk_create' function because created answers don't have ids.
    # instead of this code does one request to db for getting created answers
    # and return this result.
    js_answers = models.AnswerJobSeeker.objects.filter(
        job=job,
        owner=job_seeker,
        question__in=questions)
    return js_answers
