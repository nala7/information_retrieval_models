def spacy_process(text):
    import spacy
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)

    # Tokenization and lemmatization are done with the spacy nlp pipeline commands
    lemma_list = []
    for token in doc:
        lemma_list.append(token.lemma_)
    print("Tokenize+Lemmatize:")
    print(lemma_list)

    # Filter the stopword
    filtered_sentence = []
    for word in lemma_list:
        lexeme = nlp.vocab[word]
        if lexeme.is_stop == False:
            filtered_sentence.append(word)

            # Remove punctuation
    punctuations = "?:!.,;"
    for word in filtered_sentence:
        if word in punctuations:
            filtered_sentence.remove(word)
    print(" ")
    print("Remove stopword & punctuation: ")
    print(filtered_sentence)
