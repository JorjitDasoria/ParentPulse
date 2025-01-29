import openai
import gradio as gr
import datetime
import calendar

openai.api_key = ""

messages = [{"role": "system", "content": "You are a medical wellbeing expert that specialises in helping parents deal with stress and wellbeing of themselves."}]

def CustomChatGPT(user_input):
    try:
        messages.append({"role": "user", "content": user_input})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        ChatGPT_reply = response.choices[0].message["content"]
        messages.append({"role": "assistant", "content": ChatGPT_reply})
        return messages[1:]  # Exclude the system message
    except Exception as e:
        return [{"role": "error", "content": f"Error: {str(e)}"}]

def toggle_theme(dark_mode):
    if dark_mode:
        return gr.update(
            css="""
                body {background-color: #181818; color: #f1f1f1;}
                .chatbot {background-color: #282828; border: 1px solid #444;}
                textarea {background-color: #282828; color: #f1f1f1; border: 1px solid #444;}
                button {background-color: #444; color: #f1f1f1; border: 1px solid #555;}
            """
        )
    else:
        return gr.update(css="")

def clear_chat():
    global messages
    messages = [{"role": "system", "content": "You are a medical wellbeing expert that specialises in helping parents deal with stress and wellbeing of themselves."}]
    return []

# Calendar page function (more advanced)
def generate_calendar(year, month):
    cal = calendar.monthcalendar(year, month)
    days = []
    for week in cal:
        days.append([str(day) if day != 0 else "" for day in week])
    return days

def on_date_select(date):
    # Placeholder function to handle date selection (can be extended to show events or notes)
    return f"You selected: {date}"

# Define the app layout
with gr.Blocks(css=".container { max-width: 600px; margin: auto; }") as demo:
    with gr.Row():
        # Top left button for the calendar page
        calendar_button = gr.Button("Open Calendar", elem_id="calendar_button")
    
    # Main Chatbot page
    with gr.Tab("Chatbot"):
        gr.Markdown(
            """
            <div style="text-align: center;">
                <h1>🤱 ParentPulse: Your Wellbeing Companion 🧘</h1>
                <p>Get expert advice on stress management and wellbeing for parents. Type your question below, and I'll provide helpful insights.</p>
            </div>
            """
        )
        with gr.Row(elem_id="chat_row"):
            chatbot = gr.Chatbot(label="Chat", elem_id="chat_window", type="messages")
        with gr.Row(elem_id="input_row"):
            user_input = gr.Textbox(
                placeholder="Type your question here...",
                label="Your Question",
                lines=2,
                elem_id="user_input",
            )
        with gr.Row(elem_id="button_row"):
            submit_button = gr.Button("Submit", elem_id="submit_button")
            clear_button = gr.Button("Clear", elem_id="clear_button")
        with gr.Row(elem_id="theme_row"):
            theme_toggle = gr.Checkbox(label="Dark Mode", value=True, elem_id="dark_mode")

        # Button functionality
        submit_button.click(
            CustomChatGPT,
            inputs=user_input,
            outputs=chatbot,
            queue=False
        )

        clear_button.click(
            clear_chat,
            inputs=None,
            outputs=chatbot,
            queue=False
        )

        theme_toggle.change(
            toggle_theme,
            inputs=theme_toggle,
            outputs=None  # Only updates the CSS
        )

        # Apply dark mode by default on launch
        toggle_theme(True)

    # Calendar page
    with gr.Tab("Calendar"):
        # Dropdown for selecting the month and year
        with gr.Row():
            year = gr.Number(value=datetime.datetime.now().year, label="Year", interactive=True)
            month = gr.Number(value=datetime.datetime.now().month, label="Month", interactive=True)
            calendar_button = gr.Button("Generate Calendar", elem_id="generate_calendar_button")
        
        # Output calendar grid
        calendar_output = gr.Dataframe(headers=["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"], interactive=True)

        # Handle the calendar generation
        calendar_button.click(
            generate_calendar,
            inputs=[year, month],
            outputs=calendar_output
        )

        # Add event selection when a date is clicked
        date_selected = gr.Textbox(label="Selected Date", interactive=False)
        calendar_output.select(
            on_date_select,
            inputs=[calendar_output],
            outputs=date_selected
        )

    # Launch the app
    demo.launch(share=True)
