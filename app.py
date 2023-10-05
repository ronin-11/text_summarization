import streamlit as st
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

# Load the spaCy model and stopwords
nlp = spacy.load('en_core_web_sm')
stopwords = list(STOP_WORDS)
punctuation = punctuation + '\n'

def text_summarization(text):
    doc = nlp(text)

    # Word frequency calculation
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1

    # Calculate maximum word frequency
    max_frequency = max(word_frequencies.values())

    # Normalize word frequencies
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency

    # Sentence tokenization
    sentence_tokens = [sent for sent in doc.sents]

    # Calculate sentence scores
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]

    # Select top sentences for summary
    select_length = int(len(sentence_tokens) * 0.3)
    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)

    return summary

def main():
    st.title("Text Summarization App")
    st.write("Upload a document and get a summary!")

    uploaded_file = st.file_uploader("Upload a file", type=["txt","docx"])
    if uploaded_file is not None:
        text = uploaded_file.read().decode('utf-8')

        if st.button("Summarize"):
            summary = text_summarization(text)
            st.header("Summary")
            st.write(summary)

if __name__ == "__main__":
    main()
