from info_extraction.nlp import spacy_process


example = 'Patients who in late middle age have smoked' \
              ' 20 cigarettes a day since their teens constitute' \
              ' an at-risk group. One thing they’re clearly at ' \
              'risk for is the acute sense of guilt that a clinician' \
              ' can incite, which immediately makes a consultation tense.'

print('SPACY')
spacy_process(example)