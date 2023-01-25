#import libs
import openai 
import streamlit as st
import docx

# pip install streamlit-chat  
from streamlit_chat import message

openai.api_key = st.secrets['openai-secret']

#add title to 
st.title("chatBot : OpenAI")

#Temp selctor
with st.sidebar:
    # Create a slider to control the temperature of the model
    temperature = st.slider("Increase the temperature for wider variations", 
        min_value=0.0, 
        max_value=1.0, 
        value=0.8, 
        step=0.1)
    max_tokens = st.number_input('Insert max tokens (1 token = 3/4 words)',
        min_value=0, 
        max_value=4096,
        value=2000)

def generate_response(prompt):
        completions = openai.Completion.create(
            engine="text-davinci-003", #Select Model
            prompt = prompt,
            temperature = temperature, #0-1 Higher the temp, the more liberties it takes 
            top_p = 1,
            max_tokens = max_tokens, #1 Token = 3/4 word
            frequency_penalty = 0,
            presence_penalty = 0
    )
        return completions.choices[0].text

uploaded_file = st.file_uploader("Choose a doc file")

if uploaded_file is not None:
    doc = docx.Document(uploaded_file)
    paras = '\n'.join([p.text for p in doc.paragraphs if p.text]   )
    paras.splitlines()
    st.write(paras)

# Storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'history' not in st.session_state:
    st.session_state['history'] = []
    
# We will get the user's input by calling the get_text function
def get_text():
    input_text = st.text_input('You', placeholder='Type Prompt that goes with file here', key="001")
    return input_text

if st.session_state['generated'] == [] and uploaded_file is not None:
    #Get user response
    user_input = get_text() + paras
else:
    #Get user response
    user_input = get_text()

if user_input:
    
    #Store the input
    st.session_state.history.append(user_input)

    #Get the conversation history
    #conversation_history = '\n'.join(list(itertools.chain.from_iterable(zip(st.session_state['past'],st.session_state['generated'] ))))
    conversation_history = '\n'.join(st.session_state['history'])
    output = generate_response(conversation_history)

    #Store the chat
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)
    st.session_state.history.append(output)

if st.session_state['generated']:
    
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
