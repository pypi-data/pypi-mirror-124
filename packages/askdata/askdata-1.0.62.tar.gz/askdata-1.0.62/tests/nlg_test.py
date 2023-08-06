from askdata.NLG import nlg

if __name__ == "__main__":
    json = "[{'player': 'Cristiano Ronaldo', 'goals': 10, 'team': 'Juventus'},{'player': 'Roberto Baggio', 'goals': 2, 'team': 'Milan'}]"
    examples = ["{{player}} scored {{goals}} goals for {{team}}"]
    example_sentences = ["Crisriano Ronaldo scored 3 goals for Juventus"]
    example_records = ["{'player': 'Cristiano Ronaldo', 'goal':3, 'team' : 'Juventus'}"]
    res = nlg(json=json, examples=examples, example_sentences=example_sentences, example_records=example_records)
    print(res)
