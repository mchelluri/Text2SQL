import nltk
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

# Initialize stopwords
stop_words = set(stopwords.words('english'))

# Enhanced function to map POS tags to SQL parts
def map_pos_to_sql(tagged_tokens):
    sql_parts = {
        'SELECT': [],
        'FROM': [],
        'WHERE': [],
        'JOIN': [],
        'ORDER BY': [],
        'GROUP BY': []
    }

    # Define keywords
    select_keywords = {'give', 'show', 'list', 'display', 'select'}
    table_keywords = {'table', 'database', 'from'}
    condition_keywords = {'where', 'condition', 'named', 'with', 'having'}
    join_keywords = {'join'}
    order_keywords = {'order', 'sort'}
    group_keywords = {'group'}

    current_clause = None
    table_detected = False

    for word, tag in tagged_tokens:
        word_lower = word.lower()

        if word_lower in stop_words:
            continue

        if word_lower in select_keywords:
            current_clause = 'SELECT'
            continue

        if word_lower in table_keywords:
            current_clause = 'FROM'
            table_detected = True
            continue

        if word_lower in condition_keywords:
            current_clause = 'WHERE'
            continue

        if word_lower in join_keywords:
            current_clause = 'JOIN'
            continue

        if word_lower in order_keywords:
            current_clause = 'ORDER BY'
            continue

        if word_lower in group_keywords:
            current_clause = 'GROUP BY'
            continue

        if current_clause:
            if table_detected and current_clause == 'FROM':
                sql_parts[current_clause].append(word)
                table_detected = False
            else:
                sql_parts[current_clause].append(word)

    return sql_parts

# Enhanced function to convert English statement to SQL query
def english_to_sql(english_statement):
    # Tokenize and tag the words in the statement
    tokens = word_tokenize(english_statement)
    tagged_tokens = pos_tag(tokens)

    # Map POS tags to SQL parts
    sql_parts = map_pos_to_sql(tagged_tokens)

    # Construct the final SQL query
    select_clause = "SELECT " + ", ".join(sql_parts['SELECT']) if sql_parts['SELECT'] else ""
    from_clause = "FROM " + ", ".join(sql_parts['FROM']) if sql_parts['FROM'] else ""
    where_clause = "WHERE " + " AND ".join(sql_parts['WHERE']) if sql_parts['WHERE'] else ""
    join_clause = "JOIN " + " JOIN ".join(sql_parts['JOIN']) if sql_parts['JOIN'] else ""
    order_by_clause = "ORDER BY " + ", ".join(sql_parts['ORDER BY']) if sql_parts['ORDER BY'] else ""
    group_by_clause = "GROUP BY " + ", ".join(sql_parts['GROUP BY']) if sql_parts['GROUP BY'] else ""

    sql_query = f"{select_clause} {from_clause} {join_clause} {where_clause} {group_by_clause} {order_by_clause};"

    return sql_query.strip()

# Example usage
if __name__ == "__main__":
    english_statement = "give the list of all customers from the customers table where age is more than 30"
    sql_query = english_to_sql(english_statement)
    print("Generated SQL Query:")
    print(sql_query)