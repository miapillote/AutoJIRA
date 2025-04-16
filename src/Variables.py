
URL = {
    'landing': 'https://service.rochester.edu/servicedesk/customer/portal/101/create/358?q=lending&q_time=1693601714516'
}

TEXT = {
    'ticket_signature': "This ticket was automatically generated by the Rettner 201 Helpdesk. If you have received this in error, you may contact the desk at rettnerhelpdesk@ur.rochester.edu.",
}

XPATH = {
    'customer_element': '//*[@id="react-select-2-input"]',
    'source_element': '//*[@id="react-select-customfield_10808-instance-input"]',
    'summary_element': '//*[@id="summary"]',
    'description_element': '//*[@id="ak-editor-textarea"]',
    'resolve_element': '//*[@id="com.atlassian.servicedesk:workflow-transition-761"]',
    'submit_element': '/html/body/section/form',
    'open_ticket_element': '//*[@id="content"]/div/header/div/div/div[2]/div[2]/div/ol/li[3]/a',
    'assign_to_me_element': '//*[@id="assign-to-me"]',
    'people_dropdown_element': '//*[@id="peoplemodule-label"]/button/span',
    'transition_bar_element': '//*[@id="opsbar-transitions_more"]/span',
    'close_button_element': '//*[@id="action_id_941"]/a/div/div[1]',
}

PATH = {
    'chrome': r'--user-data-dir=C:/Users/rettnerhelpdesk/AppData/Local/Google/Chrome',
    'profile': '--profile-directory=Profile 4'
}
