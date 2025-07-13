def recognize_yesno(input_text: str) -> str:
    if input_text == 'yes' or input_text == 'y' or input_text =='si' or input_text =='s':
        return 'yes'
    elif input_text == 'no' or input_text == 'n':
        return 'no'
    else:
        return 'bho'