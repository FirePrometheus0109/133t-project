def delete_default_letter_template_for_event(company, event_type):
    if event_type:
        (company.letter_templates
                .filter(event_type=event_type)
                .update(event_type=None))
