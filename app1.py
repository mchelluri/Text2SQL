import nltk
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
import streamlit as st

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

# Initialize stopwords
stop_words = set(stopwords.words('english'))


# Function to convert English statement to SQL query
def english_to_sql(english_statement):
    # Tokenize and tag the words in the statement
    tokens = word_tokenize(english_statement)
    tagged = pos_tag(tokens)

    # Initialize SQL parts
    sql_parts = {
        'SELECT': [],
        'FROM': [],
        'WHERE': [],
        'JOIN': [],
        'ORDER BY': [],
        'GROUP BY': [],
        'HAVING': []
    }

    # Remove stopwords and parse tokens
    filtered_words = [word for word in tokens if word.lower() not in stop_words]

    # Parse the tagged tokens to form SQL query parts
    i = 0
    while i < len(tagged):
        word, tag = tagged[i]
        if tag.startswith('VB'):  # Verb tags
            if word.lower() == 'create':
                if 'database' in filtered_words:
                    sql_parts['SELECT'].append(f"CREATE DATABASE {filtered_words[-1]}")
                    break
                elif 'table' in filtered_words:
                    table_name = filtered_words[filtered_words.index('table') + 1]
                    sql_parts['SELECT'].append(f"CREATE TABLE {table_name} (id INT PRIMARY KEY)")
                    break
        elif tag.startswith('NN'):  # Noun tags
            if 'SELECT *' not in sql_parts['SELECT']:
                if i == 0:
                    sql_parts['SELECT'].append(word)
                else:
                    sql_parts['SELECT'].append(word)
        elif tag == 'IN':  # Preposition tags
            if word.lower() == 'in':
                sql_parts['FROM'].append(tagged[i + 1][0])
        elif tag == 'CD':  # Cardinal numbers
            sql_parts['WHERE'].append(f"total_sales >= {word.replace('k$', '000')}")
        elif tag == 'JJ' or tag == 'NNP':  # Adjectives or proper nouns
            if word.lower() in ['women', 'apparel', 'ga']:
                sql_parts['WHERE'].append(f"{tagged[i - 1][0]} = '{word}'")
        elif word.lower() == 'select':
            sql_parts['SELECT'].append('*')
        elif word.lower() == 'order':
            if tagged[i + 1][0].lower() == 'by':
                sql_parts['ORDER BY'].append(tagged[i + 2][0])

        i += 1

    # Construct the final SQL query
    select_clause = "SELECT " + ", ".join(sql_parts['SELECT'])
    from_clause = "FROM " + ", ".join(sql_parts['FROM']) if sql_parts['FROM'] else ""
    where_clause = "WHERE " + " AND ".join(sql_parts['WHERE']) if sql_parts['WHERE'] else ""
    group_by_clause = "GROUP BY " + ", ".join(sql_parts['GROUP BY']) if sql_parts['GROUP BY'] else ""
    having_clause = "HAVING " + " AND ".join(sql_parts['HAVING']) if sql_parts['HAVING'] else ""
    order_by_clause = "ORDER BY " + ", ".join(sql_parts['ORDER BY']) if sql_parts['ORDER BY'] else ""

    sql_query = f"{select_clause} {from_clause} {where_clause} {group_by_clause} {having_clause} {order_by_clause};"

    return sql_query.strip()


# Streamlit application
def main():
    st.title("English to SQL Converter")

    st.write("Enter an English statement to convert it to an SQL query.")
    english_statement = st.text_input("English Statement")

    if st.button("Generate SQL Query"):
        sql_query = english_to_sql(english_statement)
        st.write("Generated SQL Query:")
        st.code(sql_query)


if __name__ == "__main__":
    main()