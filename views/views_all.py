add_project_view={
            "type": "modal",
            "callback_id": "project_form",
            "title": {"type": "plain_text", "text": "Add Project"},
            "submit": {"type": "plain_text", "text": "Save"},
            "close": {"type": "plain_text", "text": "Cancel"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "title_block",
                    "label": {"type": "plain_text", "text": "Project Title"},
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "title"
                    }
                },
                {
                    "type": "input",
                    "block_id": "desc_block",
                    "label": {"type": "plain_text", "text": "Description"},
                    "element": {
                        "type": "plain_text_input",
                        "multiline": True,
                        "action_id": "description"
                    }
                },
                {
                    "type": "input",
                    "block_id": "tech_block",
                    "label": {"type": "plain_text", "text": "Tech Stack"},
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "tech"
                    }
                }
            ]
        }


add_project_view={
    
}
