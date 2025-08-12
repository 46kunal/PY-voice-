import wikipedia

wikipedia.set_lang("en")

def get_wikipedia_summary(query):
    try:
        return wikipedia.summary(query, sentences=2)
    except wikipedia.exceptions.DisambiguationError as e:
        return f"The topic is ambiguous. Did you mean: {', '.join(e.options[:3])}?"
    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn't find any info on that topic."
    except Exception as e:
        print("❌ Wikipedia Error:", e)
        return "Failed to get information from Wikipedia."
